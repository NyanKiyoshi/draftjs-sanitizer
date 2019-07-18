import pytest

from draftjs_sanitizer import clean_draft_js


@pytest.mark.parametrize("url", ("javascript:alert();",))
def test_malicious_urls(url):
    json_data = {
        "entityMap": {
            "0": {"data": {"url": url}, "type": "LINK", "mutability": "MUTABLE"}
        }
    }

    clean_draft_js(json_data)
    assert json_data == {
        "entityMap": {
            "0": {"data": {"url": "#invalid"}, "type": "LINK", "mutability": "MUTABLE"}
        }
    }


def test_malicious_url_image():
    json_data = {
        "entityMap": {
            "0": {
                "data": {"src": "javascript:alert();"},
                "type": "IMAGE",
                "mutability": "MUTABLE",
            }
        }
    }

    clean_draft_js(json_data)
    assert json_data == {
        "entityMap": {
            "0": {"data": {"src": "#invalid"}, "type": "IMAGE", "mutability": "MUTABLE"}
        }
    }
