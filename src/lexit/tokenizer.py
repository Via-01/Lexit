# tokenizer.py
"""Tokenization utilities for Lexit."""

import regex

_SENTENCE_BOUNDARY_CHARS = {".", "?", "!"}
_WHITESPACE_PATTERN = regex.compile(r"\s+")


def tokenize_word(text: str) -> list[str]:
    """Tokenize text using whitespace boundaries."""
    if not text:
        return []

    return text.split()


def _is_sentence_boundary(text: str, index: int) -> bool:
    """
    Determine whether text[index] is a real sentence boundary.

    A boundary character embedded between two alphanumeric
    characters (e.g. the "." in "Node.js" or "3.14") is part of a
    technical/compound token rather than a sentence boundary, and
    is therefore not treated as one.
    """
    if text[index] not in _SENTENCE_BOUNDARY_CHARS:
        return False

    prev_alnum = index > 0 and text[index - 1].isalnum()
    next_alnum = index + 1 < len(text) and text[index + 1].isalnum()

    return not (prev_alnum and next_alnum)


def tokenize_sentence(text: str) -> list[str]:
    """Tokenize text using '.', '?' and '!' as sentence boundaries.

    Boundary characters embedded inside a technical or compound
    token (e.g. "Node.js", "3.14") do not split the sentence.
    """
    if not text:
        return []

    sentences: list[str] = []
    current: list[str] = []

    for index, char in enumerate(text):
        if _is_sentence_boundary(text, index):
            sentence = _WHITESPACE_PATTERN.sub(" ", "".join(current)).strip()
            if sentence:
                sentences.append(sentence)
            current = []
        else:
            current.append(char)

    sentence = _WHITESPACE_PATTERN.sub(" ", "".join(current)).strip()
    if sentence:
        sentences.append(sentence)

    return sentences


def tokenize_character(text: str) -> list[str]:
    """Tokenize text into individual characters, including spaces."""
    if not text:
        return []

    return list(text)


def tokenize(
    text: str,
    method: str = "word",
) -> list[str]:
    """
    Tokenize cleaned text using the requested strategy.

    Args:
        text: Text to tokenize.
        method: Tokenization strategy: "word", "sentence", or "character".

    Returns:
        A list of tokens.

    Raises:
        ValueError: If an unsupported tokenization method is provided.
    """
    if method == "word":
        return tokenize_word(text)

    if method == "sentence":
        return tokenize_sentence(text)

    if method == "character":
        return tokenize_character(text)

    raise ValueError("tokenization must be one of: word, sentence, character")
