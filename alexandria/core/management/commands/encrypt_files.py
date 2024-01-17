from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from tqdm import tqdm

from alexandria.core.models import File
from alexandria.storages.backends.s3 import SsecGlobalS3Storage

# This is needed to disable the warning about not verifying the SSL certificate.
# It spams the output otherwise.
if not settings.AWS_S3_VERIFY:
    import urllib3

    urllib3.disable_warnings()


class Command(BaseCommand):
    help = "Swaps plain text file content to encrypted content"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        if (
            not settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION
            or settings.ALEXANDRIA_ENCRYPTION_METHOD
            == File.EncryptionStatus.NOT_ENCRYPTED.value
        ):
            return self.stdout.write(
                self.style.WARNING(
                    "Encryption is not enabled. Skipping encryption of files."
                )
            )
        # disable checksums to prevent errors
        checksum = settings.ALEXANDRIA_ENABLE_CHECKSUM
        settings.ALEXANDRIA_ENABLE_CHECKSUM = False

        sid = transaction.savepoint()

        # flip between default and encrypted storage to have the correct parameters in the requests
        DefaultStorage = get_storage_class()
        for file in tqdm(
            File.objects.filter(
                Q(encryption_status=File.EncryptionStatus.NOT_ENCRYPTED)
                | Q(encryption_status__isnull=True)
            ),
        ):
            # get original file content
            file.content.storage = DefaultStorage()
            content = file.content.open()

            if not options["dry"]:
                # overwrite with encrypted content
                file.content.storage = SsecGlobalS3Storage()
                file.content.save(file.content.name, content)

            # set encryption status
            file.encryption_status = settings.ALEXANDRIA_ENCRYPTION_METHOD
            file.save()

        settings.ALEXANDRIA_ENABLE_CHECKSUM = checksum
        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
