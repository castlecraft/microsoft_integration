import base64
import json

import frappe
import jwt
import requests
from frappe import _
from frappe.utils.oauth import login_oauth_user


@frappe.whitelist(allow_guest=True)
def azure_ad_b2c(*args, **kwargs):
    if isinstance(kwargs.get("state"), str):
        state = base64.b64decode(kwargs.get("state"))
        state = json.loads(state.decode("utf-8"))

    if not (state and state["token"]):
        frappe.respond_as_web_page(
            _("Invalid Request"), _("Token is missing"), http_status_code=417
        )

    provider = frappe.get_doc(
        "Social Login Key", frappe.get_conf().get("azure_provider_key", "azure_ad_b2c")
    )
    scope = json.loads(provider.auth_url_data).get("scope")
    data = {
        "grant_type": "authorization_code",
        "client_id": provider.client_id,
        "scope": scope,
        "code": kwargs.get("code"),
        "redirect_uri": provider.redirect_url,
        "client_secret": provider.get_password("client_secret"),
    }
    token_response = requests.post(
        url=provider.base_url + provider.access_token_url,
        data=data,
    )
    token = token_response.json()
    decoded_id_token = get_decoded_token(token.get("id_token"), provider.client_id)
    decoded_id_token["email"] = decoded_id_token.get("preferred_username")
    login_oauth_user(decoded_id_token, provider=provider.name, state=state)


def get_decoded_token(token, audience):
    r = requests.get(
        frappe.get_conf().get(
            "microsoft_jwks_url",
            "https://login.microsoftonline.com/common/discovery/v2.0/keys",
        ),
    )
    jwks_keys = r.json()
    keys = jwks_keys.get("keys")
    public_keys = {}
    for jwk in keys:
        kid = jwk["kid"]
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    kid = jwt.get_unverified_header(token)["kid"]
    key = public_keys[kid]

    return jwt.decode(
        token + "=" * (-len(token) % 4), # padded base64 string
        key=key,
        algorithms=["RS256"],
        audience=audience,
    )
