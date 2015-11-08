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


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = '{{ email_host_name }}'
EMAIL_HOST_USER = 'noreply@pydata.org'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_PORT = '587'
ALLOWED_HOSTS = ['*']

MEDIA_URL = "{{ website_url }}/media/"
STATIC_URL = "{{ website_url }}/static/"
