import pytest

from draftjs_sanitizer import clean_draft_js


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
