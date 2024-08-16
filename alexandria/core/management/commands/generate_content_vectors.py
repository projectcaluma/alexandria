from django.conf import settings
from django.core.management.base import BaseCommand
from psutil import virtual_memory
from tqdm import tqdm

from alexandria.core.models import File
from alexandria.core.tasks import set_content_vector


class Command(BaseCommand):
    help = "Fills content_vector for files that don't have their content vectorized for full text search."

    def handle(self, *args, **options):
        if not settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH:
            return self.stdout.write(
                self.style.WARNING(
                    "Content search is not enabled. Skipping vectorization of file contents."
                )
            )

        # disable additional features to focus on vectorization
        settings.ALEXANDRIA_ENABLE_CHECKSUM = False
        settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = False

        failed_files = []
        query = File.objects.filter(variant="original", content_vector__isnull=True)
        # iterate over files in batches to prevent memory exhaustion
        for file in tqdm(query.iterator(50), "Generating vectors", query.count()):
            try:
                set_content_vector(file.pk)
            except Exception as e:  # noqa: B902
                failed_files.append(str(file.id))
                self.stdout.write(
                    self.style.WARNING(f"Error processing {file.id}: {e}")
                )

            if virtual_memory().available < 300_000_000:  # pragma: no cover
                self.stdout.write(
                    self.style.ERROR("about to run out of memory, stopping")
                )
                break

        if failed_files:
            self.stdout.write(
                self.style.WARNING(
                    f"Failed to process {len(failed_files)} files: {failed_files}"
                )
            )
