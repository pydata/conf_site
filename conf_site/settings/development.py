# Top settings file for development
from conf_site.settings.base import *     # noqa: F403
from conf_site.settings.secrets import *  # noqa: F403

COMPRESS_ENABLED = False
DEBUG = True
SERVE_MEDIA = DEBUG

ALLOWED_HOSTS = ["localhost", "0.0.0.0"]

DATABASES = {
    "default": DATABASES_DEFAULT,                   # noqa: F405
}

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE                                  # noqa: F405
INSTALLED_APPS += ["debug_toolbar", ]               # noqa: F405
INTERNAL_IPS = "127.0.0.1"
