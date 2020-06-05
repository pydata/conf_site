import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

DEBUG = True
EMAIL_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    }
}

# override this in production
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

FILE_UPLOAD_PERMISSIONS = 0o644

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing
# Override this in production.py
SECRET_KEY = "6h(o)acs$22!=5z9!@j(cqon%vmfa+=33uf^1ym(vsllqa9gif"

TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "constance.context_processors.config",
                "wagtailmenus.context_processors.wagtailmenus",
                "wagtail.contrib.settings.context_processors.settings",
                "conf_site.core.context_processors.core_context",
                "conf_site.cms.context_processors.homepage_context",
            ]
        },
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "conf_site.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "conf_site.wsgi.application"

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "analytical",
    "constance",
    "crispy_forms",
    "easy_thumbnails",
    "modelcluster",
    "pinax.eventlog",
    "rest_framework",
    "reversion",
    "symposion",
    "symposion.conference",
    "symposion.proposals",
    "symposion.schedule",
    "symposion.speakers",
    "symposion.sponsorship",
    "taggit",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "wagtailmenus",

    "conf_site",
    "conf_site.cms",
    "conf_site.core",
    "conf_site.proposals",
    "conf_site.reviews",
    "conf_site.schedule",
    "conf_site.speakers",
    "conf_site.sponsorship",
]

# Note that this logging configuration DOES NOT SEND ERROR REPORTS
# BY EMAIL. If this functionality is
# needed, simply delete this section to restore the default
# LOGGING setting
# (see https://docs.djangoproject.com/en/1.11/ref/settings/#logging).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        }
    },
    "loggers": {
        "django": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

ADMINS = (
    ('Admins', 'web@pydata.org'),
)
MANAGERS = [("PyData Admin", "admin@pydata.org"), ]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_DISPLAY = lambda user: user.email      # noqa: E731
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USERNAME_REQUIRED = False

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
CACHE_TIMEOUT_SHORT = 60                            # One minute.
CACHE_TIMEOUT_MEDIUM = CACHE_TIMEOUT_SHORT * 60     # One hour.
CACHE_TIMEOUT_LONG = CACHE_TIMEOUT_MEDIUM * 24      # One day.
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "localhost:6379",
    }
}
CONFERENCE_ID = 1
CONSTANCE_CONFIG = {
    "BLIND_AUTHORS": (
        True,
        "Hide identities of reviewers from authors.",
        bool,
    ),
    "BLIND_REVIEWERS": (
        False,
        "Hide identities of authors from reviewers.",
        bool,
    ),
    "PROPOSAL_EDITING_WHEN_CFP_IS_CLOSED": (
        True,
        "If submitters can make changes to a proposal if the CFP is closed.",
        bool,
    ),
    "PROPOSAL_KEYWORDS": (False, "Support proposal keywords.", bool),
    "PROPOSAL_URL_FIELDS": (
        False,
        "Show slides & code repository fields on proposal submission form.",
        bool,
    ),
    "PROPOSALS_PER_PAGE": (
        50,
        "Number of proposals shown per page in the reviewing section",
        int,
    ),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "Proposal Options": (
        "PROPOSAL_EDITING_WHEN_CFP_IS_CLOSED",
        "PROPOSAL_KEYWORDS",
        "PROPOSAL_URL_FIELDS",
        "PROPOSALS_PER_PAGE",
    ),
    "Reviewing Options": ("BLIND_AUTHORS", "BLIND_REVIEWERS"),
}
CRISPY_TEMPLATE_PACK = "bootstrap3"
CSRF_FAILURE_VIEW = "conf_site.core.views.csrf_failure"
DEFAULT_PROPOSAL_FORM = "conf_site.proposals.forms.ProposalForm"
LOGIN_REDIRECT_URL = "dashboard"
PROPOSAL_FORMS = {
    "talk": "conf_site.proposals.forms.ProposalForm",
    "tutorial": "conf_site.proposals.forms.ProposalForm",
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage")
SYMPOSION_PAGE_REGEX = r"(([\w-]{1,})(/[\w-]{1,})*)/"
TAGGIT_CASE_INSENSITIVE = True
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_MODERATION_ENABLED = False
