import json

import mock
import pytest

from draftjs_sanitizer import to_string


@mock.patch("draftjs_sanitizer.clean_draft_js")
def test_full_clean_does_not_have_side_effects(mocked_clean):
    """Checks that ``clean_draft_js()`` gets called with a copy
    of the passed dictionary"""

    json_dict = {}
    to_string(json_dict, full_clean=True)

    assert mocked_clean.call_count == 1
    assert mocked_clean.call_args.args == (json_dict,)
    assert mocked_clean.call_args.args[0] is not json_dict


@pytest.mark.parametrize(
    "json_data, expected_str",
    (
        (
            {"something": "'<script>...."},
            r'{"something": "\u0027\u003cscript\u003e...."}',
        ),
        (
            {"'<script>....\"": {"1": {"2": {"3": "<script>"}}}},
            r'{"\u0027\u003cscript\u003e....\"": '
            r'{"1": {"2": {"3": "\u003cscript\u003e"}}}}',
        ),
    ),
)
def test_encode_malicious_strings(json_data, expected_str):
    encoded = to_string(json_data)
    assert encoded == expected_str

    decoded = json.loads(encoded)
    assert decoded == json_data
