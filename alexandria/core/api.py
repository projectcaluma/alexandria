import logging
from os.path import splitext

from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.utils.translation import gettext as _

from alexandria.core import models
from alexandria.core.validations import validate_file

log = logging.getLogger(__name__)


@transaction.atomic()
def copy_document(
    document: models.Document, user: str, group: str, category: models.Category
):
    """
    Copy a document and all its original files to a new document.

    This function eases the copying of documents by automatically setting important fields.
    Uses `create_file` to copy the original document files.
    """

    basename, ext = splitext(document.title)
    copy_suffix = _("(copy)")
    document_title = f"{basename} {copy_suffix}{ext}"
    new_document = models.Document.objects.create(
        title=document_title,
        description=document.description,
        metainfo=document.metainfo,
        category=category,
        created_by_user=user,
        created_by_group=group,
        modified_by_user=user,
        modified_by_group=group,
    )

    # Copying only the originals - create_file() will create the thumbnails
    document_files = models.File.objects.filter(
        document=document, variant=models.File.Variant.ORIGINAL.value
    ).order_by("created_at")
    for document_file in document_files:
        new_file = create_file(
            name=document_file.name,
            document=new_document,
            content=document_file.content,
            mime_type=document_file.mime_type,
            size=document_file.size,
            user=document_file.created_by_user,
            group=document_file.created_by_group,
            metainfo=document_file.metainfo,
        )
        new_file.content.copy(f"{new_file.pk}_{new_file.name}")

    return new_document


@transaction.atomic()
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
    **additional_attributes,
):
    """
    Create a file with defaults and generate a thumbnail.

    Use this instead of the normal File.objects.create to ensure that all important fields are set.
    As well as generating a thumbnail for the file.
    """
    file = models.File(
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
    validate_file(file)
    file.save()

    return file
