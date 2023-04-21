import os
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from django.conf import settings
from preview_generator.exception import UnsupportedMimeType
from preview_generator.manager import PreviewManager

from alexandria.core.models import File

from .storage_clients import client


def create_thumbnail(file):
    # TODO: this should be run by a task queue
    data = client.get_object(file.object_name)

    temp_dir = TemporaryDirectory()
    temp_filepath = Path(os.path.join(temp_dir.name, str(uuid4())))

    with temp_filepath.open("wb") as f:
        for d in data.stream(32 * 1024):
            f.write(d)

    manager = PreviewManager(str(temp_dir.name))

    preview_kwargs = {}
    if settings.THUMBNAIL_WIDTH:  # pragma: no cover
        preview_kwargs["width"] = settings.THUMBNAIL_WIDTH
    if settings.THUMBNAIL_HEIGHT:  # pragma: no cover
        preview_kwargs["height"] = settings.THUMBNAIL_HEIGHT

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
    etag = client.put_object(path_to_preview_image, thumb_file.object_name)

    thumb_file.upload_status = File.COMPLETED if etag else File.ERROR
    thumb_file.save()

    temp_dir.cleanup()

    return etag
