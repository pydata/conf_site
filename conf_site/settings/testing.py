from conf_site.settings.base import *    # noqa: F401,F403

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "testing",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "", }
}

GOOGLE_ANALYTICS_PROPERTY_ID = "UA-000000-0"
SECRET_KEY = "foobar"
SENTRY_PUBLIC_DSN = False
SETTINGS_EXPORT = [
    "GOOGLE_ANALYTICS_PROPERTY_ID",
    "SENTRY_PUBLIC_DSN",
]
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage")
