"""Main text-processing pipeline for Lexis."""

from typing import Any

from .cleaners import clean_text
from .extractors import extract_emails, extract_urls
from .tokenizer import tokenize

_SUPPORTED_TOKENIZATIONS = {"word", "sentence", "character"}


def process_text(
    text: str,
    tokenization: str = "word",
) -> dict[str, Any]:
    """
    Process text through the complete Lexis pipeline.

    Args:
        text: Input text to process.
        tokenization: Tokenization strategy. Supported values are
            "word", "sentence", and "character".

    Returns:
        A dictionary containing the original text, cleaned text,
        tokens, extracted emails, extracted URLs, and metadata.

    Raises:
        TypeError: If text is not a string.
        ValueError: If an unsupported tokenization strategy is provided.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if tokenization not in _SUPPORTED_TOKENIZATIONS:
        raise ValueError("tokenization must be one of: word, sentence, character")

    urls = extract_urls(text)
    emails = extract_emails(text)

    cleaned_text = clean_text(
        text,
        urls=urls,
        emails=emails,
    )

    if tokenization == "sentence":
        tokenization_text = clean_text(
            text,
            urls=urls,
            emails=emails,
            preserve_sentence_boundaries=True,
        )
    else:
        tokenization_text = cleaned_text

    tokens = tokenize(
        tokenization_text,
        method=tokenization,
    )

    return {
        "original_text": text,
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "emails": emails,
        "urls": urls,
        "metadata": {
            "original_length": len(text),
            "cleaned_length": len(cleaned_text),
            "token_count": len(tokens),
        },
    }
