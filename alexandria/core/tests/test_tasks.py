from alexandria.core import tasks


def test_set_content_vector(db, settings, file_factory):
    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = False
    file = file_factory()
    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = True

    tasks.set_content_vector(file.pk)

    file.refresh_from_db()

    assert file.content_vector is not None


def test_set_checksum(db, settings, file_factory):
    settings.ALEXANDRIA_ENABLE_CHECKSUM = False
    file = file_factory()
    settings.ALEXANDRIA_ENABLE_CHECKSUM = True

    tasks.set_checksum(file.pk)

    file.refresh_from_db()

    assert file.checksum is not None
