from django.db import models
from django.utils.translation import gettext_lazy as _

from alexandria.core.models import File, UUIDModel


class SignatureType(models.TextChoices):
    TIMESTAMP = "timestamp", _("Timestamp")
    ADVANCED = "advanced", _("Advanced")
    QUALIFIED = "qualified", _("Qualified")


class SignatureRequestStatus(models.TextChoices):
    OPEN = "open", _("Open")
    REQUESTED = "requested", _("Requested")
    CONFIRMED = "confirmed", _("Confirmed")
    DONE = "done", _("Done")
    TIMEOUT = "timeout", _("Timeout")
    REJECTED = "rejected", _("Rejected")
    # The user has to register with the provider first (`action_url`). Ends
    # the request, the user starts a new one after registering.
    REGISTRATION_REQUIRED = "registration_required", _("Registration required")
    # The document got a newer version while signing, signing it would undo
    # those changes
    OUTDATED = "outdated", _("Outdated")
    # The signature could not be embedded into the PDF
    FAILED = "failed", _("Failed")


ACTIVE_SIGNATURE_REQUEST_STATUSES = (
    SignatureRequestStatus.OPEN,
    SignatureRequestStatus.REQUESTED,
    SignatureRequestStatus.CONFIRMED,
)


class SignatureRequestQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=ACTIVE_SIGNATURE_REQUEST_STATUSES)

    def for_file(self, file):
        return self.filter(file=file)


class SignatureRequest(UUIDModel):
    """State of an asynchronous signature request between polls.

    The requesting user is stored in `created_by_user`. The `provider_*`
    fields and `prepared_content` are managed by the configured backend.
    """

    Status = SignatureRequestStatus
    Type = SignatureType

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name="signature_requests",
        help_text=_("File to be signed"),
    )
    signature_type = models.CharField(
        _("Signature type"),
        max_length=16,
        choices=Type.choices,
        null=True,
        blank=True,
        help_text=_("Kind of signature requested, set by the backend"),
    )
    status = models.CharField(
        _("Status"),
        max_length=32,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
    )
    timeout = models.DateTimeField(
        _("Timeout"),
        null=True,
        blank=True,
        help_text=_("After this point in time the request is cleaned up"),
    )
    action_url = models.URLField(
        _("Action URL"),
        max_length=2048,
        null=True,
        blank=True,
        help_text=_("URL the user has to open, e.g. an external signing tool"),
    )
    provider_reference = models.CharField(
        _("Provider reference"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("ID of the request at the provider"),
    )
    provider_status = models.CharField(
        _("Provider status"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Raw status of the request at the provider"),
    )
    provider_data = models.JSONField(
        _("Provider data"),
        default=dict,
        help_text=_("Backend specific state kept between polls"),
    )
    prepared_content = models.BinaryField(
        _("Prepared content"),
        null=True,
        blank=True,
        help_text=_("PDF with reserved signature space, kept between polls"),
    )

    objects = SignatureRequestQuerySet.as_manager()

    class Meta:
        verbose_name = _("Signature request")
        verbose_name_plural = _("Signature requests")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["file"],
                condition=models.Q(status__in=ACTIVE_SIGNATURE_REQUEST_STATUSES),
                name="unique_active_signature_request_per_file",
                violation_error_message=_(
                    "A signature process for this file is already in progress."
                ),
            )
        ]

    def __str__(self):
        return f"{self.file_id} ({self.status})"

    @property
    def is_active(self):
        return self.status in ACTIVE_SIGNATURE_REQUEST_STATUSES


class Signature(UUIDModel):
    """Metadata of a signature embedded in a file."""

    Type = SignatureType

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name="signatures",
        help_text=_("File containing the signature"),
    )
    signature_request = models.ForeignKey(
        SignatureRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="signatures",
    )
    signature_type = models.CharField(
        _("Signature type"), max_length=16, choices=Type.choices
    )
    signer_name = models.CharField(
        _("Signer name"),
        max_length=255,
        blank=True,
        help_text=_("Name read from the signature certificate"),
    )
    signed_at = models.DateTimeField(_("Signed at"))
    signature_hash = models.CharField(_("Signature hash"), max_length=255)

    class Meta:
        verbose_name = _("Signature")
        verbose_name_plural = _("Signatures")
        ordering = ["-signed_at"]

    def __str__(self):
        return (
            f"{self.get_signature_type_display()} {self.signer_name} ({self.signed_at})"
        )
