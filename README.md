# Lexit

**Lexit** is a lightweight, reusable, language- and model-agnostic Python text preprocessing package. It handles the common, repetitive text-cleaning and tokenization work that typically precedes an NLP or machine-learning pipeline, so you don't have to rewrite it for every project.

> Lexit prepares text. The downstream application decides what to do with it.

Lexit does not vectorize, embed, classify, or otherwise interpret text. It does one job — cleaning and tokenizing — and does it predictably.

---

## Why Lexit

- **Simple.** One function, one pipeline, one return shape. No configuration sprawl.
- **Robust.** Empty strings, non-text input, HTML, emoji, and multilingual text are all handled without raising unexpected exceptions.
- **Reusable.** The same preprocessing step works whether the output feeds a classifier, a search index, an embedding model, or a regex pipeline of your own.
- **Predictable.** The same input and options always produce the same output.
- **Dependency-minimal.** One runtime dependency ([`regex`](https://pypi.org/project/regex/)), used for reliable Unicode-aware pattern matching.

## Installation

```bash
pip install lexit-text
```

Or, with [uv](https://github.com/astral-sh/uv):

```bash
uv add lexit-text
```

Requires Python 3.10+.

## Quick start

```python
from lexit import process_text

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

There is exactly one pipeline. Lexit does not offer alternate cleaning "modes" — only a choice of tokenization strategy (see below). See [`docs/Final-Specification.md`](docs/Final-Specification.md) for the full behavioral contract, including edge cases.

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

Lexit removes punctuation that's acting as a separator, and preserves punctuation that's structurally part of a token:

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

The same applies if valid input becomes empty after cleaning (e.g. `"!!! 😀 @@@"`). Lexit never raises just because no usable text remains.

Non-string input raises `TypeError` rather than being silently coerced with `str()`:

```python
process_text(123)  # TypeError
```

## What Lexit is not

Lexit deliberately stops before any task-specific NLP/ML step. It does not provide:

- Vectorization (TF-IDF, count vectors, embeddings)
- Model training or inference
- Classification, sentiment analysis, or NER
- Language detection or translation
- An API/server layer

Take Lexit's output and hand it to whatever tool — scikit-learn, spaCy, a transformer, your own code — actually needs to do that work.

## Language support

Lexit is **Unicode-correct and works across space-delimited languages** — it does not target English specifically, and it does not attempt to be universal across every writing system either.

Concretely:

- **Unicode handling is correct everywhere.** NFC normalization, punctuation detection, and symbol/emoji detection are all based on Unicode character categories (`\p{P}`, `\p{S}`), not ASCII assumptions or hardcoded character lists. Accented Latin script, Cyrillic, Greek, Arabic, Hebrew, and Indic scripts all normalize and clean correctly.
- **Word tokenization relies on whitespace.** `process_text` splits on spaces to find word boundaries, because that's how the large majority of the world's written languages mark them.

That means:

| Language family | Works correctly? |
|---|---|
| English and other Latin-script languages | ✅ |
| French, German, Spanish, Portuguese, etc. (accents, ß, etc.) | ✅ |
| Russian, Ukrainian, Bulgarian, etc. (Cyrillic) | ✅ |
| Arabic, Urdu, Hebrew, Persian (RTL, space-delimited) | ✅ |
| Hindi, Bengali, Tamil, Telugu, Gujarati, Punjabi, Malayalam, Kannada, and other Indic languages | ✅ |
| Korean | ✅ (Korean orthography uses spaces between words, unlike Chinese/Japanese) |
| Vietnamese (Latin script) | ✅ |
| **Chinese, Japanese** | ❌ Not correctly. These languages don't use spaces between words, so word tokenization returns a whole sentence as a single token, and punctuation embedded inside that token is not removed. Sentence tokenization also doesn't work: it looks for the ASCII characters `.`, `!`, `?`, but Chinese and Japanese sentence-ending punctuation (`。`, `！`, `？`) are different, full-width Unicode characters that are never matched. Character tokenization does split correctly (it doesn't need spaces), but it inherits the punctuation issue: since punctuation-stripping only trims token *edges*, and the whole sentence is one token, embedded punctuation marks come through as their own tokens alongside the individual characters. |
| **Thai, Lao, Khmer, Myanmar** | ❌ Not correctly, for the same lack-of-spacing reason as above. |

If your text is primarily Chinese, Japanese, Thai, or another script without inter-word spacing, you'll need a dedicated word segmenter for that language (e.g. `jieba` for Chinese, `fugashi`/`MeCab` for Japanese, `pythainlp` for Thai) as a preprocessing step before or instead of Lexit's tokenization. Lexit's other cleaning steps (Unicode normalization, HTML/URL/email handling) still apply correctly to text in these languages — it's specifically word- and sentence-boundary detection that don't.

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
cd lexit
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

## Licensing and Disclaimer

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

You are free to use, modify, and distribute this code, but any modified version — including one deployed as a network service — must also be released under AGPL-3.0 with its source made available.

See the [LICENSE](./LICENSE) file for the full license text.

## Author

Vaishnavi Bhan