# Top settings file for development
from .base import *     # noqa: F403
from .secrets import *  # noqa: F403

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

SITE_ID = 2
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]

DATABASES = {
    "default": DATABASES_DEFAULT,
}

MIDDLEWARE_CLASSES = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE_CLASSES                          # noqa: F405
INSTALLED_APPS += ["debug_toolbar", ]               # noqa: F405
INTERNAL_IPS = "127.0.0.1"

LOGGING["loggers"]["django.request"]["level"] = "DEBUG"    # noqa: F405
