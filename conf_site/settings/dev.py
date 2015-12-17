# Top settings file for development
from .base import *  # noqa
from . import secrets

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

SITE_ID = 2
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]

DATABASES = {
    "default": secrets.DATABASES_DEFAULT,
}

INSTALLED_APPS += [
    "debug_toolbar",
]

LOGGING["loggers"]["django.request"]["level"] = "DEBUG"

FORCE_SCRIPT_NAME = secrets.FORCE_SCRIPT_NAME
USE_X_FORWARDED_HOST = secrets.USE_X_FORWARDED_HOST

LOGIN_URL = secrets.LOGIN_URL
MEDIA_URL = secrets.MEDIA_URL
STATIC_URL = secrets.STATIC_URL
