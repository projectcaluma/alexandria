"""
This settings module only contains alexandria specific settings.

It's imported by the main alexandria settings and is intended to also be used by third party
applications integrating alexandria.
"""

import os
from warnings import warn

import environ

env = environ.Env()
django_root = environ.Path(__file__) - 3

ENV_FILE = env.str("ENV_FILE", default=django_root(".env"))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str("ENV", "production")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


ADMIN_USERNAME = env.str("ADMIN_USERNAME", default="admin")

# Authentication
OIDC_OP_USER_ENDPOINT = env.str("OIDC_OP_USER_ENDPOINT", default=None)
OIDC_OP_TOKEN_ENDPOINT = "not supported in alexandria, but a value is needed"
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_USERNAME_CLAIM = env.str("OIDC_USERNAME_CLAIM", default="sub")
OIDC_GROUPS_CLAIM = env.str("OIDC_GROUPS_CLAIM", default="alexandria_groups")
OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=0
)
OIDC_OP_INTROSPECT_ENDPOINT = env.str("OIDC_OP_INTROSPECT_ENDPOINT", default=None)
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID", default=None)
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET", default=None)

DEV_AUTH_BACKEND = env.bool("DEV_AUTH_BACKEND", default=False)
OIDC_DRF_AUTH_BACKEND = env.str(
    "OIDC_DRF_AUTH_BACKEND",
    default="alexandria.oidc_auth.authentication.AlexandriaAuthenticationBackend",
)
if DEV_AUTH_BACKEND:
    OIDC_DRF_AUTH_BACKEND = (
        "alexandria.oidc_auth.authentication.DevelopmentAuthenticationBackend"
    )
ALEXANDRIA_OIDC_USER_FACTORY = env.str(
    "ALEXANDRIA_OIDC_USER_FACTORY", default="alexandria.oidc_auth.models.OIDCUser"
)
ALEXANDRIA_CREATED_BY_USER_PROPERTY = env.str(
    "ALEXANDRIA_CREATED_BY_USER_PROPERTY", default="username"
)
ALEXANDRIA_CREATED_BY_GROUP_PROPERTY = env.str(
    "ALEXANDRIA_CREATED_BY_GROUP_PROPERTY", default="group"
)


# Extensions
ALEXANDRIA_VISIBILITY_CLASSES = env.list(
    "ALEXANDRIA_VISIBILITY_CLASSES",
    default=default(["alexandria.core.visibilities.Any"], []),
)
ALEXANDRIA_PERMISSION_CLASSES = env.list(
    "ALEXANDRIA_PERMISSION_CLASSES",
    default=default(["alexandria.core.permissions.AllowAny"], []),
)
ALEXANDRIA_VALIDATION_CLASSES = env.list("ALEXANDRIA_VALIDATION_CLASSES", default=[])


VISIBILITY_CLASSES = env.list(
    "VISIBILITY_CLASSES", default=default(["alexandria.core.visibilities.Any"], [])
)
PERMISSION_CLASSES = env.list(
    "PERMISSION_CLASSES", default=default(["alexandria.core.permissions.AllowAny"], [])
)
VALIDATION_CLASSES = env.list("VALIDATION_CLASSES", default=[])


# Reading PERMISSION_CLASSES, VISIBILITY_CLASSES, VALIDATION_CLASSES is still supported.
# If it's set but ALEXANDRIA_* is not, copy over the config
if PERMISSION_CLASSES and not ALEXANDRIA_PERMISSION_CLASSES:  # pragma: no cover
    ALEXANDRIA_PERMISSION_CLASSES = PERMISSION_CLASSES
if VISIBILITY_CLASSES and not ALEXANDRIA_VISIBILITY_CLASSES:  # pragma: no cover
    ALEXANDRIA_VISIBILITY_CLASSES = VISIBILITY_CLASSES
if VALIDATION_CLASSES and not ALEXANDRIA_VALIDATION_CLASSES:  # pragma: no cover
    ALEXANDRIA_VALIDATION_CLASSES = VALIDATION_CLASSES


# non prefixed are deprecated, but still supported for now.
# If they're set, notify the user.
def _deprecate_env(name, replacement):
    if env.str(name, default=False):  # pragma: no cover
        warn(
            DeprecationWarning(
                f"The {name} setting is deprecated and will be removed "
                f"in a future version of alexandria. Use {replacement}"
            )
        )


_deprecate_env("PERMISSION_CLASSES", "ALEXANDRIA_PERMISSION_CLASSES")
_deprecate_env("VISIBILITY_CLASSES", "ALEXANDRIA_VISIBILITY_CLASSES")
_deprecate_env("VALIDATION_CLASSES", "ALEXANDRIA_VALIDATION_CLASSES")

# Storage
MEDIA_STORAGE_SERVICE = env.str("MEDIA_STORAGE_SERVICE", default="minio")
MINIO_STORAGE_ENDPOINT = env.str("MINIO_STORAGE_ENDPOINT", default="minio:9000")
MINIO_STORAGE_ACCESS_KEY = env.str("MINIO_STORAGE_ACCESS_KEY", default="minio")
MINIO_STORAGE_SECRET_KEY = env.str("MINIO_STORAGE_SECRET_KEY", default="minio123")
MINIO_STORAGE_USE_HTTPS = env.str("MINIO_STORAGE_USE_HTTPS", default=False)
MINIO_STORAGE_MEDIA_BUCKET_NAME = env.str(
    "MINIO_STORAGE_MEDIA_BUCKET_NAME", default="alexandria-media"
)
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = env.str(
    "MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET", default=True
)
MINIO_PRESIGNED_TTL_MINUTES = env.str("MINIO_PRESIGNED_TTL_MINUTES", default=15)


# Thumbnails
ENABLE_THUMBNAIL_GENERATION = env.bool("ENABLE_THUMBNAIL_GENERATION", default=True)
THUMBNAIL_WIDTH = env.int("THUMBNAIL_WIDTH", default=None)
THUMBNAIL_HEIGHT = env.int("THUMBNAIL_HEIGHT", default=None)
