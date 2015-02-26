import os

from .base import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES['default']['HOST'] = os.environ.get('DB_HOST', 'localhost')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['default']['PASSWORD'] = os.environ['DB_PASSWORD']
