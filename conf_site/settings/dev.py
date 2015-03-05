# Top settings file for development
from .base import *  # noqa

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['localhost', '0.0.0.0']

DEV_APPS = [
    'debug_toolbar',
]

INSTALLED_APPS = BASE_APPS + DEV_APPS