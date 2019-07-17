<div align='center'>
  <h1>DraftJS Sanitizer</h1>
  <p>Sanitizes a DraftJS JSON format from a dict to allow saving. Allows safe dumping into a string in order to prevent injection of quotes and HTML entities.</p>
  <p>
    <a href='https://travis-ci.org/NyanKiyoshi/draftjs-sanitizer/'>
      <img src='https://travis-ci.org/NyanKiyoshi/draftjs-sanitizer.svg?branch=master' alt='Build Status' />
    </a>
    <a href='https://codecov.io/gh/NyanKiyoshi/draftjs-sanitizer'>
      <img src='https://codecov.io/gh/NyanKiyoshi/draftjs-sanitizer/branch/master/graph/badge.svg' alt='Coverage Status' />
    </a>
    <a href='https://pypi.python.org/pypi/draftjs-sanitizer'>
      <img src='https://img.shields.io/pypi/v/draftjs-sanitizer.svg' alt='Version' />
    </a>
  </p>
  <p>
    <a href='https://pypi.python.org/pypi/draftjs-sanitizer'>
      <img src='https://img.shields.io/pypi/pyversions/draftjs-sanitizer.svg' alt='Supported versions' />
    </a>
    <a href='https://pypi.python.org/pypi/draftjs-sanitizer'>
      <img src='https://img.shields.io/pypi/implementation/draftjs-sanitizer.svg' alt='Supported implementations' />
    </a>
  </p>
</div>

## Installation
```
pip install draftjs-sanitizer
```

## Usage

### Remove known exploits
This removes any URLs that could be used for XSS attacks by linking raw javascript code.

```python
from draftjs_sanitizer import clean_draft_js


clean_draft_js({
    "blocks": [
        {
            "key": "an6ci",
            "data": {},
            "text": "Get Saleor today!",
            "type": "unstyled",
            "depth": 0,
            "entityRanges": [
                {
                    "key": 0,
                    "length": 17,
                    "offset": 0
                }
            ],
            "inlineStyleRanges": []
        }
    ],
    "entityMap": {
        "0": {
            "data": {
                "url": "javascript:alert('Oopsie!');"
            },
            "type": "LINK",
            "mutability": "MUTABLE"
        }
    }
})
```

### Dump JSON for HTML Usage
This allows to run it as a filter in order to prevent any injection or bypass when putting the JSON into HTML code.

```python
from draftjs_sanitizer import to_string

dumped_json = to_string({"block": "</div><script>alert('Oopsie!');</script>"})
```

#### Example 1: attribute bypass
```html
<div data-draft-js-json='{"block": "'<script>alert('Oopsie!');</script>"}'></div>
```

#### Example 2: bypass inner HTML
```html
<div>
    {"block": "</div><script>alert('Oopsie!');</script>"}
</div>
```

## Supported Checks

| Type | Entities | Description |
| ---- | -------- | ----------- |
| Javascript URL | `IMAGE`, `LINK` | Prevent injecting javascript through the `javascript` protocol into a URL. |
| Invalid URL | `IMAGE`, `LINK` | Removes any invalid URL from the JSON content. |
| Dangerous Characters | `any` | Removes any sensible character for HTML incorporation: `"`, `'`, `<`, `>`.


## Development
```
./setup.py develop
pip install -r requirements_dev.txt
```

You can easily extend the behaviors through:
- `draftjs_sanitizer.encoder.DraftJSSafeEncoder`
- `draftjs_sanitizer.sanitizer.DraftJSSanitizer`

## Dependencies
- `urllib3` for RFC 3986 parsing and validation of URLs.
