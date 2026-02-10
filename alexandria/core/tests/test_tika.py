import pytest

from alexandria.core.tika import TikaClient


@pytest.mark.no_mock_tika
@pytest.mark.vcr
@pytest.mark.parametrize("filename", ["pdf-test-en.pdf", "pdf-test-de.pdf"])
def test_tika(snapshot, testfile, filename):
    with open(testfile(filename), "rb") as f:
        buffer = f.read()

        content = TikaClient.get_content_from_buffer(buffer)
        language = TikaClient.get_language_from_content(content)

    assert {"content": content, "language": language} == snapshot
