import hashlib
import logging
import re
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoCoreValidationError
from django.core.files import File as DjangoFile
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models.fields.files import ImageFile
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField, LocalizedTextField
from preview_generator.exception import UnsupportedMimeType
from preview_generator.manager import PreviewManager

from alexandria.core.presign_urls import make_signature_components
from alexandria.storages.fields import DynamicStorageFileField

log = logging.getLogger(__name__)


def upload_file_content_to(instance, _):
    return f"{instance.pk}_{instance.name}"


def make_uuid():
    """Return a new random UUID value.

    This indirection is done for testing purposes, so test code can mock
    uuid.uuid4(). If we wouldn't do this, then the models would have a direct
    reference that doesn't get mocked away.

    We can't replace it with a lambda because Django Migrations can't handle them.
    """
    return uuid.uuid4()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by_user = models.CharField(
        _("created by user"), max_length=150, blank=True, null=True
    )
    created_by_group = models.CharField(
        _("created by group"), max_length=255, blank=True, null=True
    )
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    modified_by_user = models.CharField(
        _("created by user"), max_length=150, blank=True, null=True
    )
    modified_by_group = models.CharField(
        _("created by group"), max_length=255, blank=True, null=True
    )
    metainfo = models.JSONField(_("metainfo"), default=dict)

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    """
    Models which use uuid as primary key.

    Defined as alexandria default
    """

    id = models.UUIDField(primary_key=True, default=make_uuid, editable=False)

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    """
    Models which use a slug as primary key.

    Defined as alexandria default for configuration so it is possible
    to merge between developer and user configuration.
    """

    slug = models.SlugField(max_length=255, primary_key=True)

    class Meta:
        abstract = True


COLOR_RE = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
color_validator = RegexValidator(COLOR_RE, _("Enter a valid color."), "invalid")


class Category(SlugModel):
    name = LocalizedCharField(
        _("category name"), blank=False, null=False, required=False
    )
    description = LocalizedTextField(
        _("category description"), null=True, blank=True, required=False
    )
    color = models.CharField(
        max_length=18,
        default="#FFFFFF",
        validators=[color_validator],
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )


class TagSynonymGroup(BaseModel):
    pass


class Tag(UUIDModel):
    name = models.CharField(_("tag name"), blank=False, null=False, max_length=100)
    description = LocalizedTextField(
        _("tag description"), null=True, blank=True, required=False
    )
    tag_synonym_group = models.ForeignKey(
        TagSynonymGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tags",
    )


class Mark(SlugModel):
    name = LocalizedTextField(_("Mark name"), blank=False, null=False, max_length=100)
    description = LocalizedTextField(
        _("Mark description"), null=True, blank=True, required=False
    )


class Document(UUIDModel):
    title = LocalizedCharField(
        _("document title"), blank=True, null=True, required=False
    )
    description = LocalizedTextField(
        _("document description"), null=True, blank=True, required=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="documents")
    marks = models.ManyToManyField(Mark, blank=True, related_name="documents")
    date = models.DateField(blank=True, null=True)

    def get_latest_original(self):
        return self.files.filter(variant=File.Variant.ORIGINAL).latest("created_at")

    @transaction.atomic()
    def clone(self):
        latest_original = self.get_latest_original()
        self.pk = None
        self.save()

        with NamedTemporaryFile() as tmp:
            temp_file = Path(tmp.name)
            with temp_file.open("w+b") as file:
                file.write(latest_original.content.file.file.read())

                latest_original.content = DjangoFile(file)
                latest_original.pk = None
                latest_original.document = self
                latest_original.save()

        try:
            latest_original.create_thumbnail()
        except DjangoCoreValidationError as e:
            log.error(
                "Object {obj} created successfully. Thumbnail creation failed. Error: {error}".format(
                    obj=latest_original, error=e.messages
                )
            )

        return self


class File(UUIDModel):
    class EncryptionStatus(models.TextChoices):
        NOT_ENCRYPTED = "none", "No at-rest enryption"
        SSEC_GLOBAL_KEY = "ssec-global", "SSE-C global key encryption (AES256)"
        # NOTE: per object encryption is not implemented yet
        SSEC_OBJECT_KEY = "ssec-object", "SSE-C per object encryption (AES256)"

        __empty__ = "Encryption status not set"

    class Variant(models.TextChoices):
        ORIGINAL = "original", "original"
        THUMBNAIL = "thumbnail", "thumbnail"

    variant = models.CharField(
        choices=Variant.choices, max_length=23, default=Variant.ORIGINAL
    )
    original = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="renderings",
    )
    name = models.CharField(_("file name"), max_length=255)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="files"
    )
    checksum = models.CharField(_("checksum"), max_length=255, null=True, blank=True)
    encryption_status = models.CharField(
        choices=EncryptionStatus.choices,
        max_length=12,
        default=None,
        null=True,
        blank=True,
    )
    content = DynamicStorageFileField(upload_to=upload_file_content_to, max_length=300)
    mime_type = models.CharField(max_length=255)
    size = models.IntegerField()

    @staticmethod
    def make_checksum(bytes_: bytes) -> str:
        return f"sha256:{hashlib.sha256(bytes_).hexdigest()}"

    def set_checksum(self):
        self.checksum = self.make_checksum(self.content.file.file.read())

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if settings.ALEXANDRIA_ENABLE_CHECKSUM:
            self.set_checksum()
        return super().save(force_insert, force_update, using, update_fields)

    def create_thumbnail(self):
        if not settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION:
            return

        with NamedTemporaryFile() as tmp:
            temp_file = Path(tmp.name)
            manager = PreviewManager(str(temp_file.parent))
            with temp_file.open("wb") as f:
                f.write(self.content.file.file.read())
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
                msg = f"Unsupported MimeType for file {self.name}"
                raise DjangoCoreValidationError(msg)

        with path_to_preview_image.open("rb") as thumb:
            if self.variant == File.Variant.THUMBNAIL:
                self.content = ImageFile(thumb)
                self.save()
                return self
            file = ImageFile(thumb)
            thumb_file = File.objects.create(
                name=f"{self.name}_preview.jpg",
                document=self.document,
                variant=File.Variant.THUMBNAIL.value,
                original=self,
                encryption_status=self.encryption_status,
                content=file,
                mime_type="image/jpeg",
                size=file.size,
            )

        return thumb_file

    def get_download_url(self, request):
        if not request:
            return None

        url, expires, signature = make_signature_components(
            str(self.pk),
            request.get_host(),
            scheme=request.META.get("wsgi.url_scheme", "http"),
        )

        return f"{url}?expires={expires}&signature={signature}"

    class Meta:
        ordering = ["-created_at"]


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete file from filesystem when `File` object is deleted."""

    instance.content.delete(save=False)
