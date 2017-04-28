from base import *    # noqa: F401,F403

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "travis",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "", }
}

GOOGLE_ANALYTICS_PROPERTY_ID = "UA-000000-0"
SECRET_KEY = "foobar"
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage")
