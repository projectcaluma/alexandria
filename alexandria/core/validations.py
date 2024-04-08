from mimetypes import guess_type

from django.utils.translation import gettext_lazy as _
from django_clamd.validators import validate_file_infection
from generic_permissions.validation import validator_for
from rest_framework.exceptions import ValidationError

from alexandria.core.models import File


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

        validate_mime_type(mime_type, data["document"].category)
        data["mime_type"] = mime_type

        return data
