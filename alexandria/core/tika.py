from io import IOBase
from logging import getLogger

import requests
from django.conf import settings
from requests.exceptions import HTTPError

log = getLogger(__name__)


class TikaClient:
    """Class to handle all requests to Apache Tika."""

    @classmethod
    def get_content_from_buffer(cls, buffer: IOBase) -> str | None:
        """Get the text content of a buffer (in-memory file) from Tika.

        This will only return the "X-TIKA:content" property ignoring all other
        properties and metadata.

        Uses the tika/text resource:
        https://cwiki.apache.org/confluence/display/TIKA/TikaServer#TikaServer-TikaResource
        """

        try:
            response = requests.put(
                f"{settings.TIKA_SERVER_URL}/tika/text",
                data=buffer,
                # Tika has an internal time limit of 300s, we set the request
                # limit to match that.
                # Different values should be set in Tika as well:
                # https://github.com/CogStack/tika-service/blob/master/README.md#tika-parsers-configuration
                timeout=300,
                verify=False,
                headers={"Accept": "application/json"},
            )

            response.raise_for_status()

            result = response.json()
            content = result.get("X-TIKA:content", None) if result else None

            return content.strip() if content else None
        except HTTPError as e:  # pragma: no cover
            log.warning(f"Tika failed with error: {str(e)}")

            return None

    @classmethod
    def get_language_from_content(cls, content: str) -> str | None:
        """Get the language of a string from Tika.

        Normally, the passed `content` should be the result of calling
        `get_content_from_buffer` with the affected file.

        Uses the language/string resource:
        https://cwiki.apache.org/confluence/display/TIKA/TikaServer#TikaServer-LanguageResource
        """

        try:
            response = requests.put(
                f"{settings.TIKA_SERVER_URL}/language/string",
                data=content,
                timeout=60,
                verify=False,
                headers={"Accept": "text/plain"},
            )

            response.raise_for_status()

            return response.text.strip()
        except HTTPError as e:  # pragma: no cover
            log.warning(f"Tika failed with error: {str(e)}")

            return None
