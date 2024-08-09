import datetime
import uuid

from django.db import migrations


def slug_to_uuid(apps, schema_editor):
    Tag = apps.get_model("alexandria_core", "Tag")
    start_time = datetime.datetime.now()

    pk_mapping = {}

    # create a uuid for each tag
    for tag in Tag.objects.all():
        old_pk = tag.slug
        new_pk = uuid.uuid4()

        pk_mapping[old_pk] = new_pk

        tag.slug = new_pk
        # migrate the tag_synonym_group
        tag.tag_synonym_group = tag.tag_synonym_group

        tag.save()

    # migrate the document tags
    Document = apps.get_model("alexandria_core", "Document")
    for document in Document.objects.all():
        for tag in document.tags.all():
            document.tags.add(pk_mapping[tag.slug])
            document.tags.remove(tag)

    # delete the slug tags, which all should be older than start_time
    for tag in Tag.objects.filter(created_at__lt=start_time):
        tag.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("alexandria_core", "0010_mark"),
    ]

    operations = [
        migrations.RunPython(slug_to_uuid, reverse_code=migrations.RunPython.noop),
    ]
