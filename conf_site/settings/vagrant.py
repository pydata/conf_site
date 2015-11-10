from .base import *  # noqa
from . import secrets

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG
SITE_ID = 2
ALLOWED_HOSTS = ["*"]
LOGGING["loggers"]["django.request"]["level"] = "DEBUG"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "seattle2015",
        "USER": "seattle2015",
        # ubuntu's default pg_hba.conf allows passwordless connections from localhost
        # when a user connects to a database with the same name as the user
    }
}

INSTALLED_APPS += [
    "debug_toolbar",
]


SECRET_KEY = secrets.SECRET_KEY
EMAIL_BACKEND = secrets.EMAIL_BACKEND
EMAIL_USE_TLS = secrets.EMAIL_USE_TLS
EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = secrets.EMAIL_PORT

LOGIN_URL = secrets.LOGIN_URL
MEDIA_URL = secrets.MEDIA_URL
STATIC_URL = secrets.STATIC_URL

try:
    # local local settings if they exist
    from .local import *
except:
    pass
