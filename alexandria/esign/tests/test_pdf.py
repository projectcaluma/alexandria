from io import BytesIO

import pytest
from PIL import Image
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.diff_analysis import ModificationLevel
from pyhanko.sign.validation import validate_pdf_signature, validate_pdf_timestamp
from pyhanko_certvalidator import ValidationContext

from alexandria.esign import pdf

BYTES_RESERVED = 16384


def test_prepare_and_finish(pdf_content, sign_digest):
    prepared = pdf.prepare(pdf_content, bytes_reserved=BYTES_RESERVED)

    # State survives the round trip through the database
    digest = pdf.deserialize_digest(pdf.serialize_digest(prepared.digest))
    assert digest == prepared.digest

    signed = pdf.finish(prepared.content, digest, sign_digest(digest.document_digest))

    assert signed.startswith(pdf_content)
    embedded = pdf.last_signature(signed)
    assert embedded.signer_name == "Winston Smith"
    assert embedded.signed_at is not None


def test_prepare_adds_new_field_to_signed_pdf(pdf_content, sign_digest):
    first = pdf.prepare(pdf_content, bytes_reserved=BYTES_RESERVED)
    signed = pdf.finish(
        first.content, first.digest, sign_digest(first.digest.document_digest)
    )

    second = pdf.prepare(signed, bytes_reserved=BYTES_RESERVED)
    signed_twice = pdf.finish(
        second.content, second.digest, sign_digest(second.digest.document_digest)
    )

    assert signed_twice.startswith(signed)


def test_timestamp(pdf_content, sign_digest, timestamp_token, test_signer):
    signed_first = pdf.prepare(pdf_content, bytes_reserved=BYTES_RESERVED)
    signed = pdf.finish(
        signed_first.content,
        signed_first.digest,
        sign_digest(signed_first.digest.document_digest),
    )

    stamped = pdf.timestamp(
        signed, bytes_reserved=BYTES_RESERVED, request_token=timestamp_token
    )

    assert stamped.startswith(signed)
    reader = PdfFileReader(BytesIO(stamped))
    stamp = reader.embedded_signatures[-1]
    # A timestamp token must not be embedded as CMS signature
    assert stamp.sig_object_type == "/DocTimeStamp"
    assert stamp.sig_object["/SubFilter"] == "/ETSI.RFC3161"
    status = validate_pdf_timestamp(
        stamp,
        validation_context=ValidationContext(
            trust_roots=[test_signer.signing_cert], allow_fetching=False
        ),
    )
    assert status.intact and status.valid

    embedded = pdf.last_signature(stamped)
    assert embedded.signer_name == "Winston Smith"
    assert embedded.signed_at is not None


@pytest.fixture
def stamp_image():
    output = BytesIO()
    Image.new("RGBA", (60, 40), (0, 128, 0, 255)).save(output, format="PNG")
    return output.getvalue()


def test_visible_stamp_keeps_signatures_valid(
    pdf_content, sign_digest, timestamp_token, test_signer, stamp_image
):
    prepared = pdf.prepare(pdf_content, bytes_reserved=BYTES_RESERVED)
    signed = pdf.finish(
        prepared.content, prepared.digest, sign_digest(prepared.digest.document_digest)
    )

    stamped = pdf.timestamp(
        signed,
        bytes_reserved=BYTES_RESERVED,
        request_token=timestamp_token,
        appearance=pdf.StampAppearance(
            box=(400, 700, 560, 800), image=stamp_image, text="17.11.2026 100%"
        ),
    )

    reader = PdfFileReader(BytesIO(stamped))
    stamp = reader.embedded_signatures[-1]
    assert stamp.sig_object_type == "/DocTimeStamp"
    # Visible: the timestamp field has the stamp as appearance
    assert [float(v) for v in stamp.sig_field["/Rect"]] == [400, 700, 560, 800]
    assert "/N" in stamp.sig_field["/AP"]

    context = ValidationContext(
        trust_roots=[test_signer.signing_cert], allow_fetching=False
    )
    status = validate_pdf_signature(reader.embedded_signatures[0], context)
    # A new signature field is an allowed change after a signature
    assert status.intact and status.valid
    assert status.modification_level <= ModificationLevel.FORM_FILLING
    stamp_status = validate_pdf_timestamp(stamp, validation_context=context)
    assert stamp_status.intact and stamp_status.valid


def test_add_validation_info(pdf_content, test_signer):
    cert = test_signer.signing_cert.dump()

    result = pdf.add_validation_info(pdf_content, certs=[cert])

    assert result.startswith(pdf_content)
    dss = PdfFileReader(BytesIO(result)).root["/DSS"]
    assert len(dss["/Certs"]) == 1


def test_timestamp_certificates(timestamp_token, test_signer):
    token = timestamp_token(bytes(64))

    assert pdf.timestamp_certificates(token) == [test_signer.signing_cert.dump()]
