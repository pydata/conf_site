# Top settings file for development
from .base import *  # noqa

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['localhost', '0.0.0.0']
