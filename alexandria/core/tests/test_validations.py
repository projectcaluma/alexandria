import io

import pytest
from clamdpy.models import ScanResult
from django.urls import reverse
from rest_framework import status

from alexandria.core import validations


def test_validate_mime_type(db, category_factory):
    category = category_factory(allowed_mime_types=["image/png"])
    mime_type = "image/png"
    assert validations.validate_mime_type(mime_type, category) is True

    mime_type = "image/jpeg"
    with pytest.raises(validations.ValidationError):
        validations.validate_mime_type(mime_type, category)


def test_validate_file_infection(db, mocker, settings, file):
    settings.ALEXANDRIA_CLAMD_ENABLED = True

    assert validations.validate_file_infection(None) is None

    mocker.patch(
        "clamdpy.ClamdNetworkSocket.instream",
        return_value=ScanResult(status="OK", reason="", path=None),
    )
    assert validations.validate_file_infection(file.content) is None


@pytest.mark.parametrize(
    "scan_result,error_code,error_message",
    [
        (
            ScanResult(status="ERROR", reason="reason", path=None),
            "incomplete",
            "Malware scan had an error: reason",
        ),
        (
            ScanResult(status="FOUND", reason="", path=None),
            "infected",
            "File is infected with malware.",
        ),
    ],
)
def test_validate_file_infection_infected(
    db, mocker, settings, file, scan_result, error_code, error_message
):
    settings.ALEXANDRIA_CLAMD_ENABLED = True
    mocker.patch(
        "clamdpy.ClamdNetworkSocket.instream",
        return_value=scan_result,
    )

    with pytest.raises(validations.ValidationError) as exc_info:
        validations.validate_file_infection(file.content)
    exc = exc_info.value.get_full_details()[0]
    assert exc["code"] == error_code
    assert exc["message"] == error_message


@pytest.mark.parametrize(
    "expected_error, expected_status, pdf_content",
    [
        pytest.param(
            None,
            status.HTTP_201_CREATED,
            (
                b"%PDF-1.7\n"
                b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
                b"xref\n0 3\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n"
                b"trailer\n<< /Size 3 /Root 1 0 R >>\n"
                b"startxref\n111\n%%EOF"
            ),
            id="pdf17",
        ),
        pytest.param(
            "PDF version 1.4 is not allowed. The minimum required PDF version is 1.6",
            status.HTTP_400_BAD_REQUEST,
            (
                b"%PDF-1.4\n"
                b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
                b"xref\n0 3\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n"
                b"trailer\n<< /Size 3 /Root 1 0 R >>\n"
                b"startxref\n111\n%%EOF"
            ),
            id="pdf14",
        ),
        pytest.param(
            "Invalid PDF header: %invalid",
            status.HTTP_400_BAD_REQUEST,
            (
                b"%invalid-1.4\n"
                b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
                b"xref\n0 3\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n"
                b"trailer\n<< /Size 3 /Root 1 0 R >>\n"
                b"startxref\n111\n%%EOF"
            ),
            id="invalid_pdf",
        ),
    ],
)
def test_validate_pdf_version(
    db,
    expected_error,
    expected_status,
    pdf_content,
    admin_client,
    settings,
    document_factory,
):
    settings.ALEXANDRIA_MIN_PDF_VERSION = 1.6
    doc = document_factory()

    content = io.BytesIO(pdf_content)
    content.name = "test.pdf"
    content.content_type = "application/pdf"

    data = {"name": "test.pdf", "document": str(doc.pk), "content": content}
    url = reverse("file-list")
    resp = admin_client.post(url, data=data, format="multipart")

    assert resp.status_code == expected_status

    if expected_error:
        json = resp.json()
        assert json["errors"][0]["detail"] == expected_error
