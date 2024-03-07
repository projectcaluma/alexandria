from django.conf import settings
from manabi import ManabiAuthenticator, ManabiDAVApp
from manabi.lock import ManabiDbLockStorage
from manabi.log import HeaderLogger
from wsgidav.dir_browser import WsgiDavDirBrowser
from wsgidav.error_printer import ErrorPrinter
from wsgidav.mw.debug_filter import WsgiDavDebugFilter
from wsgidav.request_resolver import RequestResolver

from .dav_provider import AlexandriaProvider


def get_dav():
    postgres_dsn = (
        f"dbname={settings.DATABASES['default']['NAME']} "
        f"host={settings.DATABASES['default']['HOST']} "
        f"port={settings.DATABASES['default']['PORT']} "
        f"user={settings.DATABASES['default']['USER']} "
        f"password={settings.DATABASES['default']['PASSWORD']} "
        f"sslmode={settings.DATABASES['default']['OPTIONS'].get('sslmode', 'prefer')}"
    )
    ttl = 600
    root_folder = settings.MEDIA_ROOT
    if settings.ALEXANDRIA_FILE_STORAGE == "alexandria.storages.backends.s3.S3Storage":
        root_folder = "/"

    config = {
        "lock_storage": ManabiDbLockStorage(ttl, postgres_dsn),
        "provider_mapping": {
            settings.ALEXANDRIA_MANABI_DAV_URL_PATH: AlexandriaProvider(
                root_folder, cb_hook_config=None
            ),
        },
        "middleware_stack": [
            HeaderLogger,
            WsgiDavDebugFilter,
            ErrorPrinter,
            ManabiAuthenticator,
            WsgiDavDirBrowser,
            RequestResolver,
        ],
        "manabi": {
            "key": settings.MANABI_SHARED_KEY,
            "refresh": ttl,
            "initial": ttl,
            "secure": settings.MANABI_SECURE,
        },
    }
    return ManabiDAVApp(config)
