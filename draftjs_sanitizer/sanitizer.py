from logging import Logger
from typing import Dict, Iterable, Optional

from urllib3.util import parse_url

from .definitions import (
    BLACKLISTED_CHARS,
    BLACKLISTED_URL_SCHEMES,
    ENTITIES_HAVING_URLS,
)


class DraftJSSanitizer:
    def __init__(
        self,
        blacklisted_chars: Iterable = BLACKLISTED_CHARS,
        blacklisted_url_schemes: Iterable = BLACKLISTED_URL_SCHEMES,
        entities_having_url: Dict[str, Iterable] = ENTITIES_HAVING_URLS,
        logger: Optional[Logger] = None,
    ):
        """
        :param blacklisted_chars:
            The characters that should be encoded instead of being raw.
            This is only useful for dumping/encoding.

        :param blacklisted_url_schemes:
            The URL schemes to blacklist.

        :param entities_having_url:
            The different entity types that should be checked for having URL.
            To this, you can assign the list of attributes to check.
            E.g. for a `LINK`, you would pass `url` and `value` as attributes
                 to be checked for invalid URLs: `{"LINK": ("url", "value")}`

        :param logger:
            A logger if you want to log invalid inputs.
            By default, nothing is logged.
        """
        self.blacklisted_chars = blacklisted_chars
        self.blacklisted_url_schemes = blacklisted_url_schemes
        self.entities_having_url = entities_having_url
        self.logger = logger

    def warn(self, message, *args, **kwargs):
        if self.logger is not None:
            self.logger.warning(message, *args, **kwargs)

    def check_url_is_allowed(self, value: str) -> str:
        """Check if a given URL is allowed or not and return the cleaned URL,
        e.g. fixed a mal-encoded URL.

        By default, only the protocol ``javascript`` is denied.
        Other protocols are allowed (HTTP(S), FTP, inline data (images, files, ...), ..)

        Fragments are allowed as well (``#my-content``).

        Query-strings and relative/absolute paths are allowed.

        :returns: The cleaned URL.
        :raises ValueError: If the URL is invalid or blacklisted.
        """

        url = parse_url(value.strip())

        if url.scheme in self.blacklisted_url_schemes:
            raise ValueError(f"Scheme: {url.scheme} is blacklisted")

        return url.url

    def clean_draft_js_entity_url(self, entity):
        """Cleans and removes any invalid URLs passed into a draftjs entity."""

        entity_data = entity.get("data", None)
        if not entity_data or not isinstance(entity_data, dict):
            return

        for attr in self.entities_having_url[entity["type"]]:
            # Skip the attribute if there is no such attribute
            # inside the entity
            if attr not in entity_data:
                continue

            original_url = entity_data[attr]

            # Cleanup or remove the URL is disallowed
            try:
                new_url = self.check_url_is_allowed(entity_data[attr])
            except ValueError as exc:
                self.warn(f"An invalid url was sent: {original_url} -- {exc}")
                new_url = "#invalid"

            entity_data[attr] = new_url

    def clean_draft_js_entities(self, content: dict) -> None:
        """Clean all draftjs entities from malicious data."""
        entity_map = content.get("entityMap", None)

        if not entity_map or not isinstance(entity_map, dict):
            return

        for entity in entity_map.values():

            # Ignore if the entity is invalid
            if not isinstance(entity, dict):
                continue

            entity_type = entity.get("type", None)
            if entity_type in self.entities_having_url:
                self.clean_draft_js_entity_url(entity)

    def sanitize(self, value: dict):
        self.clean_draft_js_entities(value)
        return value

    def dump(self, value: dict) -> str:
        raise NotImplementedError