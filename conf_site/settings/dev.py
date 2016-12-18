# Top settings file for development
from .base import *     # noqa: F403
from . import secrets

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

SITE_ID = 2
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]
TIME_FORMAT = secrets.TIME_FORMAT
TIME_ZONE = secrets.TIME_ZONE

DATABASES = {
    "default": secrets.DATABASES_DEFAULT,
}

MIDDLEWARE_CLASSES = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE_CLASSES                          # noqa: F405
INSTALLED_APPS += ["debug_toolbar", ]               # noqa: F405
INTERNAL_IPS = "127.0.0.1"

LOGGING["loggers"]["django.request"]["level"] = "DEBUG"    # noqa: F405

FORCE_SCRIPT_NAME = secrets.FORCE_SCRIPT_NAME
USE_X_FORWARDED_HOST = secrets.USE_X_FORWARDED_HOST

LOGIN_URL = secrets.LOGIN_URL
MEDIA_URL = secrets.MEDIA_URL
STATIC_URL = secrets.STATIC_URL

GOOGLE_ANALYTICS_PROPERTY_ID = secrets.GOOGLE_ANALYTICS_PROPERTY_ID
