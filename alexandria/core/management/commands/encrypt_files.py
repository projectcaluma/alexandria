from django.core.management.base import BaseCommand
from alexandria.core.models import File
from django.conf import settings
from tqdm import tqdm


class Command(BaseCommand):
    help = "Swaps plain text file content to encrypted content"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    def handle(self, *args, **options):
        for file in tqdm(
            File.objects.filter(encryption_status=File.EncryptionStatus.NOT_ENCRYPTED)
        ):
            # get original file content
            content = file.content.open()

            # overwrite with encrypted content
            file.content.save(file.content.name, content)

            # set encryption status
            file.encryption_status = settings.ALEXANDRIA_ENCRYPTION_METHOD
            file.save()
