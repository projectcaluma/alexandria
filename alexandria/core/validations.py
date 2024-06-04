import logging
from mimetypes import guess_type

import magic
from clamdpy import ClamdNetworkSocket
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from generic_permissions.validation import validator_for
from rest_framework.exceptions import ValidationError

from alexandria.core.models import File

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
        raise ValidationError(_("File is infected with malware."), code="infected")
    elif result.status == "ERROR":
        raise ValidationError(
            (_("Malware scan had an error: ") + result.reason),
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
            _(
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
        mime_type = data["content"].content_type
        if mime_type == "application/octet-stream" or not mime_type:
            guess, encoding = guess_type(data["name"])
            if guess is not None:
                mime_type = guess
            else:
                data["content"].seek(0)
                mime_type = magic.from_buffer(data["content"].read(), mime=True)
                data["content"].seek(0)

        validate_mime_type(mime_type, data["document"].category)
        data["mime_type"] = mime_type

        return data
