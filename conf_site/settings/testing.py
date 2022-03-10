import os

from conf_site.settings.base import *    # noqa: F401,F403

DEBUG = False

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis:6379",
    }
}
CONSTANCE_REDIS_CONNECTION = "redis://redis:6379/0"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "testing_db",
        "USER": "postgres",
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": "postgres",
        "PORT": "",
    }
}

FAVICON_URL = ""
GOOGLE_ANALYTICS_PROPERTY_ID = "UA-000000-0"
LOGO_URL = ""
SECRET_KEY = "foobar"
SENTRY_PUBLIC_DSN = False
SETTINGS_EXPORT = [
    "GOOGLE_ANALYTICS_PROPERTY_ID",
    "SENTRY_PUBLIC_DSN",
]
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage")
WEBSITE_URL = ""
