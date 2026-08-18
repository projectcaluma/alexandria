import mimetypes

from django.apps import AppConfig
from django.conf import settings


def register_custom_mime_types():
    """Register mime types that are not known by the `mimetypes` module.

    This makes them detectable by `mimetypes.guess_type()`.
    """
    # `init()` rebuilds the registry, therefore it must run before any type is
    # added, otherwise the custom types would be discarded again.
    mimetypes.init()

    for mime_type, extensions in settings.ALEXANDRIA_CUSTOM_MIME_TYPES.items():
        for extension in extensions:
            mimetypes.add_type(mime_type, extension)


class DefaultConfig(AppConfig):
    name = "alexandria.core"
    label = "alexandria_core"

    def ready(self):
        register_custom_mime_types()
