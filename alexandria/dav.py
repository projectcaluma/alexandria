from functools import partial
from typing import Any, Callable, Dict, List, Tuple

from django.conf import settings
from django.db import connections
from manabi import ManabiAuthenticator, ManabiDAVApp
from manabi.lock import ManabiDbLockStorage
from manabi.log import HeaderLogger
from wsgidav.dir_browser import WsgiDavDirBrowser
from wsgidav.error_printer import ErrorPrinter
from wsgidav.mw.base_mw import BaseMiddleware
from wsgidav.mw.debug_filter import WsgiDavDebugFilter
from wsgidav.request_resolver import RequestResolver

from .dav_provider import AlexandriaProvider


class ManageDjangoConnectionsMiddleware(BaseMiddleware):
    """
    Middleware for managing Django DB connections.

    Disconnect DB connections that are not used anymore, or that have expired
    or are broken. This is doing the same thing that Django would do at the
    end of each request.

    Note: This middleware should be the first in the stack, as any middleware
    that are above it will not be able to use Django DB / models anymore after
    the request is processed
    """

    def __call__(
        self, environ: Dict[str, Any], start_response: Callable
    ) -> List[bytes]:
        self.cleanup_db_connections()
        return self.next_app(environ, partial(self.process, environ, start_response))

    def process(
        self,
        environ: Dict[str, Any],
        start_response: Callable,
        status: int,
        headers: List[Tuple[str, str]],
        exc_info=None,
    ):
        res = start_response(status, headers, exc_info)
        self.cleanup_db_connections()
        return res

    def cleanup_db_connections(self):
        # This is a bit ugly, but: Our unit tests run in a transaction, and
        # therefore we can't *really* close the obsolete connections, as it
        # would break the tests. Other than that, this is an exact copy of
        # `django.db.close_old_connections()`.
        for conn in connections.all(initialized_only=True):
            if not conn.in_atomic_block:  # pragma: no cover
                conn.close_if_unusable_or_obsolete()


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
            ManageDjangoConnectionsMiddleware,
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
        "suppress_version_info": True,
    }
    return ManabiDAVApp(config)
