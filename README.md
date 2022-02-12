## Microsoft Integration

Microsoft Integration for Frappe Framework

### Usage

Install as a standard frappe-bench app.

Add a `Social Login Key` with your Microsoft Azure AD credentials.

Example Social Login Key JSON:

```json
{
  "enable_social_login": 1,
  "provider_name": "Azure AD B2C",
  "social_login_provider": "Custom",
  "client_id": "96752e67-57d3-4c03-99d5-e57e28c30ef0",
  "client_secret": "*************************************",
  "base_url": "https://login.microsoftonline.com/95228b0c-0fd6-43d9-857c-95130599dd30",
  "authorize_url": "/oauth2/v2.0/authorize",
  "access_token_url": "/oauth2/v2.0/token",
  "redirect_url": "http://localhost:8000/api/method/microsoft_integration.callback.azure_ad_b2c",
  "api_endpoint": "https://graph.microsoft.com/oidc/userinfo",
  "custom_base_url": 1,
  "api_endpoint_args": "",
  "auth_url_data": "{\"scope\": \"openid profile email\", \"response_type\": \"code\"}",
  "user_id_property": "sub"
}
```

Notes:
  - Replace the `redirect_url` with appropriate working url of frappe/erpnext site.
  - Base URL is `https://login.microsoftonline.com/{tenant_id}`
  - Use appropriate `client_id` and `client_secret`.
  - Microsoft JWKS URL is configurable using `microsoft_jwks_url` key in `site_config.json`. Defaults to `https://login.microsoftonline.com/common/discovery/v2.0/keys`.
  - Use name of the provider as `Azure AD B2C` as it will be converted to snake case `azure_ad_b2c` for callback. If you need to change the name, configure the snake case name using `azure_provider_key` key in `site_config.json`. Defaults to `azure_ad_b2c`.

#### License

MIT
