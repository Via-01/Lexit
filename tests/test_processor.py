# test_processor.py
"""Integration tests for the Lexit processing pipeline."""

import pytest

from lexit import process_text


def test_process_text_defaults_to_word_tokenization() -> None:
    result = process_text("Hello, world!")

    assert result["original_text"] == "Hello, world!"
    assert result["cleaned_text"] == "hello world"
    assert result["tokens"] == ["hello", "world"]


def test_process_text_extracts_urls_and_emails() -> None:
    text = "Visit https://example.com or www.example.org. Contact hello@example.com."

    result = process_text(text)

    assert result["urls"] == [
        "https://example.com",
        "www.example.org",
    ]

    assert result["emails"] == ["hello@example.com"]

    assert result["cleaned_text"] == "visit or contact"


def test_process_text_sentence_tokenization() -> None:
    text = "Hello world. How are you? I am fine!"

    result = process_text(
        text,
        tokenization="sentence",
    )

    assert result["cleaned_text"] == "hello world how are you i am fine"

    assert result["tokens"] == [
        "hello world",
        "how are you",
        "i am fine",
    ]


def test_process_text_character_tokenization() -> None:
    result = process_text(
        "Hello!",
        tokenization="character",
    )

    assert result["cleaned_text"] == "hello"
    assert result["tokens"] == ["h", "e", "l", "l", "o"]


def test_process_text_preserves_meaningful_punctuation() -> None:
    result = process_text("COVID-19 affects C++ and C# developers using Node.js.")

    assert result["cleaned_text"] == (
        "covid-19 affects c++ and c# developers using node.js"
    )


def test_process_text_metadata() -> None:
    text = "Hello, world!"

    result = process_text(text)

    assert result["metadata"] == {
        "original_length": len(text),
        "cleaned_length": len("hello world"),
        "token_count": 2,
    }


def test_process_empty_text() -> None:
    result = process_text("")

    assert result == {
        "original_text": "",
        "cleaned_text": "",
        "tokens": [],
        "emails": [],
        "urls": [],
        "metadata": {
            "original_length": 0,
            "cleaned_length": 0,
            "token_count": 0,
        },
    }


def test_process_text_requires_string() -> None:
    with pytest.raises(TypeError):
        process_text(123)  # type: ignore[arg-type]


def test_process_text_rejects_invalid_tokenization() -> None:
    with pytest.raises(ValueError):
        process_text("hello", tokenization="paragraph")
