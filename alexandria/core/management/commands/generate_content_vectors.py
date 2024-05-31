from django.conf import settings
from django.core.management.base import BaseCommand
from psutil import virtual_memory
from tqdm import tqdm

from alexandria.core.models import File


class Command(BaseCommand):
    help = "Fills content_vector for files that don't have their content vectorized for full text search."

    def handle(self, *args, **options):
        if not settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH:
            return self.stdout.write(
                self.style.WARNING(
                    "Content search is not enabled. Skipping vectorization of file contents."
                )
            )

        for file in tqdm(
            File.objects.filter(variant="original", content_vector__isnull=True)
        ):
            file.set_content_vector()
            file.save()

            if virtual_memory().available < 300_000_000:  # pragma: no cover
                print("about to run out of memory, stopping")
                break
