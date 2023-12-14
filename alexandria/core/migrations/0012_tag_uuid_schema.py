from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("alexandria_core", "0011_tag_uuid"),
    ]

    operations = [
        # indexes and constraints have to be dropped before changing the data type
        # drop primary key constraint
        migrations.RunSQL(
            "ALTER TABLE alexandria_core_tag DROP CONSTRAINT alexandria_core_tag_pkey CASCADE;"
        ),
        # drop slug index on tag table
        migrations.RunSQL("DROP INDEX alexandria_core_tag_slug_1d1ce021_like;"),
        # drop tag_id index on document-tag table
        migrations.RunSQL(
            "DROP INDEX alexandria_core_document_tags_tag_id_8dc7fb00_like;"
        ),
        # change string to uuid
        migrations.RunSQL(
            "ALTER TABLE alexandria_core_tag ALTER COLUMN slug TYPE uuid USING slug::uuid;"
        ),
        migrations.RunSQL(
            "ALTER TABLE alexandria_core_document_tags ALTER COLUMN tag_id TYPE uuid USING tag_id::uuid;"
        ),
        # rename column
        migrations.RenameField(
            model_name="tag",
            old_name="slug",
            new_name="id",
        ),
        # recreate primary key constraint and index
        migrations.RunSQL(
            "ALTER TABLE alexandria_core_tag ADD CONSTRAINT alexandria_core_tag_pkey PRIMARY KEY (id);"
        ),
        # recreate foreign key constraint
        migrations.RunSQL(
            "ALTER TABLE alexandria_core_document_tags ADD CONSTRAINT alexandria_core_docu_tag_id_8dc7fb00_fk_alexandri FOREIGN KEY (tag_id) REFERENCES alexandria_core_tag (id) DEFERRABLE INITIALLY DEFERRED;"
        ),
    ]
