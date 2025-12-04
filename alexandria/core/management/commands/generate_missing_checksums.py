from django.core.management.base import BaseCommand
from django.template.defaultfilters import filesizeformat, truncatechars
from tqdm import tqdm

from alexandria.core.models import File
from alexandria.core.tasks import set_checksum


class Command(BaseCommand):
    help = "Finds documents that don't have a checksum and generates them."

    def handle(self, *args, **options):
        pbar = tqdm(
            File.objects.filter(variant="original", checksum__isnull=True).order_by(
                "size"
            )
        )
        for file in pbar:
            pbar.set_description(
                f"Processing {truncatechars(file.name, 50):<50} ({filesizeformat(file.size):>10})"
            )
            set_checksum(file.pk)
