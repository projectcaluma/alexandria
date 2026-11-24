import datetime

import pytest
from asgiref.sync import async_to_sync
from asn1crypto import keys, x509
from cryptography import x509 as crypto_x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from pyhanko.sign.signers.pdf_cms import SimpleSigner
from pyhanko.sign.timestamps.dummy_client import DummyTimeStamper
from pyhanko_certvalidator.registry import SimpleCertificateStore

from alexandria.esign import pdf


@pytest.fixture(autouse=True)
def schedule_cleanup(mocker):
    """Don't send the cleanup task to the broker."""
    return mocker.patch(
        "alexandria.esign.tasks.cancel_expired_signature_request.apply_async_on_commit"
    )


@pytest.fixture(scope="session")
def test_signer():
    """Self-signed signer standing in for the signature provider."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = crypto_x509.Name(
        [crypto_x509.NameAttribute(NameOID.COMMON_NAME, "Winston Smith")]
    )
    now = datetime.datetime.now(datetime.UTC)
    cert = (
        crypto_x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(crypto_x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=1))
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


@pytest.fixture
def sign_digest(test_signer):
    """Return the DER encoded CMS signature for a document digest."""

    def do(document_digest: bytes) -> bytes:
        return async_to_sync(test_signer.async_sign)(
            data_digest=document_digest,
            digest_algorithm=pdf.DIGEST_ALGORITHM,
            use_pades=True,
        ).dump()

    return do


@pytest.fixture
def pdf_content(testfile):
    return testfile("pdf-test-en.pdf").read_bytes()


@pytest.fixture
def timestamp_token(test_signer):
    """Return a DER encoded RFC 3161 timestamp token for a document digest."""
    timestamper = DummyTimeStamper(
        tsa_cert=test_signer.signing_cert,
        tsa_key=test_signer.signing_key,
        certs_to_embed=SimpleCertificateStore.from_certs([test_signer.signing_cert]),
    )

    def do(document_digest: bytes) -> bytes:
        return async_to_sync(timestamper.async_timestamp)(
            document_digest, pdf.DIGEST_ALGORITHM
        ).dump()

    return do
