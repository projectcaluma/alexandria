from collections import defaultdict

import botocore
from django.core.management.base import BaseCommand
from tqdm import tqdm

from alexandria.core.models import File


class Command(BaseCommand):
    help = "Fixes copied file references by creating a new copy."

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)
        parser.add_argument("--since", dest="since", type=str, default=None)

    def handle(self, *args, **options):
        filename_counts = defaultdict(list)
        file_list = File.objects.filter(variant="original")

        for tmp_file in tqdm(file_list.order_by("created_at").iterator()):
            filename = tmp_file.content.name
            filename_counts[filename].append(tmp_file.pk)

        fix_count = 0
        for filename, pks in filename_counts.items():
            # Skip files that only have one reference.
            pks_len = len(pks)
            if pks_len <= 1:
                continue

            duplicates_query = File.objects.filter(pk__in=pks).order_by("created_at")

            # Filter copies by file creation timestamp if provided
            if options["since"]:
                duplicates_query = duplicates_query.filter(
                    created_at__gt=options["since"]
                )

            original_duplicate, *duplicates = duplicates_query

            ignored_output = ""
            duplicates_len = len(duplicates)
            if duplicates_len < (pks_len - 1):
                ignored_len = pks_len - duplicates_len
                ignored_output = f"/{pks_len} (ignored {ignored_len} files older than {options['since']})"

            checksum = original_duplicate.checksum
            self.stdout.write(
                self.style.SUCCESS(
                    f'Fixing filename "{filename}" with {duplicates_len}{ignored_output} duplicate(s)'
                )
            )

            for duplicate in duplicates:
                # Check if the duplicate has a checksum and skip if it does not match
                # the original. If it does not have a checksum, we try to copy the
                # original file.
                if duplicate.checksum and duplicate.checksum != checksum:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Failed: File ID {duplicate.pk} with filename {filename} has a different checksum than the original."
                        )
                    )
                    continue

                new_filename = f"{duplicate.pk}_{duplicate.name}"

                try:
                    # perform the copy operation
                    if not options["dry"]:
                        duplicate.content.copy(f"{duplicate.pk}_{duplicate.name}")

                    self.stdout.write(
                        self.style.SUCCESS(
                            f" > Fixed file ID {duplicate.pk} with new filename {new_filename} (Checksum: {checksum})"
                        )
                    )
                    fix_count += 1
                except botocore.exceptions.ClientError as e:
                    if e.response["Error"]["Code"] == "NoSuchKey":
                        self.stderr.write(
                            self.style.ERROR(
                                f" > Failed: File ID {duplicate.pk} with filename {duplicate.content.name} does not exist in S3. (Checksum: {checksum})"
                            )
                        )
                    else:
                        self.stderr.write(
                            self.style.ERROR(
                                f" > Failed: Error while fixing File ID {duplicate.pk} with filename {duplicate.content.name}, client error: {e} (Checksum: {checksum})"
                            )
                        )
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f" > Failed: Error while fixing File ID {duplicate.pk} with filename {duplicate.content.name}, error: {e} (Checksum: {checksum})"
                        )
                    )

        self.stdout.write("")
        if fix_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Fixed {fix_count} files with copied references.")
            )
        else:
            self.stdout.write(
                self.style.WARNING("No files with copied references where fixed.")
            )
