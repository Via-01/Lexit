# Lexis v1 — Final Behavioral Specification

## 1. Overview

**Lexis** is a lightweight, reusable, language- and model-agnostic Python text preprocessing package.

Its purpose is to handle the common, repetitive text-cleaning and tokenization work that is typically required before text is passed into an NLP or machine-learning pipeline.

Lexis is intentionally **simple, robust, and focused**.

It does **not** attempt to replace NLP frameworks or provide downstream NLP/ML functionality.

### Core principle

> **Lexis prepares text. The downstream application decides what to do with it.**

Lexis therefore does not perform vectorization, embeddings, model training, sentiment analysis, or other task-specific processing.

---

# 2. Scope

Lexis v1 provides:

* Text validation
* Unicode normalization
* Case normalization
* HTML removal
* URL extraction
* Email extraction
* URL/email removal from the text being processed
* Whitespace normalization
* General punctuation normalization/removal
* Emoji/decorative symbol removal
* Number preservation
* Tokenization
* Basic processing metadata
* A consistent dictionary-based return format

Lexis supports three tokenization modes:

1. `word` — default
2. `sentence`
3. `character`

There is only **one Lexis v1 behavior/pipeline**. The package should not become a collection of radically different preprocessing modes.

---

# 3. Public Input

The primary public function is:

```python
process_text(text: str, tokenization: str = "word") -> dict
```

`text` accepts:

```python
str
```

Only strings are valid inputs.

`tokenization` accepts one of:

```python
"word"       # default
"sentence"
"character"
```

## Invalid input

If `text` is not a string, Lexis raises:

```python
TypeError
```

Lexis should **not silently convert arbitrary objects using `str()`**.

For example:

```python
process_text(123)
```

should raise `TypeError` rather than silently processing `"123"`.

This prevents accidental misuse and hidden bugs in ML pipelines.

## Invalid tokenization value

If `tokenization` is not one of `"word"`, `"sentence"`, or `"character"`, Lexis raises:

```python
ValueError
```

For example:

```python
process_text("hello world", tokenization="paragraph")
```

should raise `ValueError` rather than silently falling back to a default.

---

# 4. Empty Input

Empty input is valid.

For example:

```python
process_text("")
```

should not raise an exception.

It should return the normal dictionary structure with empty values.

The same principle applies when valid input becomes empty after preprocessing.

For example, if the input contains only removable content:

```text
"!!! 😀 @@@"
```

Lexis should return an empty processing result rather than raising an error.

---

# 5. Processing Pipeline

The finalized Lexis v1 pipeline is:

```text
Raw input
    ↓
1. Input validation
    ↓
2. Extract URLs
    ↓
3. Extract email addresses
    ↓
4. Unicode normalization
    ↓
5. Remove extracted URLs and emails
    ↓
6. Remove HTML
    ↓
7. Remove emojis/decorative symbols
    ↓
8. Meaning-aware punctuation handling
    ↓
9. Convert text to lowercase
    ↓
10. Normalize whitespace
    ↓
11. Tokenize
    ↓
12. Generate metadata
    ↓
13. Return dictionary
```

The order is intentional.

URLs and emails are extracted **before** cleaning so that they are preserved in the output rather than destroyed by subsequent preprocessing. Extraction runs directly against the raw input; it does not depend on prior Unicode normalization.

Whitespace normalization runs **last**, immediately before tokenization. Earlier steps (HTML removal, extraction removal) intentionally leave gaps behind — collapsing whitespace only once, at the end, keeps that cleanup logic in a single place rather than repeating it after every step.

Symbol removal (emoji/decorative characters) runs **before** punctuation handling, and both run **before** lowercasing, so that a token's alphanumeric shape is still intact when Lexis decides which punctuation is structurally meaningful.

---

# 6. Unicode Normalization

Lexis performs **Unicode normalization**.

The purpose is to normalize equivalent Unicode representations without converting the text into ASCII.

Lexis should **not** transliterate arbitrary Unicode text into English/ASCII.

For example, Unicode normalization should not turn an entire multilingual text into an ASCII approximation.

The package remains language-agnostic.

The normalization form should use the standard NFC approach unless an implementation-level dependency requires an equivalent Unicode-normalization mechanism.

---

# 7. Case Normalization

All processed text is converted to lowercase.

Example:

```text
"Machine Learning Is FUN"
```

becomes:

```text
"machine learning is fun"
```

This is intentionally not configurable in v1.

Lexis provides one consistent default behavior rather than exposing a large configuration surface.

---

# 8. URL Extraction

URLs are extracted from the original input before destructive cleaning.

A URL is recognized if it begins with `http://`, `https://`, or `www.`. A bare domain with no scheme and no `www.` prefix (e.g. `example.com`) is not treated as a URL.

Extracted URLs are returned separately in:

```python
"urls"
```

Example:

```text
"Visit https://example.com for more information."
```

produces approximately:

```python
"urls": [
    "https://example.com"
]
```

`www.`-prefixed addresses are extracted the same way:

```text
"See www.example.org for details."
```

produces:

```python
"urls": [
    "www.example.org"
]
```

## Trailing punctuation

Sentence or phrase punctuation immediately following a URL (`.`, `,`, `!`, `?`, `;`, `:`) is not considered part of the URL and is stripped from the extracted value:

```text
"Visit https://example.com."
```

produces:

```python
"urls": [
    "https://example.com"
]
```

not `"https://example.com."`.

The extracted URL is then removed from the text being cleaned.

Therefore the URL is preserved as structured information while not contaminating the cleaned NLP text.

---

# 9. Email Extraction

Email addresses are extracted from the original input before destructive cleaning.

Extracted email addresses are returned separately in:

```python
"emails"
```

Example:

```text
"Contact us at hello@example.com"
```

produces:

```python
"emails": [
    "hello@example.com"
]
```

The extracted email address is then removed from the text being cleaned.

This prevents useful information from being lost while keeping email syntax out of the cleaned NLP text.

---

# 10. HTML Removal

HTML markup is removed from the text.

The goal is to remove markup while preserving meaningful textual content.

Example:

```html
<p>Hello <strong>world</strong></p>
```

should become approximately:

```text
Hello world
```

HTML tags themselves should not remain in the cleaned text.

---

# 11. Whitespace Normalization

Lexis normalizes unnecessary whitespace.

This includes:

* Repeated spaces
* Tabs
* Newlines
* Leading whitespace
* Trailing whitespace

For example:

```text
"  Hello    world\n\nthis is\tLexis  "
```

becomes:

```text
"Hello world this is Lexis"
```

Whitespace normalization occurs before the final output is generated.

---

# 12. Punctuation Handling

Punctuation handling follows a **meaning-preserving general NLP rule**.

### Core rule

> Remove punctuation when it functions as surrounding or separating punctuation; preserve punctuation when it is structurally part of a meaningful token.

Lexis should therefore avoid blindly deleting every punctuation character.

## Punctuation that should normally be removed

Examples:

```text
Hello!       → hello
"What"       → what
(Hello)      → hello
Hello, world → hello world
What?        → what
```

Common sentence/phrase punctuation such as:

```text
.
,
!
?
:
;
(
)
[
]
{
}
"
'
```

is removed when it acts as surrounding or separating punctuation.

## Punctuation that is structurally meaningful should be preserved

Examples:

```text
COVID-19
state-of-the-art
3.14
don't
C++
C#
```

should retain their meaningful internal punctuation.

Therefore:

```text
COVID-19
```

becomes:

```text
covid-19
```

rather than:

```text
covid19
```

Likewise:

```text
3.14
```

remains:

```text
3.14
```

and:

```text
don't
```

remains:

```text
don't
```

## Trailing punctuation on technical tokens

A token can simultaneously contain meaningful internal punctuation *and* trailing punctuation that is purely a sentence/phrase separator. Only the separator is removed; the internal punctuation is preserved.

```text
Node.js.   → node.js
C++.       → c++
```

Note that in `Node.js.` the first `.` is structurally part of the token and the second `.` is sentence punctuation, even though both characters are the same symbol. Lexis distinguishes them by position — punctuation embedded between two alphanumeric characters is preserved, while punctuation at the true edge of a token (nothing meaningful before or after it in context) is removed — rather than by classifying the whole token as "technical" or "not technical" and protecting every matching character in it.

The implementation should use a Unicode-aware/general tokenization strategy rather than maintaining an unnecessarily large hand-written punctuation exception list.

---

# 13. Numbers

Numbers are preserved.

Numbers may contain meaningful punctuation and should not be blindly removed.

Examples:

```text
2026
19
3.14
COVID-19
```

remain represented in the processed text.

The rationale is that numerical information can be important to downstream NLP/ML tasks.

Lexis should therefore not assume that numbers are noise.

---

# 14. Emojis and Decorative Symbols

Emojis are treated separately from punctuation.

Lexis removes emojis and decorative/non-linguistic symbols from the cleaned text.

Example:

```text
"Hello 😀 🚀 ❤️"
```

becomes approximately:

```text
"hello"
```

This does **not** mean that every Unicode character is stripped.

The distinction is:

* Meaningful linguistic/technical characters → preserve
* Meaningful internal punctuation → preserve
* Numbers → preserve
* Emojis/decorative symbols → remove

Some characters, such as `+`, are classified as Unicode symbols but are also structurally meaningful within a technical token (e.g. `C++`). In that case the symbol is preserved rather than removed:

```text
"C++ is fast 🚀" → "c++ is fast"
```

The `+` characters in `C++` are kept; the rocket emoji is removed.

---

# 15. Tokenization

Lexis supports exactly three tokenization strategies.

```text
word
sentence
character
```

The default is:

```text
word
```

The tokenization method can be selected when calling the processing function.

Conceptually:

```python
process_text(text)
```

uses:

```text
word
```

while:

```python
process_text(text, tokenization="sentence")
```

uses sentence tokenization.

And:

```python
process_text(text, tokenization="character")
```

uses character tokenization.

The preprocessing pipeline itself remains the same.

Only the final representation of the cleaned text changes.

---

# 16. Word Tokenization

Word tokenization uses **whitespace as the primary word boundary**.

Example:

```text
"machine learning is useful"
```

becomes:

```python
[
    "machine",
    "learning",
    "is",
    "useful"
]
```

The tokens are generated from the already-cleaned text.

Meaningful internal punctuation remains part of a token.

For example:

```text
"covid-19"
```

remains a token rather than being arbitrarily split into:

```python
["covid", "19"]
```

---

# 17. Sentence Tokenization

Sentence tokenization uses exactly these sentence-boundary characters:

```python
[".", "?", "!"]
```

No additional punctuation is treated as a sentence boundary in v1.

For example:

```text
"Lexis is simple. Lexis is useful! Is it reusable?"
```

becomes:

```python
[
    "lexis is simple",
    "lexis is useful",
    "is it reusable"
]
```

Sentence punctuation itself is not included in the returned sentence tokens.

Commas, semicolons, colons, etc. do not create sentence boundaries.

## Boundary characters inside technical tokens

A boundary character is only treated as a sentence boundary when it is *not* sandwiched between two alphanumeric characters. A `.`, `?`, or `!` embedded inside a technical or compound token (e.g. `Node.js`, `3.14`) is part of that token, not a sentence break — consistent with how the same characters are treated everywhere else in the pipeline (see §12).

```text
"Use Node.js for this. It works with C++ too!"
```

becomes:

```python
[
    "use node.js for this",
    "it works with c++ too"
]
```

`Node.js` is not split into `"node"` and `"js"` as separate sentences. A boundary character at the true edge of a sentence — including one immediately after a technical token, such as `Node.js.` — still ends the sentence normally.

---

# 18. Character Tokenization

Character tokenization returns individual characters from the final cleaned text.

Spaces are included.

For example:

```text
"hello world"
```

becomes:

```python
[
    "h",
    "e",
    "l",
    "l",
    "o",
    " ",
    "w",
    "o",
    "r",
    "l",
    "d"
]
```

This keeps character tokenization literal and predictable.

Lexis does not introduce another hidden whitespace-removal step specifically for character tokenization.

---

# 19. Return Format

Every successful call returns the same dictionary structure regardless of tokenization mode.

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
        "token_count": int
    }
}
```

## `original_text`

The exact text supplied to Lexis.

No modification is made to this field.

## `cleaned_text`

The final normalized and cleaned text after:

* Unicode normalization
* URL/email removal
* HTML removal
* whitespace normalization
* lowercasing
* punctuation handling
* emoji/decorative-symbol removal

## `tokens`

The tokens generated from `cleaned_text`.

The exact contents depend on the selected tokenization method.

## `emails`

All extracted email addresses.

## `urls`

All extracted URLs.

## `metadata`

Basic information about the processed result.

### `original_length`

Length of the original input text.

### `cleaned_length`

Length of the final cleaned text.

### `token_count`

Number of tokens returned in `tokens`.

---

# 20. Empty Result

If valid input is empty or becomes empty after preprocessing, Lexis still returns the same dictionary structure.

Conceptually:

```python
{
    "original_text": "...",
    "cleaned_text": "",
    "tokens": [],
    "emails": [],
    "urls": [],
    "metadata": {
        "original_length": ...,
        "cleaned_length": 0,
        "token_count": 0
    }
}
```

Lexis does not raise an exception merely because no usable text remains.

---

# 21. What Lexis Does NOT Provide

Lexis v1 deliberately excludes functionality that belongs to downstream NLP/ML tooling.

It does not provide:

* TF-IDF vectorization
* Count vectorization
* Word embeddings
* Transformer embeddings
* Word2Vec
* Model training
* Classification
* Sentiment analysis
* Named entity recognition
* Language detection
* Translation
* Topic modeling
* ML inference
* Large configurable preprocessing frameworks
* API/server functionality

The consumer can take Lexis's output and use any of these tools afterward.

---

# 22. Design Philosophy

Lexis should remain:

### Simple

A user should be able to understand the package and its output quickly.

### Robust

Common real-world text and edge cases should be handled safely and predictably.

### Reusable

The same package should work as a preprocessing step across many different NLP/ML projects.

### Agnostic

Lexis should not assume whether the downstream task is:

* classification
* regression
* search
* clustering
* information retrieval
* embeddings
* traditional NLP
* deep learning

### Predictable

The same input and configuration should produce deterministic, understandable output.

### Lightweight

Lexis should not unnecessarily recreate functionality already provided by established NLP libraries.

---

# 23. Final Lexis v1 Pipeline

The implementation must follow this finalized pipeline:

```text
Raw text
   │
   ▼
Input validation
   │
   ▼
Extract URLs ────────────────┐
   │                         │
   ▼                         │
Extract emails ──────────────┤
   │                         │
   ▼                         │
Unicode normalization        │
   │                         │
   ▼                         │
Remove extracted URLs/emails │
   │                         │
   ▼                         │
Remove HTML                  │
   │                         │
   ▼                         │
Remove emojis/decorative     │
symbols                      │
   │                         │
   ▼                         │
Meaning-aware punctuation    │
handling                     │
   │                         │
   ▼                         │
Lowercase                    │
   │                         │
   ▼                         │
Normalize whitespace         │
   │                         │
   ▼                         │
Tokenization                 │
   │                         │
   ▼                         │
Metadata generation          │
   │                         │
   ▼                         │
Return dictionary ◄──────────┘
```

## Final tokenization choices

```text
word       ← default
sentence
character
```

## Final output

```python
{
    "original_text": ...,
    "cleaned_text": ...,
    "tokens": ...,
    "emails": ...,
    "urls": ...,
    "metadata": {
        "original_length": ...,
        "cleaned_length": ...,
        "token_count": ...
    }
}
```

---

# 24. Implementation Freeze

This specification represents the **Lexis v1 behavioral contract**.

Once implementation begins:

* Do not add additional preprocessing features.
* Do not add vectorization.
* Do not introduce an API.
* Do not add unnecessary configuration options.
* Do not change the return structure.
* Do not change the core processing order.
* Do not introduce task-specific NLP behavior.

Any future functionality should be considered for a separate version rather than changing the agreed v1 behavior mid-implementation.

---

# 25. Errata

This section tracks corrections made to this document so that it accurately describes the shipped v1 implementation. These are documentation fixes, not behavior changes — the freeze in §24 still applies to the underlying pipeline stages, return structure, and scope.

* **Pipeline order (§5, §23).** The original draft listed whitespace normalization before lowercasing and punctuation handling, and listed extraction as occurring after Unicode normalization. The implemented order extracts URLs/emails from the raw input first, then normalizes, cleans, and normalizes whitespace last, immediately before tokenization. §5 and §23 have been corrected to match the implementation.
* **Sentence tokenization and technical tokens (§17).** The original draft did not account for boundary characters embedded inside a technical token (e.g. the `.` in `Node.js`). A boundary character is only a sentence boundary when it is not sandwiched between two alphanumeric characters, consistent with the meaning-preserving punctuation rule already defined in §12.
* **URL extraction (§8).** Documented two behaviors that were already implemented but not written down: `www.`-prefixed addresses are recognized as URLs, and trailing sentence/phrase punctuation immediately after a URL is stripped from the extracted value.
* **Technical-token symbol preservation (§14).** Documented that a character which is simultaneously a Unicode symbol and part of a technical token's meaningful punctuation (e.g. `+` in `C++`) is preserved rather than stripped during emoji/decorative-symbol removal.
* **Public function signature (§3).** Documented the `tokenization` parameter and the `ValueError` raised for an unsupported value, both of which were already implemented but missing from the original signature description.