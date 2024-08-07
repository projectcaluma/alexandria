# Generated by Django 3.2.20 on 2023-08-14 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alexandria_core", "0006_rename_metainfo_jsonfield_verbose_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="alexandria_core.category",
            ),
        ),
    ]
