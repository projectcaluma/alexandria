import pytest
from clamdpy.models import ScanResult

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
