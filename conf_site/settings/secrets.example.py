# Example secrets file for production.
# Replace values with your production settings.
#
# People also use environment variables rather than a secrets file, but for new
# users importing from a file is easier to understand


DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pydata_seattle2015',
        'USER': 'pydata_seattle2015',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SECRET_KEY = ''

# EMAIL_BACKEND = "mailer.backend.DbBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
ALLOWED_HOSTS = ['*']

WAGTAIL_SITE_NAME = "PyData Seattle 2015"
