# test_extractors.py
"""Tests for Lexit URL and email extraction."""

from lexit.extractors import extract_emails, extract_urls


def test_extract_http_url() -> None:
    text = "Visit http://example.com for more information."

    assert extract_urls(text) == ["http://example.com"]


def test_extract_https_url() -> None:
    text = "Visit https://example.com for more information."

    assert extract_urls(text) == ["https://example.com"]


def test_extract_www_url() -> None:
    text = "Visit www.example.com for more information."

    assert extract_urls(text) == ["www.example.com"]


def test_bare_domain_is_not_extracted() -> None:
    text = "Visit example.com for more information."

    assert extract_urls(text) == []


def test_extract_url_with_path_and_query() -> None:
    text = "Visit https://example.com/path/to/page?q=hello&x=1."

    assert extract_urls(text) == ["https://example.com/path/to/page?q=hello&x=1"]


def test_remove_trailing_url_punctuation() -> None:
    text = "See https://example.com, https://example.org! https://example.net?"

    assert extract_urls(text) == [
        "https://example.com",
        "https://example.org",
        "https://example.net",
    ]


def test_preserve_internal_url_punctuation() -> None:
    text = "Visit https://example.com/path_(test)?q=hello!"

    assert extract_urls(text) == ["https://example.com/path_(test)?q=hello"]


def test_extract_multiple_urls() -> None:
    text = "Visit https://example.com and www.example.org."

    assert extract_urls(text) == [
        "https://example.com",
        "www.example.org",
    ]


def test_no_urls() -> None:
    text = "There are no links here."

    assert extract_urls(text) == []


def test_extract_standard_email() -> None:
    text = "Contact hello@example.com for help."

    assert extract_emails(text) == ["hello@example.com"]


def test_extract_multiple_emails() -> None:
    text = "Contact a@example.com or support@example.org."

    assert extract_emails(text) == [
        "a@example.com",
        "support@example.org",
    ]


def test_no_emails() -> None:
    text = "There are no email addresses here."

    assert extract_emails(text) == []
