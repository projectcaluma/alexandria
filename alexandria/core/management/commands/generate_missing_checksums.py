from django.core.management.base import BaseCommand
from tqdm import tqdm

from alexandria.core.models import File
from alexandria.core.tasks import make_checksum


class Command(BaseCommand):
    help = "Finds files that don't have a checksum and generates them."

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    def handle(self, *args, **options):
        fix_count = 0
        for file in tqdm(File.objects.filter(checksum__isnull=True)):
            file.content.file.file.seek(0)
            checksum = make_checksum(file.content.file.file.read())
            file.checksum = checksum

            if not options["dry"]:
                file.save(update_fields=["checksum"])

            fix_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Generated checksum for file {file.pk} with checksum {checksum}"
                )
            )

        self.stdout.write("")
        if fix_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Generated {fix_count} missing checksums.")
            )
        else:
            self.stdout.write(
                self.style.WARNING("No files with a missing checksum where found.")
            )
