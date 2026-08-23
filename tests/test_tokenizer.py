# test_tokenizer.py
"""Tests for Lexis tokenization."""

import pytest

from lexis.tokenizer import (
    tokenize,
    tokenize_character,
    tokenize_sentence,
    tokenize_word,
)


def test_word_tokenization() -> None:
    assert tokenize_word("hello world again") == [
        "hello",
        "world",
        "again",
    ]


def test_word_tokenization_uses_whitespace() -> None:
    text = "hello    world\nagain"

    assert tokenize_word(text) == [
        "hello",
        "world",
        "again",
    ]


def test_sentence_tokenization() -> None:
    text = "Hello. How are you? I am fine!"

    assert tokenize_sentence(text) == [
        "Hello",
        "How are you",
        "I am fine",
    ]


def test_sentence_tokenization_supports_all_boundaries() -> None:
    text = "First. Second? Third!"

    assert tokenize_sentence(text) == [
        "First",
        "Second",
        "Third",
    ]


def test_sentence_tokenization_empty_text() -> None:
    assert tokenize_sentence("") == []


def test_word_tokenization_empty_text() -> None:
    assert tokenize_word("") == []


def test_character_tokenization() -> None:
    assert tokenize_character("hello") == [
        "h",
        "e",
        "l",
        "l",
        "o",
    ]


def test_character_tokenization_preserves_spaces() -> None:
    assert tokenize_character("hello world") == list("hello world")


def test_character_tokenization_empty_text() -> None:
    assert tokenize_character("") == []


def test_tokenize_defaults_to_word() -> None:
    assert tokenize("hello world") == ["hello", "world"]


def test_tokenize_word() -> None:
    assert tokenize("hello world", method="word") == [
        "hello",
        "world",
    ]


def test_tokenize_sentence() -> None:
    assert tokenize(
        "Hello. How are you?",
        method="sentence",
    ) == [
        "Hello",
        "How are you",
    ]


def test_tokenize_character() -> None:
    assert tokenize("hello", method="character") == list("hello")


def test_invalid_tokenization_method() -> None:
    with pytest.raises(ValueError):
        tokenize("hello world", method="paragraph")
