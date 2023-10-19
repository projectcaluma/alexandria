from django.core.management import call_command

from ..models import Category


def test_load_example_data(db):
    assert len(Category.objects.all()) == 0

    call_command("loaddata", "initial_data.json")

    assert len(Category.objects.all()) == 6
    assert Category.objects.get(pk="alle-beteiligten").color == "#CB68C1"
