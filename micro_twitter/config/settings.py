"""
Django settings for micro_twitter project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

from django_guid.integrations import CeleryIntegration
from environs import Env

env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key
SECRET_KEY = env.str("SECRET_KEY")

# https://docs.djangoproject.com/en/4.2/ref/settings/#debug
DEBUG = env.bool("DEBUG", False)

# TODO.
# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", subcast="str", default=[])


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "django_guid",
    "django_celery_results",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
]
DEVELOPED_APPS = [
    "micro_twitter.common",
    "micro_twitter.users",
    "micro_twitter.timeline",
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + DEVELOPED_APPS

# https://docs.djangoproject.com/en/4.2/ref/settings/#middleware
MIDDLEWARE = [
    "django_guid.middleware.guid_middleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#root-urlconf
ROOT_URLCONF = "micro_twitter.config.urls"

# https://docs.djangoproject.com/en/4.2/ref/settings/#wsgi-application
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "micro_twitter.config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": 5432,
    }
}

# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "micro_twitter.common.validators.NumberPasswordValidator",
    },
    {
        "NAME": "micro_twitter.common.validators.UpperCasePasswordValidator",
    },
    {
        "NAME": "micro_twitter.common.validators.LowerCasePasswordValidator",
    },
    {
        "NAME": "micro_twitter.common.validators.SymbolPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "10/min", "user": "1000/day"},
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}

# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": "MicroTwitter API",
    "DESCRIPTION": "API documentation for MicroTwitter application.",
    "VERSION": "1.0.0",
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# https://docs.djangoproject.com/en/4.2/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/4.2/ref/settings/#time-zone
TIME_ZONE = env.str("TIME_ZONE", "Africa/Cairo")

# https://docs.djangoproject.com/en/4.2/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/4.2/ref/settings/#use-tz
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR, "uploads")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 21600, "max_retries": 2}
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", "django-db")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXTENDED = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_POOL_LIMIT = env.int("CELERY_BROKER_POOL_LIMIT", 10)
CELERY_BROKER_CONNECTION_TIMEOUT = env.int("CELERY_BROKER_CONNECTION_TIMEOUT", 2)
CELERY_TASK_TIME_LIMIT = env.int("CELERY_TASK_TIME_LIMIT", 600)
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", True
)

# Emails.
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", "webmaster@localhost")


# Logging request correlation ID and celery tasks IDs.
DJANGO_GUID = {
    "INTEGRATIONS": [
        CeleryIntegration(
            use_django_logging=True,
            log_parent=True,
        )
    ],
}

# Logging Settings.
BASE_LOGGING_DIR = Path(BASE_DIR, "logs")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
        "celery_tracing": {
            "()": "django_guid.integrations.celery.log_filters.CeleryTracing"
        },
    },
    "formatters": {
        "simple": {
            "format": (
                "[{asctime}] [{levelname}] [{correlation_id}] [{celery_parent_id}]"
                " [{celery_current_id}] [{name}]: {message}"
            ),
            "style": "{",
        },
        "verbose": {
            "format": (
                "[{asctime}] [{levelname}] [{correlation_id}] [{celery_parent_id}]"
                " [{celery_current_id}] [{name}] [{funcName}():{lineno}]: {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["correlation_id", "celery_tracing"],
        },
        "info_level_handler": {
            "level": "INFO",
            "filters": ["correlation_id", "celery_tracing"],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "filename": Path(BASE_LOGGING_DIR, "main.log"),
            "formatter": "simple",
        },
        "warning_level_handler": {
            "level": "WARNING",
            "filters": ["correlation_id", "celery_tracing"],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "filename": Path(BASE_LOGGING_DIR, "errors.log"),
            "formatter": "verbose",
        },
        "email_handler": {
            "level": "INFO",
            "filters": ["correlation_id", "celery_tracing"],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "filename": Path(BASE_LOGGING_DIR, "email.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["warning_level_handler", "console"],
            "propagate": False,
            "level": "WARNING",
        },
        "email_logger": {
            "handlers": ["email_handler", "warning_level_handler"],
            "propagate": False,
            "level": "INFO",
        },
    },
}
