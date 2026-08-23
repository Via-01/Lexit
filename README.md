# Lexis

**Lexis** is a lightweight, reusable, language- and model-agnostic Python text preprocessing package. It handles the common, repetitive text-cleaning and tokenization work that typically precedes an NLP or machine-learning pipeline, so you don't have to rewrite it for every project.

> Lexis prepares text. The downstream application decides what to do with it.

Lexis does not vectorize, embed, classify, or otherwise interpret text. It does one job — cleaning and tokenizing — and does it predictably.

---

## Why Lexis

- **Simple.** One function, one pipeline, one return shape. No configuration sprawl.
- **Robust.** Empty strings, non-text input, HTML, emoji, and multilingual text are all handled without raising unexpected exceptions.
- **Reusable.** The same preprocessing step works whether the output feeds a classifier, a search index, an embedding model, or a regex pipeline of your own.
- **Predictable.** The same input and options always produce the same output.
- **Dependency-minimal.** One runtime dependency ([`regex`](https://pypi.org/project/regex/)), used for reliable Unicode-aware pattern matching.

## Installation

```bash
pip install lexis-text
```

Or, with [uv](https://github.com/astral-sh/uv):

```bash
uv add lexis-text
```

Requires Python 3.10+.

## Quick start

```python
from lexis import process_text

result = process_text("Visit https://example.com or email hello@example.com! COVID-19 news 🚀.")
```

```python
{
    "original_text": "Visit https://example.com or email hello@example.com! COVID-19 news 🚀.",
    "cleaned_text": "visit or email covid-19 news",
    "tokens": ["visit", "or", "email", "covid-19", "news"],
    "emails": ["hello@example.com"],
    "urls": ["https://example.com"],
    "metadata": {
        "original_length": 70,
        "cleaned_length": 28,
        "token_count": 5
    }
}
```

Notice what happened in that one call:

- The URL and email address were pulled out into structured fields instead of being mangled by lowercasing/punctuation stripping.
- `COVID-19` kept its hyphen — punctuation that's structurally part of a token is preserved, not blindly stripped.
- The emoji was removed as decorative noise; the text was not.
- Whitespace was normalized and the text was lowercased and tokenized in one pass.

## What `process_text` does

Every call runs the same fixed pipeline:

1. Validate input
2. Extract URLs and email addresses (before anything destructive touches the text)
3. Normalize Unicode (NFC)
4. Remove the extracted URLs/emails, and any HTML markup, from the working text
5. Remove emojis and decorative symbols
6. Apply meaning-aware punctuation handling
7. Lowercase
8. Normalize whitespace
9. Tokenize
10. Return a dictionary with the cleaned text, tokens, extractions, and metadata

There is exactly one pipeline. Lexis does not offer alternate cleaning "modes" — only a choice of tokenization strategy (see below). See [`docs/Final-Specification.md`](docs/Final-Specification.md) for the full behavioral contract, including edge cases.

## Tokenization strategies

```python
process_text(text)                              # word (default)
process_text(text, tokenization="sentence")
process_text(text, tokenization="character")
```

| Mode | Behavior |
|---|---|
| `word` | Splits cleaned text on whitespace. `"Node.js"` stays one token. |
| `sentence` | Splits on `.`, `?`, `!` — but only when the character isn't embedded inside a technical token. `"Use Node.js. It's fast!"` → `["use node.js", "it's fast"]`, not three fragments. |
| `character` | Every character of the cleaned text, including spaces, as its own token. |

## Meaning-aware punctuation handling

Lexis removes punctuation that's acting as a separator, and preserves punctuation that's structurally part of a token:

```python
process_text("COVID-19, C++, and don't forget 3.14!")["cleaned_text"]
# "covid-19 c++ and don't forget 3.14"
```

The comma and exclamation point are gone. The hyphen, apostrophe, `++`, and decimal point are not — they change the meaning of the token they belong to.

This same logic applies consistently across cleaning, punctuation handling, and tokenization, so a technical token like `Node.js` behaves the same way whether it's in the middle of a sentence or at the very end of one.

## Numbers

Numbers are preserved, not treated as noise — `2026`, `19`, and `3.14` all remain in the cleaned text, since numeric information is frequently meaningful for downstream tasks.

## Empty and edge-case input

Empty input is valid and does not raise:

```python
process_text("")
```

```python
{
    "original_text": "",
    "cleaned_text": "",
    "tokens": [],
    "emails": [],
    "urls": [],
    "metadata": {"original_length": 0, "cleaned_length": 0, "token_count": 0}
}
```

The same applies if valid input becomes empty after cleaning (e.g. `"!!! 😀 @@@"`). Lexis never raises just because no usable text remains.

Non-string input raises `TypeError` rather than being silently coerced with `str()`:

```python
process_text(123)  # TypeError
```

## What Lexis is not

Lexis deliberately stops before any task-specific NLP/ML step. It does not provide:

- Vectorization (TF-IDF, count vectors, embeddings)
- Model training or inference
- Classification, sentiment analysis, or NER
- Language detection or translation
- An API/server layer

Take Lexis's output and hand it to whatever tool — scikit-learn, spaCy, a transformer, your own code — actually needs to do that work.

## Return format

Every successful call returns the same shape, regardless of tokenization mode:

```python
{
    "original_text": str,
    "cleaned_text": str,
    "tokens": list[str],
    "emails": list[str],
    "urls": list[str],
    "metadata": {
        "original_length": int,
        "cleaned_length": int,
        "token_count": int,
    },
}
```

## Development

```bash
git clone <repo-url>
cd lexis
uv sync --extra dev
```

Run the test suite:

```bash
uv run pytest
```

Lint and type-check:

```bash
uv run ruff check .
uv run mypy src
```

## Documentation

- [`docs/Final-Specification.md`](docs/Final-Specification.md) — the full behavioral contract: every rule, edge case, and example.
- [`docs/Final-Package-and-Dependencies.md`](docs/Final-Package-and-Dependencies.md) — project structure, module responsibilities, and dependency philosophy.

## License

MIT — see [`LICENSE`](LICENSE).

## Author

Vaishnavi Bhan