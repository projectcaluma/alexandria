"""
This settings module only contains alexandria specific settings.

It's imported by the main alexandria settings and is intended to also be used by third party
applications integrating alexandria.
"""

import os

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

ALEXANDRIA_DEV_AUTH_BACKEND = env.bool("ALEXANDRIA_DEV_AUTH_BACKEND", default=False)
OIDC_DRF_AUTH_BACKEND = env.str(
    "OIDC_DRF_AUTH_BACKEND",
    default="alexandria.oidc_auth.authentication.AlexandriaAuthenticationBackend",
)
if ALEXANDRIA_DEV_AUTH_BACKEND:
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

# Storage
ALEXANDRIA_MEDIA_STORAGE_SERVICE = env.str(
    "ALEXANDRIA_MEDIA_STORAGE_SERVICE", default="minio"
)
ALEXANDRIA_MINIO_STORAGE_ENDPOINT = env.str(
    "ALEXANDRIA_MINIO_STORAGE_ENDPOINT", default="minio:9000"
)
ALEXANDRIA_MINIO_STORAGE_ACCESS_KEY = env.str(
    "ALEXANDRIA_MINIO_STORAGE_ACCESS_KEY", default="minio"
)
ALEXANDRIA_MINIO_STORAGE_SECRET_KEY = env.str(
    "ALEXANDRIA_MINIO_STORAGE_SECRET_KEY", default="minio123"
)
ALEXANDRIA_MINIO_STORAGE_USE_HTTPS = env.bool(
    "ALEXANDRIA_MINIO_STORAGE_USE_HTTPS", default=False
)
ALEXANDRIA_MINIO_STORAGE_MEDIA_BUCKET_NAME = env.str(
    "ALEXANDRIA_MINIO_STORAGE_MEDIA_BUCKET_NAME", default="alexandria-media"
)
ALEXANDRIA_MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = env.bool(
    "ALEXANDRIA_MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET", default=True
)
ALEXANDRIA_MINIO_PRESIGNED_TTL_MINUTES = env.str(
    "ALEXANDRIA_MINIO_PRESIGNED_TTL_MINUTES", default=15
)


# Thumbnails
ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = env.bool(
    "ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION", default=True
)
ALEXANDRIA_THUMBNAIL_WIDTH = env.int("ALEXANDRIA_THUMBNAIL_WIDTH", default=None)
ALEXANDRIA_THUMBNAIL_HEIGHT = env.int("ALEXANDRIA_THUMBNAIL_HEIGHT", default=None)

# Checksums
ALEXANDRIA_ENABLE_CHECKSUM = env.bool("ALEXANDRIA_ENABLE_CHECKSUM", default=True)
