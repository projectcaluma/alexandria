# Make tag names monolingual.
#
# Note: There are no actual users of this app yet, so we
# don't bother to convert the names properly.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alexandria_core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=100, verbose_name="tag name"),
        ),
    ]
