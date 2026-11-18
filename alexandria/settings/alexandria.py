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
ALEXANDRIA_GET_USER_AND_GROUP_FUNCTION = env.str(
    "ALEXANDRIA_GET_USER_AND_GROUP_FUNCTION",
    default="alexandria.oidc_auth.authentication.get_user_and_group",
)


# Extensions
ALEXANDRIA_VISIBILITY_CLASSES = env.list(
    "ALEXANDRIA_VISIBILITY_CLASSES",
    default=default(["generic_permissions.visibilities.Any"], []),
)
ALEXANDRIA_PERMISSION_CLASSES = env.list(
    "ALEXANDRIA_PERMISSION_CLASSES",
    default=default(["generic_permissions.permissions.AllowAny"], []),
)
ALEXANDRIA_VALIDATION_CLASSES = env.list(
    "ALEXANDRIA_VALIDATION_CLASSES",
    default=["alexandria.core.validations.AlexandriaValidator"],
)

# We use DGAP as a permission/visibility/validation handler. Copy
# the configuration over so DGAP knows
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = ALEXANDRIA_VISIBILITY_CLASSES
GENERIC_PERMISSIONS_PERMISSION_CLASSES = ALEXANDRIA_PERMISSION_CLASSES
GENERIC_PERMISSIONS_VALIDATION_CLASSES = ALEXANDRIA_VALIDATION_CLASSES

# Storage
#
# The default storage is the file system. This is mostly for development and
# testing environments.
ALEXANDRIA_FILE_STORAGE = env.str(
    "ALEXANDRIA_FILE_STORAGE", default="alexandria.storages.backends.s3.S3Storage"
)
ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = env.bool(
    "ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION", default=False
)
ALEXANDRIA_ENCRYPTION_METHOD = env.str(
    "ALEXANDRIA_ENCRYPTION_METHOD", default="ssec-global"
)
# Number of seconds a signed download url expires
ALEXANDRIA_DOWNLOAD_URL_LIFETIME = env.int(
    "ALEXANDRIA_DOWNLOAD_URL_LIFETIME", default=300
)
PRESIGNED_URL_LIFETIME = ALEXANDRIA_DOWNLOAD_URL_LIFETIME

# S3 / boto3 storage client specific configurations
# -------------------------------------------------
#
# Boto3 is the AWS SDK for Python including Simple Storage Service (S3) or more
# generically simple object storate (SOS)
#
# Documentation and available VARIABLES for configuration:
# django-storages: https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
# boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html#boto3-documentation
#
# S3 compatible services like Amazon S3, Garage, Minio or Exoscale
#
# In order to make use an S3 storage backend set `ALEXANDRIA_FILE_STORAGE` to one of
#  - storages.backends.s3.S3Storage
#  - storages.backends.s3boto3.S3Boto3Storage
# For your convenience alexandria provides:
#  - alexandria.storages.backends.s3.S3Storage
#
# At rest encryption
# ------------------
# S3 supports serverside encryption (SSE) methods. They differ by who owns the  keys
# and the algorhythms used.
#
# SSE-C
# -----
# serverside encryption with customer managed key
#
# Every object is encrypted with a SHA256 32bit key.
#
# `ssec-global`: every object is encrypted with the same key
# `seec-object`: every object is encryption with a key derived from a shared secret and
#                a unique object specific property.
#
# Identity to access the storage service
ALEXANDRIA_S3_ACCESS_KEY = env.str("ALEXANDRIA_S3_ACCESS_KEY", default="minio")
# SECRET to authenticate with the storage service
ALEXANDRIA_S3_SECRET_KEY = env.str("ALEXANDRIA_S3_SECRET_KEY", default="minio123")
ALEXANDRIA_S3_ENDPOINT_URL = env.str(
    "ALEXANDRIA_S3_ENDPOINT_URL", default="http://minio:9000"
)
# SSL is turned off for the dev environment. Don't do that in production
ALEXANDRIA_S3_USE_SSL = env.bool("ALEXANDRIA_S3_USE_SSL", default=False)
# SSL certificate verification is turned off for the dev environment. Don't do that in production
ALEXANDRIA_S3_VERIFY = env.bool("ALEXANDRIA_S3_VERIFY", default=False)
ALEXANDRIA_S3_BUCKET_NAME = env.str(
    "ALEXANDRIA_S3_BUCKET_NAME", default="alexandria-media"
)
ALEXANDRIA_S3_REGION_NAME = env.str("ALEXANDRIA_S3_REGION_NAME", default=None)
# Object parameter translate to specific headers and values in put and get requests
ALEXANDRIA_S3_OBJECT_PARAMETERS = {}
# Shared secret for at-rest encryption of objects
# NOTE: required to be 32 bytes long
ALEXANDRIA_S3_STORAGE_SSEC_SECRET = env.str(
    "ALEXANDRIA_S3_STORAGE_SSEC_SECRET", default="".join(["x" for _ in range(32)])
)

# Thumbnails
ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = env.bool(
    "ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION", default=True
)
ALEXANDRIA_THUMBNAIL_WIDTH = env.int("ALEXANDRIA_THUMBNAIL_WIDTH", default=None)
ALEXANDRIA_THUMBNAIL_HEIGHT = env.int("ALEXANDRIA_THUMBNAIL_HEIGHT", default=600)

# Checksums
ALEXANDRIA_ENABLE_CHECKSUM = env.bool("ALEXANDRIA_ENABLE_CHECKSUM", default=True)

# Minimum accepted PDF version
ALEXANDRIA_MIN_PDF_VERSION = env.float("ALEXANDRIA_MIN_PDF_VERSION", default=None)

# Additional mime types that are not known by the `mimetypes` module. They map a
# mime type to its file extensions, e.g.
# `text/plain=ili,itf;application/vnd.ms-outlook=msg`, and are registered as
# non-standard types on app startup.
ALEXANDRIA_CUSTOM_MIME_TYPES = env.dict(
    "ALEXANDRIA_CUSTOM_MIME_TYPES",
    cast={"value": [str]},
    default={
        "application/vnd.ms-outlook": ["msg"],
    },
)

# Clamav service
ALEXANDRIA_CLAMD_TCP_SOCKET = env.str("ALEXANDRIA_CLAMD_TCP_SOCKET", default=3310)
ALEXANDRIA_CLAMD_TCP_ADDR = env.str("ALEXANDRIA_CLAMD_TCP_ADDR", default="localhost")
ALEXANDRIA_CLAMD_ENABLED = env.bool("ALEXANDRIA_CLAMD_ENABLED", default=False)

# Document merge service
ALEXANDRIA_ENABLE_PDF_CONVERSION = env.bool(
    "ALEXANDRIA_ENABLE_PDF_CONVERSION", default=False
)
ALEXANDRIA_DMS_URL = env.str("ALEXANDRIA_DMS_URL", default="http://dms:8000/api/v1")

# Manabi
ALEXANDRIA_USE_MANABI = env.bool("ALEXANDRIA_USE_MANABI", default=False)
ALEXANDRIA_MANABI_DAV_URL_PATH = env.str(
    "ALEXANDRIA_MANABI_DAV_URL_PATH", default="/dav"
)
ALEXANDRIA_MANABI_ALLOWED_MIMETYPES = env.list(
    "ALEXANDRIA_MANABI_ALLOWED_MIMETYPES",
    default=[
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
)
ALEXANDRIA_MANABI_DAV_URI_SCHEMES = env.dict(
    "ALEXANDRIA_MANABI_DAV_URI_SCHEMES",
    default={
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "ms-word:ofe|u|",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "ms-excel:ofe|u|",
    },
)
ALEXANDRIA_MANABI_VERSION_CREATION_THRESHOLD_ENABLED = env.bool(
    "ALEXANDRIA_MANABI_VERSION_CREATION_THRESHOLD_ENABLED",
    default=False,
)
ALEXANDRIA_MANABI_VERSION_CREATION_THRESHOLD_SECONDS = env.int(
    "ALEXANDRIA_MANABI_VERSION_CREATION_THRESHOLD_SECONDS",
    default=60 * 30,
)
MANABI_SHARED_KEY = env.str(
    "MANABI_SHARED_KEY", default=default("2QhWg20fXq0xlnJUkFTDgFoA3JWqvb86OejD9mAVFCW")
)
MANABI_SECURE = ENV == "production"
MANABI_DEBUG = env.bool("MANABI_DEBUG", default=False)

# Use a relatively long refresh timeout because since Word 2509, the server-sent lock timeout is ignored,
# and re-locking is done after ~40mins.
# https://learn.microsoft.com/en-us/answers/questions/5629856/webdav-lock-issues-with-ms-office-v2509-monthly-cu
MANABI_TOKEN_REFRESH_TIMEOUT = env.int("MANABI_TOKEN_REFRESH_TIMEOUT", default=60 * 60)
MANABI_TOKEN_ACTIVATE_TIMEOUT = env.int(
    "MANABI_TOKEN_ACTIVATE_TIMEOUT", default=10 * 60
)


# Content search
ALEXANDRIA_ENABLE_CONTENT_SEARCH = env.bool(
    "ALEXANDRIA_ENABLE_CONTENT_SEARCH", default=False
)
ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG = env.dict(
    "ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG",
    default={
        "en": "english",
        "de": "german",
        "fr": "french",
        "it": "italian",
    },
)
ALEXANDRIA_CONTENT_SEARCH_TYPE = env.str(
    "ALEXANDRIA_CONTENT_SEARCH_TYPE", default="phrase"
)

# Mime types that are considered safe for Content-Disposition: inline
SAFE_FOR_INLINE_DISPOSITION = env.list(
    "ALEXANDRIA_SAFE_FOR_INLINE_DISPOSITION",
    default=[
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/gif",
    ],
)

# Tika
TIKA_SERVER_URL = env.str("TIKA_SERVER_URL", default="http://tika:9998")

# Electronic signatures
# Signature provider, signing is disabled without one. Development default:
# local provider with a self-signed certificate
ALEXANDRIA_ESIGN_BACKEND = env.str(
    "ALEXANDRIA_ESIGN_BACKEND",
    default=default("alexandria.esign.backends.local.LocalBackend", None),
)
# DeepSign service account connection, see
# https://admin.deepbox.swiss/third-party-connection/
ALEXANDRIA_DEEPSIGN_CONNECTION_URL = env.str(
    "ALEXANDRIA_DEEPSIGN_CONNECTION_URL",
    default="https://admin.deepbox.swiss/third-party-connection/",
)
ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_ID = env.str(
    "ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_ID", default=None
)
# Public URL of the connection callback endpoint
ALEXANDRIA_DEEPSIGN_CALLBACK_URL = env.str(
    "ALEXANDRIA_DEEPSIGN_CALLBACK_URL", default=None
)
# Where the browser is redirected to after the callback
ALEXANDRIA_DEEPSIGN_CALLBACK_REDIRECT_URL = env.str(
    "ALEXANDRIA_DEEPSIGN_CALLBACK_REDIRECT_URL", default="/"
)
ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_SECRET = env.str(
    "ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_SECRET", default=None
)
# DeepSign API, defaults to the integration environment in development
ALEXANDRIA_DEEPSIGN_TOKEN_URL = env.str(
    "ALEXANDRIA_DEEPSIGN_TOKEN_URL",
    default=default(
        "https://int.deepcloud.swiss/auth/realms/sso/protocol/openid-connect/token",
        None,
    ),
)
ALEXANDRIA_DEEPSIGN_GATEWAY_URL = env.str(
    "ALEXANDRIA_DEEPSIGN_GATEWAY_URL",
    default=default("https://deepgateway.int.deepcloud.swiss/api/v1", None),
)
ALEXANDRIA_DEEPSIGN_SIGN_URL = env.str(
    "ALEXANDRIA_DEEPSIGN_SIGN_URL",
    default=default("https://api.int.sign.deepbox.swiss/api/v1", None),
)
ALEXANDRIA_DEEPSIGN_SIGNATURE_MODE = env.str(
    "ALEXANDRIA_DEEPSIGN_SIGNATURE_MODE", default="qualified"
)
ALEXANDRIA_DEEPSIGN_JURISDICTION = env.str(
    "ALEXANDRIA_DEEPSIGN_JURISDICTION", default="zertes"
)
# DeepSign person reference is `<prefix><username>`
ALEXANDRIA_DEEPSIGN_PERSON_REF_PREFIX = env.str(
    "ALEXANDRIA_DEEPSIGN_PERSON_REF_PREFIX", default="alexandria-"
)
# The DeepID app discards unconfirmed requests after 2 minutes
ALEXANDRIA_DEEPSIGN_TIMEOUT_SECONDS = env.int(
    "ALEXANDRIA_DEEPSIGN_TIMEOUT_SECONDS", default=150
)
ALEXANDRIA_DEEPSIGN_HTTP_TIMEOUT_SECONDS = env.int(
    "ALEXANDRIA_DEEPSIGN_HTTP_TIMEOUT_SECONDS", default=30
)
# Space reserved in the PDF for the CMS signature returned by DeepSign
ALEXANDRIA_DEEPSIGN_SIGNATURE_BYTES_RESERVED = env.int(
    "ALEXANDRIA_DEEPSIGN_SIGNATURE_BYTES_RESERVED", default=59898
)
# Fernet key to encrypt the DeepSign service account passwords, generate
# with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
ALEXANDRIA_ESIGN_ENCRYPTION_KEY = env.str(
    "ALEXANDRIA_ESIGN_ENCRYPTION_KEY",
    default=default("Y6ARqJXoX8dO2RiGFBIWaFLX_UlFzQFCg_fmv1F3_Ww=", None),
)
# Visible stamp: page index and box `x1,y1,x2,y2` in PDF points from the
# bottom left corner (default: top right corner of an A4 page)
ALEXANDRIA_DEEPSIGN_STAMP_PAGE = env.int("ALEXANDRIA_DEEPSIGN_STAMP_PAGE", default=0)
ALEXANDRIA_DEEPSIGN_STAMP_BOX = env.list(
    "ALEXANDRIA_DEEPSIGN_STAMP_BOX", cast=float, default=[415, 722, 565, 812]
)
ALEXANDRIA_DEEPSIGN_STAMP_OPACITY = env.float(
    "ALEXANDRIA_DEEPSIGN_STAMP_OPACITY", default=0.6
)
# Function `(file, user, group) -> {"image": bytes, "text": str}` returning
# the visible stamp, e.g. the stamp image of the municipality
ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION = env.str(
    "ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION",
    default=default("alexandria.esign.dev.example_stamp_data", None),
)
