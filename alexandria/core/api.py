import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File

from alexandria.core import models

log = logging.getLogger(__name__)


def create_document_file(
    user: str,
    group: str,
    category: models.Category,
    document_title: str,
    file_name: str,
    file_content: File,
    mime_type: str,
    file_size: int,
    additional_document_attributes={},
    additional_file_attributes={},
):
    """
    Create a document and file with the given attributes.

    This function eases the creation of documents and files by automatically setting important fields.
    Uses `create_file` to create the file.
    """
    document = models.Document.objects.create(
        title=document_title,
        category=category,
        created_by_user=user,
        created_by_group=group,
        modified_by_user=user,
        modified_by_group=group,
        **additional_document_attributes,
    )
    file = create_file(
        document=document,
        user=user,
        group=group,
        name=file_name,
        content=file_content,
        mime_type=mime_type,
        size=file_size,
        **additional_file_attributes,
    )

    return document, file


def create_file(
    document: models.Document,
    user: str,
    group: str,
    name: str,
    content: File,
    mime_type: str,
    size: int,
    **additional_attributes
):
    """
    Create a file with defaults and generate a thumbnail.

    Use this instead of the normal File.objects.create to ensure that all important fields are set.
    As well as generating a thumbnail for the file.
    """
    file = models.File.objects.create(
        name=name,
        content=content,
        mime_type=mime_type,
        size=size,
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
        **additional_attributes,
    )

    try:
        file.create_thumbnail()
    except ValidationError as e:  # pragma: no cover
        log.error(
            "Object {obj} created successfully. Thumbnail creation failed. Error: {error}".format(
                obj=file, error=e.messages
            )
        )

    return file
