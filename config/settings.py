"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    APP_DEBUG=(bool, False),
    APP_ENVIRON=(bool, False),
    APP_STATIC_URL=(str, "static/"),
    APP_MEDIA_URL=(str, "media/"),
    APPS_DIR=(str, "apps/"),
    EMAIL_USE_TLS=(bool, False),
)
env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("APP_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("APP_DEBUG")

ALLOWED_HOSTS = env("APP_ALLOWED_HOSTS").split(",")

# django-debug-toolbar
INTERNAL_IPS = [
    "0.0.0.0",
    "127.0.0.1",
]

# ------------------------------------------------------------
# DEBUG
# ------------------------------------------------------------
if DEBUG:
    import socket  # only if you haven't already imported this

    from core.utils.globals import SET_GLOBALS

    SET_GLOBALS()

    # django-debug-toolbar docker
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

# ------------------------------------------------------------
# APPS
# ------------------------------------------------------------
# Application definition
DJANGO_APPS_DEFAULT = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

DJANGO_APPS_EXTRA = [
    # 'django.contrib.sites',
    "django.contrib.sitemaps",  #
    "django.contrib.postgres",
]

THIRD_PARTY_APPS: list[str] = [
    # "social_django",
    "django_extensions",
    # "rest_framework",
    # "rest_framework.authtoken",
    # "taggit",
    # "easy_thumbnails",
    "debug_toolbar",
]

FLY_APPS: list[str] = [
    "fly_admin.admin.FlyAdminConfig",
    "fly_admin.apps.FlyAdminConfig",
    "core.apps.CoreConfig",
    "account.apps.AccountConfig",
    "ui.apps.UiConfig",
]

LOCAL_APPS: list[str] = [
    "apps.shop.apps.ShopConfig",
]

INSTALLED_APPS = (
    FLY_APPS + DJANGO_APPS_DEFAULT + DJANGO_APPS_EXTRA + THIRD_PARTY_APPS + LOCAL_APPS
)

APPS_DIR = env("APPS_DIR")

# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------
DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

THIRD_PARTY_MIDDLEWARES = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

LOCAL_MIDDLEWARES = []

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARES + LOCAL_MIDDLEWARES

# ------------------------------------------------------------
# URLS
# ------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# ------------------------------------------------------------
# TEMPLATES, STATIC, MEDIA
# ------------------------------------------------------------
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
                "django.template.context_processors.media",
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = env("APP_STATIC_URL")

STATIC_ROOT = BASE_DIR / "static"

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STATICFILES_DIRS
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     ("images", BASE_DIR / "static_images"),
#     ("css", BASE_DIR / "static_css"),
# ]

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STATICFILES_STORAGE
# Deprecated
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        # https://docs.djangoproject.com/en/4.2/topics/files/#file-storage
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#storages
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        # "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
    # "example": {
    #     "BACKEND": "django.core.files.storage.FileSystemStorage",
    #     "OPTIONS": {
    #         "location": "/example",
    #         "base_url": "/example/",
    #     },
    # },
}

MEDIA_URL = env("APP_MEDIA_URL")

MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------
# WSGI
# ------------------------------------------------------------
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if "test" == env("APP_ENVIRON", False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USERNAME"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        },
        # "default": {
        #     "ENGINE": "django.db.backends.mysql",
        #     "NAME": os.environ.get("DB_DATABASE"),
        #     "USER": os.environ.get("DB_USERNAME"),
        #     "PASSWORD": os.environ.get("DB_PASSWORD"),
        #     "HOST": "db",
        #     "PORT": "3306",
        #     "TEST": {
        #         "MIRROR": "test",
        #     },
        # },
    }

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------
# AUTH
# ------------------------------------------------------------

AUTH_USER_MODEL = "account.User"

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#other-authentication-sources

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "account.authentication.EmailAuthBackend",
]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# https://docs.djangoproject.com/en/4.2/topics/auth/passwords/

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/profile/"

# SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# ------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ------------------------------------------------------------
# Email
# ------------------------------------------------------------
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")

# ------------------------------------------------------------
# Email
# ------------------------------------------------------------
# REST_FRAMEWORK = {
#     "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
#     "DEFAULT_PARSER_CLASSES": ("rest_framework_json_api.parsers.JSONParser",),
#     "DEFAULT_RENDERER_CLASSES": (
#         "rest_framework_json_api.renderers.JSONRenderer",
#         "rest_framework.renderers.BrowsableAPIRenderer",
#     ),
#     "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
#     "DEFAULT_FILTER_BACKENDS": (
#         "rest_framework_json_api.filters.QueryParameterValidationFilter",
#         "rest_framework_json_api.filters.OrderingFilter",
#         "rest_framework_json_apidjango_filters.DjangoFilterBackend",
#         "rest_framework.filters.SearchFilter",
#     ),
#     "SEARCH_PARAM": "filter[search]",
#     "TEST_REQUEST_RENDERER_CLASSES": (
#         "rest_framework_json_api.renderers.JSONRenderer",
#     ),
#     "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
# }

# ------------------------------------------------------------
# DJANGO EXTENSIONS
# ------------------------------------------------------------
SHELL_PLUS = env("SHELL_PLUS")

# ------------------------------------------------------------
# Redis
# ------------------------------------------------------------
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")
REDIS_DB = env("REDIS_DB")

# ------------------------------------------------------------
# Vite
# ------------------------------------------------------------
VITE_PORT = env("VITE_PORT")
VITE_SRC = "/ui/vite_src/"
