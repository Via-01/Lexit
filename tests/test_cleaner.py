# test_cleaner.py
"""Tests for Lexis text cleaning."""

from lexis.cleaners import (
    clean_punctuation,
    clean_text,
    lowercase,
    normalize_unicode,
    normalize_whitespace,
    remove_extracted,
    remove_html,
    remove_symbols,
)


def test_unicode_normalization() -> None:
    text = "Cafe\u0301"

    assert normalize_unicode(text) == "Café"


def test_lowercase() -> None:
    assert lowercase("Hello WORLD") == "hello world"


def test_remove_html_tags() -> None:
    text = "<p>Hello <strong>world</strong></p>"

    assert remove_html(text) == " Hello  world  "


def test_remove_html_attributes() -> None:
    text = '<p class="important">Hello</p>'

    assert remove_html(text) == " Hello "


def test_preserve_text_inside_html() -> None:
    text = "<div>Hello <b>world</b></div>"

    assert remove_html(text) == " Hello  world  "


def test_remove_extracted_urls_and_emails() -> None:
    text = "Contact hello@example.com or visit https://example.com."

    result = remove_extracted(
        text,
        urls=["https://example.com"],
        emails=["hello@example.com"],
    )

    assert result == "Contact   or visit  ."


def test_normalize_whitespace() -> None:
    text = "  Hello    world\n\tagain  "

    assert normalize_whitespace(text) == "Hello world again"


def test_remove_sentence_punctuation() -> None:
    assert clean_punctuation("Hello! How are you? Fine.") == ("Hello How are you Fine")


def test_preserve_internal_punctuation() -> None:
    text = "COVID-19 3.14 don't state-of-the-art"

    assert clean_punctuation(text) == text


def test_preserve_technical_tokens() -> None:
    text = "C++ C# .NET Node.js"

    assert clean_punctuation(text) == text


def test_remove_boundary_punctuation() -> None:
    text = '"Hello," (world!) [test].'

    assert clean_punctuation(text) == "Hello world test"


def test_remove_symbols() -> None:
    text = "Hello 😀 world ™ ★"

    assert remove_symbols(text) == "Hello  world  "


def test_clean_text() -> None:
    text = (
        "<p>Hello, WORLD!</p> Visit https://example.com, or email TEST@example.com. 😀"
    )

    result = clean_text(
        text,
        urls=["https://example.com"],
        emails=["TEST@example.com"],
    )

    assert result == "hello world visit or email"


def test_clean_empty_text() -> None:
    assert clean_text("", urls=[], emails=[]) == ""
