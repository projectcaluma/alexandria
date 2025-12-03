from django.core.management.base import BaseCommand
from django.template.defaultfilters import filesizeformat, truncatechars
from psutil import virtual_memory
from tqdm import tqdm

from alexandria.core.models import File
from alexandria.core.tasks import create_thumbnail


class Command(BaseCommand):
    help = "Finds documents that don't have a thumbnail and generates them."

    def handle(self, *args, **options):
        pbar = tqdm(File.objects.filter(variant="original", renderings__isnull=True).order_by("size"))
        for file in pbar:
            pbar.set_description(
                f"Processing {truncatechars(file.name, 50) :<50} ({filesizeformat(file.size) :>10})"
            )
            create_thumbnail(file.pk)
            if virtual_memory().available < 300_000_000:
                print("about to run out of memory, stopping")
                break
