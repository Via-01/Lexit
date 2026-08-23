# Lexis v1 — Package Structure and Dependencies

## 1. Project Structure

Lexis uses a standard `src`-based Python package layout.

```text
lexis/
├── docs/
│     ├── Final-Specification.md
│     └── Final-Package-and-Dependencies.md
│ 
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── lexis/
│       ├── __init__.py
│       ├── processor.py
│       ├── cleaners.py
│       ├── extractors.py
│       └── tokenizer.py
│
└── tests/
    ├── test_cleaner.py
    ├── test_extractors.py
    ├── test_tokenizer.py
    └── test_processor.py
```

Note the test-file naming is intentionally singular where the module it covers is plural (`tests/test_cleaner.py` tests `src/lexis/cleaners.py`); this is existing convention, not a typo.

Generated artifacts — `__pycache__/`, `*.egg-info/`, `.pytest_cache/` — are build/tooling output, not part of the source layout above, and should not be tracked in version control. If the project doesn't already have a `.gitignore` covering these, add one.

> **Note:** `README.md` and `LICENSE` are listed above as part of the intended structure but are not yet present in the repository. A README has been added alongside this documentation pass; a `LICENSE` file still needs to be chosen and added separately, since `pyproject.toml` already declares `license = { file = "LICENSE" }`.

## 2. Module Responsibilities

### `processor.py`

The main orchestration layer.

Responsible for coordinating the complete Lexis pipeline:

```text
input validation
→ extraction
→ cleaning
→ tokenization
→ metadata
→ result dictionary
```

This is the primary internal entry point used by the public API.

---

### `extractors.py`

Contains extraction logic for information that needs to be preserved separately from the cleaned text.

Responsibilities:

* URL extraction
* Email extraction

Extracted URLs and emails are returned in the final result dictionary.

---

### `cleaners.py`

Contains the actual text-cleaning operations.

Responsibilities:

* Unicode normalization
* HTML tag removal
* URL/email removal from processing text
* Emoji/decorative-symbol removal
* Meaning-aware punctuation handling
* Lowercase conversion
* Whitespace normalization

The cleaner should not perform tokenization.

---

### `tokenizer.py`

Contains the three supported tokenization strategies:

```text
word
sentence
character
```

The default tokenization strategy is `word`.

The tokenizer operates on the already-cleaned text.

---

### `__init__.py`

Defines the public package interface.

Users should be able to import the primary Lexis functionality directly from the package rather than needing to know the internal module structure.

The internal modules should therefore remain implementation details.

---

## 3. Runtime Dependencies

Lexis intentionally keeps its runtime dependency footprint extremely small.

### External dependency

```text
regex
```

`regex` is used for robust Unicode-aware pattern matching and text classification.

This is justified because Lexis needs reliable handling of:

* Unicode text
* Unicode character categories
* URLs
* Email addresses
* HTML markup
* punctuation
* symbols
* multilingual text

Lexis does not attempt to recreate sophisticated Unicode-aware regular-expression functionality solely to achieve zero dependencies.

### Python standard library

The standard library should be used wherever appropriate, including functionality such as:

* Unicode normalization
* basic string operations
* type annotations
* metadata calculations

No additional runtime libraries should be introduced unless implementation demonstrates a genuine requirement.

---

## 4. Development Dependencies

Development-only dependencies:

```text
pytest
ruff
mypy
```

### `pytest`

Used for the complete automated test suite.

Tests should cover both ordinary examples and edge cases.

### `ruff`

Used for linting and formatting.

### `mypy`

Used for static type checking.

---

## 5. Explicitly Excluded Dependencies

Lexis v1 does **not** depend on:

* spaCy
* NLTK
* pandas
* scikit-learn
* transformers
* PyTorch
* TensorFlow
* BeautifulSoup
* emoji-specific libraries
* embedding libraries
* vectorization libraries

Lexis is a preprocessing utility, not a complete NLP framework.

---

## 6. Python Compatibility

Target Python version:

```text
Python >= 3.10
```

Lexis does not require newer Python-specific functionality, so unnecessarily restricting the supported Python versions would reduce reusability.

---

## 7. Design Principle

The dependency philosophy is:

> **Dependency-minimal, not dependency-free.**

A small, well-justified dependency is preferable to recreating complex Unicode-aware functionality poorly simply to avoid an external package.

The intended runtime footprint is therefore:

```text
Python standard library
        +
      regex
```

Nothing more unless a genuine implementation requirement is discovered.

---

## 8. Architectural Constraints

The following are fixed for Lexis v1:

* Use a `src` package layout.
* Keep internal responsibilities separated.
* Do not introduce a model/data-class layer unnecessarily.
* Do not add an API/server layer.
* Do not introduce an NLP framework dependency.
* Do not add vectorization functionality.
* Keep the public interface small.
* Keep runtime dependencies minimal.
* Keep implementation details behind the public package interface.