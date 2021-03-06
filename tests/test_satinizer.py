import pytest

from draftjs_sanitizer import DraftJSSanitizer, clean_draft_js


def test_returns_same_object():
    json_data = {}
    assert clean_draft_js(json_data) is json_data


@pytest.mark.parametrize(
    "json_data",
    (
        # Missing data attribute
        {"entityMap": {"0": {"type": "LINK", "mutability": "MUTABLE"}}},
        # Invalid data type
        {"entityMap": {"0": {"data": None, "mutability": "MUTABLE"}}},
        # Missing type attribute
        {"entityMap": {"0": {"data": {}, "mutability": "MUTABLE"}}},
        # Invalid entity map
        {"entityMap": None},
        # Empty map
        {},
    ),
)
def test_ignores_invalid_draftjs(json_data):
    base_data = json_data.copy()

    clean_draft_js(json_data)
    assert json_data == base_data


def test_dump():
    data = {"hello<>": ""}
    assert DraftJSSanitizer().dump(data) == r'{"hello\u003c\u003e": ""}'
