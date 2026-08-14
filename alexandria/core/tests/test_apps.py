import mimetypes

import pytest

from alexandria.core.apps import register_custom_mime_types


@pytest.fixture
def custom_mime_types(settings):
    original = settings.ALEXANDRIA_CUSTOM_MIME_TYPES
    settings.ALEXANDRIA_CUSTOM_MIME_TYPES = {"text/plain": ["ili", "itf"]}
    register_custom_mime_types()

    yield

    settings.ALEXANDRIA_CUSTOM_MIME_TYPES = original
    register_custom_mime_types()


def test_custom_mime_types_registered_on_startup():
    # `.msg` is not known by the `mimetypes` module and is only detectable
    # because it is registered by the app config on startup.
    assert mimetypes.guess_type("mail.msg", strict=False) == (
        "application/vnd.ms-outlook",
        None,
    )


def test_register_custom_mime_types(custom_mime_types):
    # If strict is `True` (default) the types are not detected
    assert mimetypes.guess_type("data.ili") == (None, None)
    assert mimetypes.guess_type("data.itf") == (None, None)

    # If strict is `False` they are detected
    assert mimetypes.guess_type("data.ili", strict=False) == ("text/plain", None)
    assert mimetypes.guess_type("data.itf", strict=False) == ("text/plain", None)

    # types that are not configured anymore are not detected
    assert mimetypes.guess_type("mail.msg") == (None, None)

    # well known types are still detected
    assert mimetypes.guess_type("data.txt") == ("text/plain", None)
