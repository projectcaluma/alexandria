import hashlib
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import requests
from django.conf import settings
from preview_generator.exception import UnsupportedMimeType
from preview_generator.manager import PreviewManager

from alexandria.core.models import File

from .storage_clients import client


def get_file(file):
    # TODO: this should be run by a task queue
    data = client.get_object(file.object_name)

    temp_dir = TemporaryDirectory()
    temp_filepath = Path(os.path.join(temp_dir.name, str(uuid4())))

    with temp_filepath.open("wb") as f:
        for d in data.stream(32 * 1024):
            f.write(d)

    return temp_dir, temp_filepath


def create_thumbnail(file, temp_dir, temp_filepath):
    manager = PreviewManager(str(temp_dir.name))

    preview_kwargs = {}
    if settings.ALEXANDRIA_THUMBNAIL_WIDTH:  # pragma: no cover
        preview_kwargs["width"] = settings.ALEXANDRIA_THUMBNAIL_WIDTH
    if settings.ALEXANDRIA_THUMBNAIL_HEIGHT:  # pragma: no cover
        preview_kwargs["height"] = settings.ALEXANDRIA_THUMBNAIL_HEIGHT

    try:
        path_to_preview_image = manager.get_jpeg_preview(
            str(temp_filepath), **preview_kwargs
        )
    except UnsupportedMimeType:
        temp_filepath.unlink()
        return False
    thumb_file = File.objects.create(
        name=f"{file.name}.jpg",
        document=file.document,
        variant=File.THUMBNAIL,
        original=file,
    )

    upload_url = client.upload_url(thumb_file.object_name)
    with Path(path_to_preview_image).open("br") as f:
        result = requests.put(
            upload_url, headers={"Content-Type": "image/jpeg"}, data=f.read()
        )

    thumb_file.upload_status = File.COMPLETED if result.ok else File.ERROR
    thumb_file.save()

    return result.ok


def get_checksum(temp_filepath):
    with open(temp_filepath, "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()

        return f"sha256:{checksum}"
