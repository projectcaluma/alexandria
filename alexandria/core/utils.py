from django.conf import settings
from django.core.exceptions import ValidationError

from alexandria.core import models


def create_document_file(user, group, document_attributes, file_attributes):
    document = models.Document.objects.create(
        created_by_user=user,
        created_by_group=group,
        modified_by_user=user,
        modified_by_group=group,
        **document_attributes,
    )
    file = create_file(document, user, group, file_attributes)

    return document, file


def create_file(document, user, group, attributes):
    file = models.File.objects.create(
        document=document,
        encryption_status=(
            settings.ALEXANDRIA_ENCRYPTION_METHOD
            if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION
            else None
        ),
        created_by_user=user,
        created_by_group=group,
        modified_by_user=user,
        modified_by_group=group,
        **attributes,
    )

    try:
        file.create_thumbnail()
    except ValidationError:  # pragma: no cover
        # thumbnail could not be generated because of an unsupported mime type
        pass

    return file
