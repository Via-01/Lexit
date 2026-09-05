# cleaners.py
"""Text cleaning utilities for Lexit."""

import unicodedata

import regex

# HTML tags are replaced with a space so adjacent text is not merged.
_HTML_TAG_PATTERN = regex.compile(r"<[^>]*>")

# Unicode symbols, including emoji and decorative symbols.
_SYMBOL_PATTERN = regex.compile(r"\p{S}")

# Unicode punctuation.
_PUNCTUATION_PATTERN = regex.compile(r"\p{P}")

# Runs of whitespace.
_WHITESPACE_PATTERN = regex.compile(r"\s+")

# Sentence-boundary punctuation.
_SENTENCE_PUNCTUATION = {".", "?", "!"}

# Punctuation commonly used inside technical or compound tokens.
_TECHNICAL_PUNCTUATION = {".", "+", "#"}


def normalize_unicode(text: str) -> str:
    """Normalize text using Unicode NFC normalization."""
    return unicodedata.normalize("NFC", text)


def remove_html(text: str) -> str:
    """Remove HTML tags while preserving surrounding text."""
    return _HTML_TAG_PATTERN.sub(" ", text)


def remove_extracted(
    text: str,
    urls: list[str],
    emails: list[str],
) -> str:
    """Remove previously extracted URLs and email addresses from text."""
    for value in [*urls, *emails]:
        text = text.replace(value, " ")

    return text


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace and strip surrounding whitespace."""
    return _WHITESPACE_PATTERN.sub(" ", text).strip()


def lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def _is_technical_token(token: str) -> bool:
    """
    Determine whether a token contains meaningful technical punctuation.

    Technical punctuation is preserved for tokens such as:

        C++
        C#
        .NET
        Node.js
        state-of-the-art
        COVID-19
        3.14

    Ordinary punctuation surrounding normal words is not considered
    technical punctuation.
    """
    if not token:
        return False

    # C++ / C#
    if token.startswith("C") and any(char in token for char in {"+", "#"}):
        return True

    # .NET-style tokens.
    if token.startswith(".") and len(token) > 1 and token[1].isalnum():
        return True

    # Tokens containing punctuation between alphanumeric characters.
    for index in range(1, len(token) - 1):
        if (
            token[index] in _TECHNICAL_PUNCTUATION
            and token[index - 1].isalnum()
            and token[index + 1].isalnum()
        ):
            return True

    # Hyphenated tokens such as COVID-19 and state-of-the-art.
    if "-" in token:
        parts = token.split("-")
        if all(part and any(char.isalnum() for char in part) for part in parts):
            return True

    return False


def _is_meaningful_edge_punctuation(token: str, index: int) -> bool:
    """
    Determine whether token[index] is technical punctuation that is
    actually doing meaningful work at that position, as opposed to
    incidental punctuation (e.g. a trailing sentence period) that
    merely shares a character with a technical pattern elsewhere.

    This mirrors the patterns recognized by _is_technical_token, but
    is evaluated per-character/per-position so that, e.g., the
    trailing "." in "Node.js." is not protected just because the
    token also contains the meaningful "." in "Node.js".
    """
    char = token[index]

    if char not in _TECHNICAL_PUNCTUATION:
        return False

    # Punctuation embedded between two alphanumeric characters,
    # e.g. the "." in "Node.js" or "3.14".
    if 0 < index < len(token) - 1:
        if token[index - 1].isalnum() and token[index + 1].isalnum():
            return True

    # C++ / C# style trailing technical punctuation.
    if char in {"+", "#"} and token[:index].rstrip("+#") == "C":
        return True

    # .NET-style leading punctuation.
    if char == "." and index == 0 and len(token) > 1 and token[1].isalnum():
        return True

    return False


def clean_punctuation(
    text: str,
    preserve_sentence_boundaries: bool = False,
) -> str:
    """
    Remove punctuation that does not contribute to token meaning.

    Punctuation used as part of a technical or compound token is
    preserved. Sentence-boundary punctuation can optionally be
    preserved for sentence tokenization.
    """
    cleaned_tokens: list[str] = []

    for token in text.split():
        start = 0
        end = len(token)

        while start < end:
            char = token[start]

            if preserve_sentence_boundaries and char in _SENTENCE_PUNCTUATION:
                break

            if _is_meaningful_edge_punctuation(token, start):
                break

            if not _PUNCTUATION_PATTERN.fullmatch(char):
                break

            start += 1

        while end > start:
            char = token[end - 1]

            if preserve_sentence_boundaries and char in _SENTENCE_PUNCTUATION:
                break

            if _is_meaningful_edge_punctuation(token, end - 1):
                break

            if not _PUNCTUATION_PATTERN.fullmatch(char):
                break

            end -= 1

        cleaned_tokens.append(token[start:end])

    return " ".join(token for token in cleaned_tokens if token)


def remove_symbols(text: str) -> str:
    """
    Remove Unicode symbols while preserving '+' in technical tokens.
    """
    cleaned_tokens: list[str] = []

    for token in text.split():
        technical_token = _is_technical_token(token)
        cleaned_token: list[str] = []

        for char in token:
            if not _SYMBOL_PATTERN.fullmatch(char):
                cleaned_token.append(char)
                continue

            if technical_token and char == "+":
                cleaned_token.append(char)

        cleaned_tokens.append("".join(cleaned_token))

    return " ".join(cleaned_tokens)


def clean_text(
    text: str,
    urls: list[str],
    emails: list[str],
    preserve_sentence_boundaries: bool = False,
) -> str:
    """
    Run the complete Lexit text-cleaning pipeline.

    The preserve_sentence_boundaries option is an internal mechanism
    used when sentence tokenization needs '.', '?' and '!' to remain
    available as sentence boundaries.
    """
    text = normalize_unicode(text)
    text = remove_extracted(text, urls, emails)
    text = remove_html(text)
    text = remove_symbols(text)
    text = clean_punctuation(
        text,
        preserve_sentence_boundaries=preserve_sentence_boundaries,
    )
    text = lowercase(text)
    text = normalize_whitespace(text)

    return text
