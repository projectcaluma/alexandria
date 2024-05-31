import mimetypes
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.core.management.base import BaseCommand
from psutil import virtual_memory
from tqdm import tqdm

from alexandria.core.models import File


class Command(BaseCommand):
    help = "Sets mime type and size of files that don't have it yet"

    def handle(self, *args, **options):
        files = File.objects.filter(mime_type="application/octet-stream", size=0)

        for file in tqdm(files):
            with NamedTemporaryFile() as tmp:
                temp_file = Path(tmp.name)
                with temp_file.open("wb") as f:
                    f.write(file.content.file.file.read())
                file.size = os.path.getsize(temp_file)
                tmp.close()

            mime_type, _ = mimetypes.guess_type(file.content.file.name)
            if mime_type:
                file.mime_type = mime_type

            file.save()

            if virtual_memory().available < 300_000_000:
                print("about to run out of memory, stopping")
                break
