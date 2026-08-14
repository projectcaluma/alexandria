import mimetypes

from django.apps import AppConfig
from django.conf import settings


def register_custom_mime_types():
    """Register mime types that are not known by the `mimetypes` module.

    They are registered as non-standard types, therefore they are only
    detectable by non-strict lookups, e.g. `mimetypes.guess_type(name, strict=False)`.
    """
    # `init()` rebuilds the registry, therefore it must run before any type is
    # added, otherwise the custom types would be discarded again.
    mimetypes.init()

    for mime_type, extensions in settings.ALEXANDRIA_CUSTOM_MIME_TYPES.items():
        for extension in extensions:
            # `add_type()` expects the extension with a leading dot
            mimetypes.add_type(mime_type, f".{extension}", strict=False)


class DefaultConfig(AppConfig):
    name = "alexandria.core"
    label = "alexandria_core"

    def ready(self):
        register_custom_mime_types()
