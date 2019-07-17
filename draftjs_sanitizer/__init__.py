from .encoder import DraftJSSafeEncoder
from .sanitizer import DraftJSSanitizer

__all__ = ["DraftJSSanitizer", "DraftJSSafeEncoder", "clean_draft_js", "to_string"]


def clean_draft_js(definitions: dict) -> dict:
    """Sanitize a given DraftJS JSON definitions for saving or exporting."""
    cls = DraftJSSanitizer()
    return cls.sanitize(definitions)


def to_string(definitions: dict, full_clean=False) -> str:
    """Sanitize risky characters from the definitions to allow putting the JSON safely
    into HTML code.

    :param full_clean: Whether all the checks should be ran instead of only checking for
        dangerous characters. Basically runs ``clean_draft_js`` before dumping.
    """