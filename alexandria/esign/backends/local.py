"""Local signature provider for development, without DeepSign.

Signs and timestamps with a self-signed certificate created at runtime, so
validators report the signatures as untrusted. A signature completes on the
first poll, without confirmation. Only allowed with `DEBUG`.
"""

import datetime
from functools import cache

from asgiref.sync import async_to_sync
from asn1crypto import keys, x509
from cryptography import x509 as crypto_x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from pyhanko.sign.signers.pdf_cms import SimpleSigner
from pyhanko.sign.timestamps.dummy_client import DummyTimeStamper
from pyhanko_certvalidator.registry import SimpleCertificateStore

from alexandria.esign import pdf
from alexandria.esign.api import store_signed_file
from alexandria.esign.models import Signature, SignatureRequest

from .base import SignatureBackend

# Same as `ALEXANDRIA_DEEPSIGN_SIGNATURE_BYTES_RESERVED` would be overkill,
# the local signature contains no revocation info
BYTES_RESERVED = 16384
# Top right corner of an A4 page
STAMP_BOX = (415, 722, 565, 812)


@cache
def _signer() -> SimpleSigner:
    """Return a signer with a self-signed certificate, one per process."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = crypto_x509.Name(
        [crypto_x509.NameAttribute(NameOID.COMMON_NAME, "Alexandria Development")]
    )
    now = datetime.datetime.now(datetime.UTC)
    cert = (
        crypto_x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(crypto_x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=365))
        # Also used as timestamp authority
        .add_extension(
            crypto_x509.ExtendedKeyUsage([ExtendedKeyUsageOID.TIME_STAMPING]),
            critical=True,
        )
        .sign(key, hashes.SHA256())
    )
    signing_cert = x509.Certificate.load(cert.public_bytes(serialization.Encoding.DER))
    return SimpleSigner(
        signing_cert=signing_cert,
        signing_key=keys.PrivateKeyInfo.load(
            key.private_bytes(
                serialization.Encoding.DER,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        ),
        cert_registry=SimpleCertificateStore.from_certs([signing_cert]),
    )


class LocalBackend(SignatureBackend):
    """Development provider, enabled for every group."""

    def __init__(self):
        if not settings.DEBUG:
            raise ImproperlyConfigured(
                "The local signature backend can only be used in DEBUG mode!"
            )

    def is_enabled_for(self, group):
        return bool(group)

    def request_signature(self, signature_request):
        signature_request.signature_type = SignatureRequest.Type.ADVANCED
        with signature_request.file.content.open() as content:
            prepared = pdf.prepare(content.read(), bytes_reserved=BYTES_RESERVED)

        signature_request.status = SignatureRequest.Status.REQUESTED
        signature_request.provider_data = {
            "digest": pdf.serialize_digest(prepared.digest)
        }
        signature_request.prepared_content = prepared.content
        signature_request.timeout = timezone.now() + datetime.timedelta(minutes=2)

    def poll_signature(self, signature_request):
        # Confirmed right away
        digest = pdf.deserialize_digest(signature_request.provider_data["digest"])
        signature = async_to_sync(_signer().async_sign)(
            data_digest=digest.document_digest,
            digest_algorithm=pdf.DIGEST_ALGORITHM,
            use_pades=True,
        ).dump()
        store_signed_file(
            signature_request.file,
            content=pdf.finish(signature_request.prepared_content, digest, signature),
            signature=signature,
            signature_type=signature_request.signature_type,
            user=signature_request.created_by_user,
            group=signature_request.created_by_group,
            signature_request=signature_request,
        )

    def cancel_signature(self, signature_request):
        signature_request.status = SignatureRequest.Status.TIMEOUT
        signature_request.prepared_content = None

    def stamp(self, file, user, group, data):
        """Timestamp locally, with the visible stamp if `data` contains one."""
        signer = _signer()
        timestamper = DummyTimeStamper(
            tsa_cert=signer.signing_cert,
            tsa_key=signer.signing_key,
            certs_to_embed=SimpleCertificateStore.from_certs([signer.signing_cert]),
        )
        tokens = []

        def request_token(digest: bytes) -> bytes:
            tokens.append(
                async_to_sync(timestamper.async_timestamp)(
                    digest, pdf.DIGEST_ALGORITHM
                ).dump()
            )
            return tokens[-1]

        appearance = None
        if data.get("image") or data.get("text"):
            appearance = pdf.StampAppearance(
                box=STAMP_BOX,
                image=data.get("image"),
                text=data.get("text"),
            )

        with file.content.open() as content:
            stamped = pdf.timestamp(
                content.read(),
                bytes_reserved=BYTES_RESERVED,
                request_token=request_token,
                appearance=appearance,
            )

        return store_signed_file(
            file,
            content=stamped,
            signature=tokens[-1],
            signature_type=Signature.Type.TIMESTAMP,
            user=user,
            group=group,
        )
