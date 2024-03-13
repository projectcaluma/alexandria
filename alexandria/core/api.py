from django.conf import settings
from django.core.exceptions import ValidationError

from alexandria.core import models


def create_document_file(user, group, document_attributes, file_attributes):
    """
    Create a document and file with the given attributes.

    This function eases the creation of documents and files by automatically setting important fields.
    Uses ``create_file`` to create the file.

    :param user: The user creating the document and file.
    :param group: The group creating the document and file.
    :param document_attributes: A dictionary containing the fields for the document. (required: category, title)
    :param file_attributes: A dictionary containing the fields for the file. (required: name, content, mime_type, size)
    :return: A tuple containing the created document and file.

    """
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
    """
    Create a file with defaults and generate a thumbnail.

    Use this instead of the normal File.objects.create to ensure that all important fields are set.
    As well as generating a thumbnail for the file.

    :param document: The document associated with the file.
    :param user: The user who created the file.
    :param group: The group who created the file.
    :param attributes: A dictionary containing the fields for the file. (required: name, content, mime_type, size)
    :return: The created file object.
    """
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
