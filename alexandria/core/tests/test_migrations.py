import uuid

import pytest


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:  # pragma: no cover
        return False


@pytest.mark.django_db()
def test_tag_pk_migration(migrator):
    """Ensures that the initial migration works."""
    old_state = migrator.apply_initial_migration(("alexandria_core", "0010_mark"))

    Tag = old_state.apps.get_model("alexandria_core", "Tag")
    Document = old_state.apps.get_model("alexandria_core", "Document")
    Synonym = old_state.apps.get_model("alexandria_core", "TagSynonymGroup")

    synonym = Synonym.objects.create()

    tag1 = Tag.objects.create(slug="apple", name="Apple", tag_synonym_group=synonym)
    tag2 = Tag.objects.create(slug="banana", name="Banana", tag_synonym_group=synonym)
    tag3 = Tag.objects.create(slug="melon", name="Melon")
    old_ids = {tag1.pk, tag2.pk, tag3.pk}

    doc1 = Document.objects.create(title="Sand")
    doc2 = Document.objects.create(title="Dirt")

    doc1.tags.add(tag1, tag3)
    doc2.tags.add(tag2)

    assert Tag.objects.count() == 3

    new_state = migrator.apply_tested_migration(
        ("alexandria_core", "0012_tag_uuid_schema")
    )

    # After the initial migration is done, we can use the model state:
    Tag = new_state.apps.get_model("alexandria_core", "Tag")
    Document = new_state.apps.get_model("alexandria_core", "Document")
    tags = Tag.objects.all()
    doc1 = Document.objects.get(title="Sand")
    doc2 = Document.objects.get(title="Dirt")

    assert tags.count() == 3
    assert set(tags.values_list("pk", flat=True)).intersection(old_ids) == set()

    assert tags.get(name="Apple").tag_synonym_group.pk == synonym.pk
    assert tags.get(name="Banana").tag_synonym_group.pk == synonym.pk
    assert tags.get(name="Melon").tag_synonym_group is None

    assert doc1.tags.count() == 2
    assert doc2.tags.count() == 1

    assert doc1.tags.filter(name="Apple").exists()
    assert doc1.tags.filter(name="Melon").exists()
    assert doc2.tags.filter(name="Banana").exists()

    for tag in tags:
        assert is_valid_uuid(tag.id)


@pytest.mark.django_db()
def test_0013_file_content(migrator):
    old_state = migrator.apply_initial_migration(
        ("alexandria_core", "0012_tag_uuid_schema")
    )

    OldFile = old_state.apps.get_model("alexandria_core", "file")
    OldDocument = old_state.apps.get_model("alexandria_core", "document")
    doc = OldDocument.objects.create()
    OldFile.objects.create(name="existing_file", document=doc)

    new_state = migrator.apply_tested_migration(
        ("alexandria_core", "0013_file_content")
    )

    NewFile = new_state.apps.get_model("alexandria_core", "file")
    _file = NewFile.objects.first()
    assert _file.name in _file.content.url
