import re

from django.conf import global_settings

from .alexandria import *  # noqa
from .alexandria import default, env, environ

SECRET_KEY = env.str("SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))


# Application definition

INSTALLED_APPS = [
    "django.contrib.postgres",
    "localized_fields",
    "psqlextra",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "alexandria.core.apps.DefaultConfig",
    "generic_permissions.apps.GenericPermissionsConfig",
    "manabi_migrations",
]

if ENV == "dev":  # noqa
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "alexandria.urls"
WSGI_APPLICATION = "alexandria.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env.str("DATABASE_NAME", default="alexandria"),
        "USER": env.str("DATABASE_USER", default="alexandria"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=default("alexandria")),
        "HOST": env.str("DATABASE_HOST", default="localhost"),
        "PORT": env.str("DATABASE_PORT", default=""),
        "OPTIONS": env.dict("DATABASE_OPTIONS", default={}),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


def parse_languages(languages):
    return [(language, language) for language in languages]


LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en")
LANGUAGES = (
    parse_languages(env.list("LANGUAGES", default=["en"])) or global_settings.LANGUAGES
)

TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

LOCALIZED_FIELDS_EXPERIMENTAL = True

# Don't clutter workdir with uploaded stuff when developing
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default="/media/uploads")


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "ORDERING_PARAM": "sort",
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.MultiPartRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True

# Anonymous writing
ALEXANDRIA_ALLOW_ANONYMOUS_WRITE = env.bool(
    "ALEXANDRIA_ALLOW_ANONYMOUS_WRITE", default=False
)

if ALEXANDRIA_ALLOW_ANONYMOUS_WRITE:
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        "rest_framework.permissions.AllowAny",
    ]


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search(r"(.+) \<(.+@.+)\>", admin)
        if not match:  # pragma: no cover
            raise environ.ImproperlyConfigured(
                'In ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("ADMINS", default=[]))

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Runserver plus
RUNSERVERPLUS_POLLER_RELOADER_TYPE = (
    "stat"  # change back to auto after https://github.com/pallets/werkzeug/issues/2945
)

# Celery config
REDIS_HOST = env.str("REDIS_HOST", default="redis")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_USER = env.str("REDIS_USER", default="default")
REDIS_PASSWORD = env.str("REDIS_PASSWORD", default="redis")
CELERY_BROKER_URL = env.str(
    "CELERY_BROKER_URL",
    default=f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
)
CELERY_TASK_ACKS_LATE = env.bool(
    "CELERY_TASK_ACKS_LATE",
    default=True,
)
CELERY_TASK_SOFT_TIME_LIMIT = env.int("CELERY_TASK_SOFT_TIME_LIMIT", default=60)
