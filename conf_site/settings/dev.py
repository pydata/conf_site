# Top settings file for development
from .base import *  # noqa
from . import secrets

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

SITE_ID = 2
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]

INSTALLED_APPS += [
    "debug_toolbar",
]

LOGGING["loggers"]["django.request"]["level"] = "DEBUG"

