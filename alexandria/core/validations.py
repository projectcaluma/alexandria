import logging
from mimetypes import guess_type

import magic
from clamdpy import ClamdNetworkSocket
from django.conf import settings
from django.utils.translation import gettext_lazy
from generic_permissions.validation import validator_for
from rest_framework.exceptions import ValidationError

from alexandria.core.models import Document, File

log = logging.getLogger(__name__)


def validate_file_infection(file_content):
    # inspired by django-clamd
    if file_content is None or not settings.ALEXANDRIA_CLAMD_ENABLED:
        return

    scanner = ClamdNetworkSocket(
        settings.ALEXANDRIA_CLAMD_TCP_ADDR, settings.ALEXANDRIA_CLAMD_TCP_SOCKET
    )

    file_content.seek(0)
    result = scanner.instream(file_content)
    file_content.seek(0)

    if result.status == "FOUND":
        raise ValidationError(
            gettext_lazy("File is infected with malware."), code="infected"
        )
    elif result.status == "ERROR":
        raise ValidationError(
            (gettext_lazy("Malware scan had an error: ") + result.reason),
            code="incomplete",
        )


def validate_file(file):
    validate_file_infection(file.content)
    validate_mime_type(file.mime_type, file.document.category)


def validate_mime_type(mime_type, category):
    if (
        category.allowed_mime_types is not None
        and len(category.allowed_mime_types)
        and mime_type not in category.allowed_mime_types
    ):
        raise ValidationError(
            gettext_lazy(
                "File type %(mime_type)s is not allowed in category %(category)s."
                % {"mime_type": mime_type, "category": category.pk}
            )
        )

    return True


class AlexandriaValidator:
    @validator_for(File)
    def validate_file(self, data, context):
        validate_file_infection(data["content"])

        # Validate that the mime type is allowed in the category
        content_type_header = data["content"].content_type
        extension_type, _ = guess_type(data["name"])

        if not content_type_header:  # pragma: no cover
            raise ValidationError(gettext_lazy("Missing Content-Type header"))
        if not extension_type:
            raise ValidationError(gettext_lazy("Unknown file extension"))

        if content_type_header == "application/octet-stream":
            content_type_header = extension_type
        if content_type_header != extension_type:
            raise ValidationError(
                gettext_lazy(
                    "Content-Type %(content_type)s does not match file extension %(extension)s."
                    % {"content_type": content_type_header, "extension": extension_type}
                )
            )

        data["content"].seek(0)
        file_content_type = magic.from_buffer(data["content"].read(), mime=True)
        data["content"].seek(0)

        if file_content_type != content_type_header:
            raise ValidationError(
                gettext_lazy(
                    "Content-Type %(content_type)s does not match detected file content %(file_content_type)s."
                    % {
                        "content_type": content_type_header,
                        "file_content_type": file_content_type,
                    }
                )
            )

        validate_mime_type(content_type_header, data["document"].category)
        data["mime_type"] = content_type_header

        return data

    @validator_for(Document)
    def validate_document(self, data, context):
        if context["request"].method == "PATCH" and "category" in data:
            category = data["category"]
            document = context["view"].get_object()
            if not document.category.pk == category.pk:
                # Validate if a document is moved to another category that the
                # mime type of the file is still compatible with the category's
                # mime types.
                validate_mime_type(document.get_latest_original().mime_type, category)
        return data
