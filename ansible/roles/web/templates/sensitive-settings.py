# Passwords, API keys, and other sensitive information.

DATABASES_DEFAULT = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "{{ django_database }}",
    "USER": "{{ database_user }}",
    "PASSWORD": "{{ database_password }}",
    "HOST": "{{ database_host }}",
    "PORT": "",
}


SECRET_KEY = "{{ django_secret_key }}"
SESSION_COOKIE_PATH = "{{ subdirectory }}" or "/"
TIME_FORMAT = "{{ time_format }}"
TIME_ZONE = "{{ timezone }}"

DEFAULT_FROM_EMAIL = "{{ default_email }}"
SERVER_EMAIL = "{{ default_email }}"
EMAIL_USE_TLS = True
EMAIL_HOST = '{{ email_host_name }}'
EMAIL_HOST_USER = '{{ email_host_user }}'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_PORT = '587'
# Determine which email backend to use. Note that previous variables
# are only relevant to the SMTP backend.
{% if sendgrid_api_key and environment_type != "development" %}
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = "{{ sendgrid_api_key }}"
{% elif environment_type != "development" %}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
{% else %}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
{% endif %}

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = {% if subdirectory %}True{% else %}False{% endif %}


LOGIN_URL = "{{ website_url }}/account/login/"
MEDIA_URL = "{{ website_url }}/media/"
STATIC_URL = "{{ website_url }}/static/"

{% if environment_type != "development" and sentry_secret_key != "" %}
RAVEN_CONFIG = {
    "dsn": ("https://{{ sentry_public_key }}:{{ sentry_secret_key }}@sentry.io"
            "/{{ sentry_project_id }}"),
    "environment": "{{ environment_type }}",
    "name": "{{ conference_identifier }}",
    "processors": ("raven.processors.SanitizePasswordsProcessor", ),
    "release": "{{ git_status.stdout }}",
    "site": "{{ conference_name }}",
}
SENTRY_PUBLIC_DSN = "https://{{ sentry_public_key }}@sentry.io/{{ sentry_project_id }}"
{% else %}
SENTRY_PUBLIC_DSN = False
{% endif %}

GOOGLE_ANALYTICS_PROPERTY_ID = "{{ google_analytics_id }}"

SETTINGS_EXPORT = [
    "GOOGLE_ANALYTICS_PROPERTY_ID",
    "SENTRY_PUBLIC_DSN",
]
WAGTAIL_SITE_NAME = "{{ conference_name }}"
