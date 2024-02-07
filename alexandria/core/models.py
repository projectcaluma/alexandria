import hashlib
import re
import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField, LocalizedTextField

from alexandria.storages.fields import DynamicStorageFileField


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

    def clone(self):
        latest_original = (
            self.files.filter(variant="original").order_by("-created_at").first()
        )
        self.pk = None
        self.save()

        # TODO: decide on how to deal with thumbnail creation
        latest_original.pk = None
        latest_original.document = self
        latest_original.save()

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

    class Meta:
        ordering = ["-created_at"]


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete file from filesystem when `File` object is deleted."""

    instance.content.delete(save=False)
