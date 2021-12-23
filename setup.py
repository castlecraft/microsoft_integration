from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in microsoft_integration/__init__.py
from microsoft_integration import __version__ as version

setup(
	name="microsoft_integration",
	version=version,
	description="Microsoft Integration for Frappe Framework",
	author="Castlecraft Ecommerce Pvt. Ltd.",
	author_email="support@castlecraft.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
