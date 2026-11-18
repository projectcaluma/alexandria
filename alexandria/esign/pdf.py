"""PAdES hash signing helpers based on pyHanko.

Interrupted signing: the signer certificate is only known once the provider
returned the signature, so the PDF is prepared with reserved space for the
signature, the digest is sent to the provider, and the returned CMS signature
is embedded later. See
https://docs.pyhanko.eu/en/latest/lib-guide/signing.html#interrupted-signing-when-the-signer-s-certificate-is-not-known-a-priori

Stamps are document timestamps, added in one go by `timestamp`.
"""

import asyncio
import base64
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO

from asgiref.sync import async_to_sync
from asn1crypto import cms, crl, ocsp
from asn1crypto.x509 import Certificate
from PIL import Image
from pyhanko.pdf_utils import generic, layout
from pyhanko.pdf_utils.images import PdfImage
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec, SigSeedSubFilter, append_signature_field
from pyhanko.sign.signers.pdf_byterange import PreparedByteRangeDigest
from pyhanko.sign.signers.pdf_cms import ExternalSigner
from pyhanko.sign.signers.pdf_signer import PdfTBSDocument
from pyhanko.sign.timestamps import TimeStamper
from pyhanko.sign.validation.dss import DocumentSecurityStore
from pyhanko.stamp import TextStampStyle

DIGEST_ALGORITHM = "sha512"


@dataclass
class PreparedPdf:
    digest: PreparedByteRangeDigest
    content: bytes


@dataclass
class EmbeddedSignature:
    signer_name: str | None
    signed_at: datetime | None


def _field_name(reader: PdfFileReader) -> str:
    """Return a signature field name that does not exist in the PDF yet."""
    existing = {sig.field_name for sig in reader.embedded_signatures}
    index = len(existing) + 1
    while f"Signature{index}" in existing:  # pragma: no cover
        index += 1
    return f"Signature{index}"


def prepare(content: bytes, bytes_reserved: int) -> PreparedPdf:
    """Add an empty signature field to the PDF and compute its digest.

    `bytes_reserved` must be big enough for the CMS signature returned by the
    provider, including certificates and revocation info.
    """
    writer = IncrementalPdfFileWriter(BytesIO(content))
    pdf_signer = signers.PdfSigner(
        signers.PdfSignatureMetadata(
            field_name=_field_name(writer.prev),
            md_algorithm=DIGEST_ALGORITHM,
            subfilter=SigSeedSubFilter.PADES,
        ),
        # The signer certificate is not known yet. The signature value is a
        # placeholder, the real signature is embedded in `finish`.
        signer=ExternalSigner(
            signing_cert=None, cert_registry=None, signature_value=bytes(512)
        ),
    )
    digest, _tbs_document, output = async_to_sync(
        pdf_signer.async_digest_doc_for_signing
    )(writer, bytes_reserved=bytes_reserved)
    return PreparedPdf(digest=digest, content=output.getvalue())


def serialize_digest(digest: PreparedByteRangeDigest) -> dict:
    return {
        "document_digest": base64.b64encode(digest.document_digest).decode("ascii"),
        "reserved_region_start": digest.reserved_region_start,
        "reserved_region_end": digest.reserved_region_end,
    }


def deserialize_digest(data: dict) -> PreparedByteRangeDigest:
    return PreparedByteRangeDigest(
        document_digest=base64.b64decode(data["document_digest"]),
        reserved_region_start=data["reserved_region_start"],
        reserved_region_end=data["reserved_region_end"],
    )


def finish(
    prepared_content: bytes, digest: PreparedByteRangeDigest, signature: bytes
) -> bytes:
    """Embed the DER encoded CMS `signature` into the prepared PDF."""
    output = BytesIO(prepared_content)
    PdfTBSDocument.finish_signing(output, digest, signature)
    return output.getvalue()


class _CallbackTimeStamper(TimeStamper):
    """Get the timestamp token from a callback instead of a TSA URL."""

    def __init__(self, request_token: Callable[[bytes], bytes]):
        super().__init__()
        self._request_token = request_token

    async def async_timestamp(self, message_digest, md_algorithm):
        # The callback is blocking (HTTP), keep it out of the event loop
        token = await asyncio.to_thread(self._request_token, message_digest)
        return cms.ContentInfo.load(token)


@dataclass
class StampAppearance:
    """Visible stamp, `box` is `(x1, y1, x2, y2)` in PDF points from the
    bottom left corner of page `page`."""

    box: tuple[float, float, float, float]
    image: bytes | None = None
    text: str | None = None
    page: int = 0
    opacity: float = 0.6


def _add_visible_field(writer, field_name: str, appearance: StampAppearance):
    """Create the timestamp field with the stamp as its appearance.

    A new signature field with appearance is an allowed change after earlier
    signatures. A separate annotation or drawing into the page content would
    make them report "document modified after signing".
    """
    x1, y1, x2, y2 = appearance.box
    append_signature_field(
        writer,
        SigFieldSpec(
            sig_field_name=field_name, on_page=appearance.page, box=appearance.box
        ),
    )
    style = TextStampStyle(
        # Interpolated by pyhanko, a literal `%` has to be escaped
        stamp_text=(appearance.text or "").replace("%", "%%"),
        background=(
            PdfImage(Image.open(BytesIO(appearance.image)))
            if appearance.image
            else None
        ),
        background_opacity=appearance.opacity,
        border_width=0,
    )
    stamp = style.create_stamp(
        writer, layout.BoxConstraints(width=x2 - x1, height=y2 - y1), text_params={}
    )
    field = next(
        ref.get_object()
        for ref in writer.root["/AcroForm"]["/Fields"]
        if ref.get_object().get("/T") == field_name
    )
    field["/AP"] = generic.DictionaryObject({generic.pdf_name("/N"): stamp.register()})


def timestamp(
    content: bytes,
    bytes_reserved: int,
    request_token: Callable[[bytes], bytes],
    appearance: StampAppearance | None = None,
) -> bytes:
    """Add a document timestamp (stamp) to the PDF.

    A RFC 3161 timestamp token is no CMS signature, it has to be embedded as
    `/DocTimeStamp` with subfilter `/ETSI.RFC3161`, otherwise validators
    reject it. `request_token` receives the SHA-512 document digest and
    returns the DER encoded timestamp token.

    With `appearance`, the timestamp field shows the stamp, the timestamp
    covers it.
    """
    writer = IncrementalPdfFileWriter(BytesIO(content))
    field_name = _field_name(writer.prev)
    if appearance:
        _add_visible_field(writer, field_name, appearance)

    stamper = signers.PdfTimeStamper(
        timestamper=_CallbackTimeStamper(request_token), field_name=field_name
    )
    output = async_to_sync(stamper.async_timestamp_pdf)(
        writer, DIGEST_ALGORITHM, bytes_reserved=bytes_reserved
    )
    return output.getvalue()


def add_validation_info(
    content: bytes,
    certs: list[bytes] = (),
    ocsps: list[bytes] = (),
    crls: list[bytes] = (),
) -> bytes:
    """Store certificates and revocation info in the PDF (DSS).

    Long-term validation (LTV): validators can still check the signatures
    after the certificates expired or the revocation services are offline.
    Values are DER encoded.
    """
    output = BytesIO(content)
    DocumentSecurityStore.add_dss(
        output,
        sig_contents=None,
        certs=[Certificate.load(c) for c in certs],
        ocsps=[ocsp.OCSPResponse.load(o) for o in ocsps],
        crls=[crl.CertificateList.load(c) for c in crls],
    )
    return output.getvalue()


def timestamp_certificates(token: bytes) -> list[bytes]:
    """Return the DER encoded certificates embedded in a timestamp token."""
    signed_data = cms.ContentInfo.load(token)["content"]
    return [cert.chosen.dump() for cert in signed_data["certificates"] or []]


def last_signature(content: bytes) -> EmbeddedSignature:
    """Return signer and signing time of the last signature in the PDF."""
    signature = PdfFileReader(BytesIO(content)).embedded_signatures[-1]
    if signature.sig_object_type == "/DocTimeStamp":
        # Signed by the timestamp authority, the time is in the token
        tst_info = signature.signed_data["encap_content_info"]["content"].parsed
        signed_at = tst_info["gen_time"].native
    else:
        signed_at = signature.self_reported_timestamp
    return EmbeddedSignature(
        signer_name=signature.signer_cert.subject.native.get("common_name"),
        signed_at=signed_at,
    )
