import pytest

from alexandria.core.factories import DocumentFactory, FileFactory
from alexandria.core.models import File


@pytest.mark.parametrize("admin_groups", [["foo"]])
def test_clone_document(admin_client, minio_mock):
    document = DocumentFactory()

    v1 = FileFactory(document=document, variant="original", name="v1")
    FileFactory(document=document, variant="thumbnail", original=v1)
    v2 = FileFactory(document=document, variant="original", name="v2")
    FileFactory(
        document=document,
        variant="thumbnail",
        original=v2,
        name="thumbnail_file",
    )

    clone = document.clone()

    # in the test, the thumbnail for the cloned file is not created
    # because the minio hook is not called
    assert File.objects.count() == 5
    assert list(clone.files.values_list("name", flat=True)) == [
        v2.name,
    ]
