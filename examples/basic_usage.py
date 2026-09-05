"""
Basic usage of Lexit.

Shows the default (word) pipeline, the two other tokenization modes,
and what happens with messy real-world input (HTML, emoji, a URL, an
email address, and mixed punctuation).
"""

from lexit import process_text


def main() -> None:
    text = (
        "<p>Hey there!</p> Check https://example.com or email "
        "hello@example.com. COVID-19 news, Node.js 3.14 release 🚀!"
    )

    print("=== word tokenization (default) ===")
    result = process_text(text)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== sentence tokenization ===")
    sentence_result = process_text(
        "Use Node.js for this. It works with C++ too!",
        tokenization="sentence",
    )
    print(sentence_result["tokens"])

    print("\n=== character tokenization ===")
    character_result = process_text("Hi!", tokenization="character")
    print(character_result["tokens"])


if __name__ == "__main__":
    main()
