from django.core.management.base import BaseCommand
from django.db.models import F, Max, Q
from tqdm import tqdm

from alexandria.core.models import Document


class Command(BaseCommand):
    """
    Fix modified_at in alexandria_core_document based on the latest file modification.

    For each document, sets the modified_at to the latest modified_at of its files,
    but only if the document's modified_at is older than the latest file modification.
    """

    help = (
        "Fix modified_at in alexandria_core_document based on latest file modification"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Actually commit the changes to the database (default is dry-run)",
        )

    def handle(self, *args, **options):
        commit = options["commit"]

        self.stdout.write(
            self.style.WARNING(
                "Fixing modified_at in alexandria_core_document based on latest file modifications..."
            )
        )

        if not commit:
            self.stdout.write(
                self.style.WARNING(
                    "Running in DRY-RUN mode. Use --commit to apply changes."
                )
            )

        # This query finds documents where the document's modified_at is older
        # than the latest modified_at of its files (excluding thumbnails)
        documents_queryset = (
            Document.objects.annotate(
                latest_file_modified=Max(
                    "files__modified_at", filter=~Q(files__variant="thumbnail")
                )
            )
            .filter(modified_at__lt=F("latest_file_modified"))
            .order_by("id")
        )

        total_documents = documents_queryset.count()

        if total_documents == 0:
            self.stdout.write(self.style.SUCCESS("No documents need to be updated."))
            return

        self.stdout.write(
            self.style.SUCCESS(f"Found {total_documents} documents to update")
        )

        batch_size = 100
        updated_count = 0

        with tqdm(total=total_documents, desc="Updating documents") as pbar:
            while updated_count < total_documents:
                if commit:
                    # commit: documents get updated and don't match query anymore
                    batch = list(
                        documents_queryset.values("id", "latest_file_modified")[
                            :batch_size
                        ]
                    )
                else:
                    # dry-run: use offset to skip already processed documents
                    batch = list(
                        documents_queryset.values("id", "latest_file_modified")[
                            updated_count : updated_count + batch_size
                        ]
                    )

                if not batch:
                    break

                # fetch document objects
                document_ids = [doc_data["id"] for doc_data in batch]
                documents_list = list(Document.objects.filter(id__in=document_ids))

                # create lookup for latest_file_modified values
                modified_at_lookup = {
                    doc_data["id"]: doc_data["latest_file_modified"]
                    for doc_data in batch
                }

                # update modified_at for each document
                for document in documents_list:
                    document.modified_at = modified_at_lookup[document.id]

                # bulk update all documents in this batch (only if commit is True)
                if documents_list:
                    if commit:
                        Document.objects.bulk_update(documents_list, ["modified_at"])
                    updated_count += len(documents_list)
                    pbar.update(len(documents_list))

        # summary
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 60))
        self.stdout.write(self.style.SUCCESS(f"Documents updated: {updated_count}"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        if commit:
            self.stdout.write(
                self.style.SUCCESS("\nChanges have been committed to the database.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "\nDRY-RUN: No changes were made. Use --commit to apply changes."
                )
            )
