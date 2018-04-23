from .base import *  # noqa: F403
from .secrets import *  # noqa: F403


DEBUG = True

DATABASES = {
    "default": DATABASES_DEFAULT,       # noqa: F405
}

SITE_ID = 1

SECURE_SSL_REDIRECT = True
