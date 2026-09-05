"""
Batch-processing example.

A common real use case: cleaning a list of raw text records (e.g. rows
pulled from a CSV, a set of support tickets, scraped reviews) before
handing them to a downstream model, search index, or analysis step.
"""

from lexit import process_text

raw_records = [
    "I LOVE this product!! 😍 10/10 would buy again.",
    "Terrible support. Contact me at angry@example.com asap.",
    "Meh, it's okay. See www.example.org/reviews for details...",
    "",  # empty input is valid and simply produces empty output
]


def main() -> None:
    for i, record in enumerate(raw_records, start=1):
        result = process_text(record)
        print(f"--- record {i} ---")
        print(f"original: {result['original_text']!r}")
        print(f"cleaned:  {result['cleaned_text']!r}")
        print(f"tokens:   {result['tokens']}")
        if result["urls"]:
            print(f"urls:     {result['urls']}")
        if result["emails"]:
            print(f"emails:   {result['emails']}")
        print()


if __name__ == "__main__":
    main()
