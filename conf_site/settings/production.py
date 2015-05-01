from .base import *  # noqa
from . import secrets


DEBUG = False
TEMPLATE_DEBUG = DEBUG
# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

DATABASES = {
    "default": secrets.DATABASES_DEFAULT,
}

SITE_ID = 1

ALLOWED_HOSTS = secrets.ALLOWED_HOSTS

SECRET_KEY = secrets.SECRET_KEY

EMAIL_BACKEND = secrets.EMAIL_BACKEND
EMAIL_USE_TLS = secrets.EMAIL_USE_TLS
EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = secrets.EMAIL_PORT
