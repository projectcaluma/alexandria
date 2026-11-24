from generic_permissions.config import ObjectPermissionsConfig

from alexandria.core.models import Document

# Actions checked as object permission on the document. Hosts map them in
# their permission classes like any other document action (e.g. ebau's
# `{category}:sign`), which also restricts in which categories it's allowed.
SIGN = "sign"
STAMP = "stamp"


def has_document_permission(request, document: Document, action: str) -> bool:
    """Return whether the configured permission classes allow `action`."""
    return all(
        handler(request, document, action=action)
        for handler in ObjectPermissionsConfig.get_handlers(Document)
    )
