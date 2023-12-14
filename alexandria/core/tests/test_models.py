import pytest

from alexandria.core.models import File


@pytest.mark.parametrize("admin_groups", [["foo"]])
def test_clone_document(admin_client, file_factory):
    v1_thumb = file_factory(variant=File.Variant.THUMBNAIL)
    v2_thumb = file_factory(variant=File.Variant.THUMBNAIL, document=v1_thumb.document)
    clone = v1_thumb.document.clone()

    # in the test, the thumbnail for the cloned file is not created
    # because the minio hook is not called
    assert File.objects.count() == 5
    assert list(clone.files.values_list("name", flat=True)) == [
        v2_thumb.document.files.filter(variant=File.Variant.ORIGINAL).first().name,
    ]
