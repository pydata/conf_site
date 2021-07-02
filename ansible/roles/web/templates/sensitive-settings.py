# Passwords, API keys, and other sensitive information.
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from conf_site.settings.base import INSTALLED_APPS


DATABASES_DEFAULT = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "{{ django_database }}",
    "USER": "{{ database_user }}",
    "PASSWORD": "{{ database_password }}",
    "HOST": "{{ database_host }}",
    "PORT": "",
}


SECRET_KEY = "{{ django_secret_key }}"
SESSION_COOKIE_PATH = "{{ subdirectory }}" or "/"

DATE_FORMAT = "{{ date_format }}"
TIME_FORMAT= "{{ time_format }}"
TIME_ZONE = "{{ timezone }}"
DATETIME_FORMAT= "{{ date_format }} {{ time_format }}"

DEFAULT_FROM_EMAIL = "{{ default_email }}"
SERVER_EMAIL = "{{ default_email }}"
EMAIL_USE_TLS = True
EMAIL_HOST = '{{ email_host_name }}'
EMAIL_HOST_USER = '{{ email_host_user }}'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_PORT = '587'
# Determine which email backend to use. Note that previous variables
# are only relevant to the SMTP backend.
{% if postmark_api_token and environment_type != "development" %}
EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"
ANYMAIL = {
    "POSTMARK_SEND_DEFAULTS": {
        "esp_extra": {"MessageStream": "{{ conference_identifier }}"},
    },
    "POSTMARK_SERVER_TOKEN": "{{ postmark_api_token }}",
}
{% elif environment_type != "development" %}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
{% else %}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
{% endif %}

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = {% if subdirectory %}True{% else %}False{% endif %}


WEBSITE_URL = "{{ website_url }}"
LOGIN_URL = "{{ website_url }}/accounts/login/"
LOGO_URL = "{{ logo_url }}"
MEDIA_URL = "{{ website_url }}/media/"
STATIC_URL = "{{ website_url }}/static/"

SENTRY_PUBLIC_DSN = (
    "https://{{ sentry_public_key }}@sentry.io/{{ sentry_project_id }}"
)

{% if environment_type != "development" %}
sentry_sdk.init(
    dsn=SENTRY_PUBLIC_DSN,
    environment="{{ environment_type }}",
    integrations=[DjangoIntegration(), RedisIntegration()],
    release="{{ git_status.stdout }}",
    server_name="{{ conference_identifier }}",
    traces_sample_rate=0.1,
)
{% endif %}

GOOGLE_ANALYTICS_PROPERTY_ID = "{{ google_analytics_id }}"
{% if github_oauth_client_id is defined %}
INSTALLED_APPS = INSTALLED_APPS + ["allauth.socialaccount.providers.github"]
{% endif %}
{% if google_oauth_client_id is defined %}
INSTALLED_APPS = INSTALLED_APPS + ["allauth.socialaccount.providers.google"]
{% endif %}
SOCIALACCOUNT_PROVIDERS = {
    {% if github_oauth_client_id is defined %}"github": {
        "APP": {
            "client_id": "{{ github_oauth_client_id }}",
            "secret": "{{ github_oauth_client_secret }}",
        }
    },{% endif %}
    {% if google_oauth_client_id is defined %}"google": {
        "APP": {
            "client_id": "{{ google_oauth_client_id }}",
            "secret": "{{ google_oauth_client_secret }}",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },{% endif %}
}
