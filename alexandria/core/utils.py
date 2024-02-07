from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFile
from preview_generator.exception import UnsupportedMimeType
from preview_generator.manager import PreviewManager

from alexandria.core.models import File


def create_thumbnail(file_: File):
    with NamedTemporaryFile() as tmp:
        temp_file = Path(tmp.name)
        manager = PreviewManager(str(temp_file.parent))
        with temp_file.open("wb") as f:
            f.write(file_.content.file.file.read())
        preview_kwargs = {}
        if settings.ALEXANDRIA_THUMBNAIL_WIDTH:  # pragma: no cover
            preview_kwargs["width"] = settings.ALEXANDRIA_THUMBNAIL_WIDTH
        if settings.ALEXANDRIA_THUMBNAIL_HEIGHT:  # pragma: no cover
            preview_kwargs["height"] = settings.ALEXANDRIA_THUMBNAIL_HEIGHT
        try:
            path_to_preview_image = Path(
                manager.get_jpeg_preview(str(temp_file), **preview_kwargs)
            )
        except UnsupportedMimeType:
            msg = f"Unsupported MimeType for file {file_.name}"
            raise ValidationError(msg)

    with path_to_preview_image.open("rb") as thumb:
        if file_.variant == File.Variant.THUMBNAIL:
            file_.content = ImageFile(thumb)
            file_.save()
            return file_
        file = ImageFile(thumb)
        thumb_file = File.objects.create(
            name=f"{file_.name}_preview.jpg",
            document=file_.document,
            variant=File.Variant.THUMBNAIL.value,
            original=file_,
            encryption_status=file_.encryption_status,
            content=file,
            mime_type="image/jpeg",
            size=file.size,
        )

    return thumb_file
