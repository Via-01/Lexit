# extractors.py
"""Utilities for extracting URLs and email addresses from text."""

import regex

# URLs must explicitly begin with http://, https://, or www.
_URL_PATTERN = regex.compile(r"(?<!\S)(?:https?://|www\.)[^\s]+")

# Standard email-address pattern.
_EMAIL_PATTERN = regex.compile(
    r"(?<![\w.+-])"
    r"[\w.!#$%&'*+/=?^`{|}~-]+"
    r"@"
    r"[\w](?:[\w-]{0,61}[\w])?"
    r"(?:\.[\w](?:[\w-]{0,61}[\w])?)+"
)

# Punctuation that commonly appears after a URL as sentence/phrase punctuation.
_TRAILING_URL_PUNCTUATION = ".,!?;:"


def extract_urls(text: str) -> list[str]:
    """Extract HTTP, HTTPS, and www URLs from text."""
    urls = []

    for match in _URL_PATTERN.finditer(text):
        url = match.group()

        # Remove punctuation that is clearly acting as sentence/phrase
        # punctuation at the end of the URL.
        url = url.rstrip(_TRAILING_URL_PUNCTUATION)

        if url:
            urls.append(url)

    return urls


def extract_emails(text: str) -> list[str]:
    """Extract standard email addresses from text."""
    emails = _EMAIL_PATTERN.findall(text)

    return [email.rstrip(".,!?;:") for email in emails]
