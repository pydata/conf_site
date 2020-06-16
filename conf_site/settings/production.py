from conf_site.settings.base import *  # noqa: F403
from conf_site.settings.secrets import *  # noqa: F403


DEBUG = False
# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

DATABASES = {
    "default": DATABASES_DEFAULT,       # noqa: F405
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
JUPYTERCON_BASE_URL = "https://jupytercon.com"
SECURE_SSL_REDIRECT = True
