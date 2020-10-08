from pathlib import Path

from django.conf import settings
from django.core.management import CommandError, call_command
from ..models import Category


def test_load_example_data(db):

    assert len(Category.objects.all()) == 0

    call_command("loaddata", "initial_data.json")

    assert len(Category.objects.all()) == 5
    assert Category.objects.first().color == "#CB68C1"
