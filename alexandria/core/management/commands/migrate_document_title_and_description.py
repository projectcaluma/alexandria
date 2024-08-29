from django.core.management.base import BaseCommand
from pghstore import loads
from tqdm import tqdm

from alexandria.core.models import Document


class Command(BaseCommand):
    help = "Migrate document title and description from localized to unlocalized."

    def add_arguments(self, parser):
        parser.add_argument("source_language")

    def handle(self, *args, **options):
        source_language = options["source_language"]
        for document in tqdm(Document.objects.all()):
            try:
                document.title = loads(document.title)[source_language]
                document.description = loads(document.description)[source_language]
                document.save()
            except ValueError:
                pass
