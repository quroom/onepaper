from django.utils.translation import ugettext_lazy as _

"""
Django settings for onepaper project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import random
import string
import sys

from django.contrib.messages import constants as messages
from dotenv import load_dotenv

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = ')fe%8bp3c4$*v*ghv46s+4iwbir5)vhj4p5u)4@-db6c5b3&x-'
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", ")fe%8bp3c4$*v*ghv46s+4iwbir5)vhj4p5u)4@-db6c5b3&x-"
)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get("DJANGO_DEBUG", "True") != "False"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "*").split(",")
PRODUCT = os.environ.get("DJANGO_PRODUCT", "True") == "True"
NO_CACHE_STRING = "u" + "".join(random.choices(string.digits, k=10))
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.naver",
    "rest_framework",
    "rest_framework.authtoken",
    "crispy_forms",
    "phonenumber_field",
    "multiselectfield",
    "webpack_loader",
    "django_cleanup.apps.CleanupConfig",
    "django_filters",
    "debug_toolbar",
    "django_summernote",
    "addresses",
    "helps",
    "profiles",
    "papers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

if PRODUCT == False and DEBUG == False:
    MIDDLEWARE.insert(0, "whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "onepaper.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],
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

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "onepaper.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGES = [
    ("ko-KR", _("Korean")),
    ("en-US", _("English")),
]

LANGUAGE_CODE = "ko-KR"
# LANGUAGE_CODE = 'en-US'

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), os.path.join(BASE_DIR, "frontend/dist")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

if PRODUCT == False and DEBUG == False:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

ACCOUNT_ADAPTER = "profiles.adapters.CustomAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/accounts/email/confirmed/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_FORMS = {
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    "signup": "profiles.forms.SocialCustomUserForm",
}

AUTH_USER_MODEL = "profiles.CustomUser"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

# django-crispy-forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# django.contrib.sites
SITE_ID = 1

# Phonenumber Field setting
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "KR"

# Django-REST-Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "core.utils.BrowsableAPIRendererWithoutForms",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "PAGE_SIZE": 10,
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": DEBUG,
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE": os.path.join(FRONTEND_DIR, "webpack-stats.json"),
    }
}

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
if EMAIL_HOST_PASSWORD != "":
    SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "Error <error@onepaper.biz>")
    DEFAULT_FROM_EMAIL = "Onepaper <no-reply@onepaper.biz>"
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "email-smtp.ap-northeast-2.amazonaws.com"
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

USE_S3 = os.environ.get("USE_S3", "False") != "False"

if USE_S3 and DEBUG == False:
    AWS_IS_GZIPPED = True
    GZIP_CONTENT_TYPES = (
        "text/css",
        "application/javascript",
        "application/x-javascript",
        "text/javascript",
    )
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = "ap-northeast-2"
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = os.environ.get(
        "AWS_S3_CUSTOM_DOMAIN", "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
    )
    DEFAULT_FILE_STORAGE = "onepaper.storages.S3DefaultStorage"
    STATICFILES_STORAGE = "onepaper.storages.S3StaticStorage"

if not TESTING and "RDS_HOSTNAME" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["RDS_DB_NAME"],
            "USER": os.environ["RDS_USERNAME"],
            "PASSWORD": os.environ["RDS_PASSWORD"],
            "HOST": os.environ["RDS_HOSTNAME"],
            "PORT": os.environ["RDS_PORT"],
        }
    }

SUMMERNOTE_CONFIG = {
    "attachment_require_authentication": True,
    "attachment_filesize_limit": 5242880 * 2,
    "disable_attachment": True,
}

ADMINS = [("quroom", "quroom@naver.com")]

DJANGO_SSL = os.environ.get("DJANGO_HTTP", "False") != "True"
if DJANGO_SSL == True:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 60  # FIXME Update more long seconds later. 365 * 24 * 60 * 60
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

INTERNAL_IPS = os.environ.get("DJANGO_INTERNAL_IPS", "").split(",")

if DEBUG == False and PRODUCT:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": "INFO", "handlers": ["file"]},
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "/var/log/gunicorn/django-green.log",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }

KAKAO_CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID", "")
KAKAO_CLIENT_SECRET = os.environ.get("KAKAO_CLIENT_SECRET", "")
NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
SOCIALACCOUNT_PROVIDERS = {
    "naver": {"APP": {"client_id": NAVER_CLIENT_ID, "secret": NAVER_CLIENT_SECRET, "key": ""}},
    "kakao": {"APP": {"client_id": KAKAO_CLIENT_ID, "secret": "", "key": ""}},
    "google": {
        "APP": {
            "client_id": GOOGLE_CLIENT_ID,
            "secret": GOOGLE_CLIENT_SECRET,
            "key": "",
        }
    },
}

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
