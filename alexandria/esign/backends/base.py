from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

if TYPE_CHECKING:  # pragma: no cover
    from alexandria.core.models import File
    from alexandria.esign.models import Signature, SignatureRequest


class SignatureProviderError(APIException):
    """The signature provider failed or returned an unexpected response."""

    status_code = 502
    default_detail = _("The signature provider is not available.")
    default_code = "signature_provider_error"


class SignatureBackend(ABC):
    """Contract for signature provider implementations.

    One backend is configured per deployment via `ALEXANDRIA_ESIGN_BACKEND`.

    `request_signature`, `poll_signature` and `cancel_signature` update the
    given request in place (`signature_type`, `status`,
    `provider_reference`, `provider_status`, `action_url`, `provider_data`,
    `prepared_content`, `timeout`). The caller saves it.

    Backends where the user signs in an external tool set `action_url` in
    `request_signature`. The frontend opens it and keeps polling until the request is
    no longer active.
    """

    @abstractmethod
    def is_enabled_for(self, group: str | None) -> bool:
        """Return whether members of `group` are allowed to sign."""
        ...  # pragma: no cover

    @abstractmethod
    def request_signature(self, signature_request: "SignatureRequest") -> None:
        """Start the signature process at the provider."""
        ...  # pragma: no cover

    @abstractmethod
    def poll_signature(self, signature_request: "SignatureRequest") -> None:
        """Fetch the current state from the provider.

        Once the provider returns the signature, the backend embeds it into
        the PDF, creates the signed file and the `Signature`, and sets the
        status to `done`.
        """
        ...  # pragma: no cover

    @abstractmethod
    def cancel_signature(self, signature_request: "SignatureRequest") -> None:
        """Clean up a request that ran into its timeout."""
        ...  # pragma: no cover

    @abstractmethod
    def stamp(
        self, file: "File", user: str | None, group: str | None, data: dict
    ) -> "Signature":
        """Stamp `file` with a timestamp signature (seal).

        Stamps need no confirmation, so this runs synchronously. The stamped
        PDF is stored as new version of the document, see
        `alexandria.esign.api.store_signed_file`.

        `data` is backend specific, e.g. the visible stamp image.
        """
        ...  # pragma: no cover
