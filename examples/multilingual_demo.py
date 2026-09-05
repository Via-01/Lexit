"""
Multilingual demo: 12 non-Indic languages, the 22 Scheduled Languages
of India (per the Eighth Schedule of the Indian Constitution), and a
dedicated Chinese comparison at the end.

Purpose
-------
This exercises Lexit's tokenizer against a wide range of real Unicode
scripts to show:

  1. Space-delimited languages (the large majority here) tokenize
     correctly regardless of script complexity.
  2. Chinese (and, for the same reason, Japanese/Thai/etc. — see
     README > Language support) does NOT tokenize correctly, because
     it has no inter-word spacing for `.split()` to key off.

A note on translation accuracy
-------------------------------
The phrases below are simple, illustrative greetings meant to
exercise each script — NOT verified professional translations. A few
of the lower-resource languages here (Santali/Ol Chiki, Kashmiri,
Sindhi, Dogri, Bodo, Konkani, Maithili, Manipuri) are best-effort
approximations. If you need these for anything beyond a tokenizer
demo, have a native speaker check them.

Tokenization mode is chosen pseudo-randomly per record (seeded, so
re-running this script gives the same result) to show that all three
modes behave sensibly across scripts — not just the default.
"""

import random

from lexit import process_text

# Reproducible "random" mode selection, weighted toward word/sentence
# since character mode on multi-word text is long and not very
# illustrative on its own.
random.seed(7)
_MODES = ["word", "word", "sentence", "sentence", "character"]


def _mode() -> str:
    return random.choice(_MODES)


# --- 12 non-Indic languages ---------------------------------------
non_indic = [
    ("French", "Bonjour le monde ! Comment allez-vous aujourd'hui ?"),
    ("German", "Hallo Welt! Wie geht es dir heute?"),
    ("Spanish", "¡Hola mundo! ¿Cómo estás hoy?"),
    ("Russian", "Привет, мир! Как твои дела сегодня?"),
    ("Arabic", "مرحبا بالعالم! كيف حالك اليوم؟"),
    ("Hebrew", "שלום עולם! מה שלומך היום?"),
    ("Greek", "Γεια σου κόσμε! Πώς είσαι σήμερα;"),
    ("Korean", "안녕하세요 세계! 오늘 기분이 어떠세요?"),
    ("Vietnamese", "Xin chào thế giới! Hôm nay bạn thế nào?"),
    ("Thai", "สวัสดีชาวโลก! วันนี้เป็นอย่างไรบ้าง?"),
    ("Persian (Farsi)", "سلام دنیا! امروز حالت چطور است؟"),
    ("Japanese", "こんにちは世界！今日は元気ですか？"),
]

# --- 22 Scheduled Languages of India --------------------------------
indic = [
    ("Hindi", "नमस्ते दुनिया! आज आप कैसे हैं?"),
    ("Bengali", "ওহে বিশ্ব! আজ তুমি কেমন আছো?"),
    ("Marathi", "नमस्कार जग! आज तू कसा आहेस?"),
    ("Telugu", "హలో ప్రపంచం! ఈ రోజు మీరు ఎలా ఉన్నారు?"),
    ("Tamil", "வணக்கம் உலகம்! இன்று நீங்கள் எப்படி இருக்கிறீர்கள்?"),
    ("Gujarati", "નમસ્તે દુનિયા! આજે તમે કેમ છો?"),
    ("Urdu", "ہیلو دنیا! آج آپ کیسے ہیں؟"),
    ("Kannada", "ಹಲೋ ಜಗತ್ತೇ! ಇಂದು ನೀವು ಹೇಗಿದ್ದೀರಿ?"),
    ("Odia", "ନମସ୍କାର ବିଶ୍ୱ! ଆଜି ଆପଣ କେମିତି ଅଛନ୍ତି?"),
    ("Malayalam", "ഹലോ ലോകം! ഇന്ന് നിങ്ങൾക്ക് സുഖമാണോ?"),
    ("Punjabi", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਦੁਨੀਆ! ਅੱਜ ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?"),
    ("Assamese", "নমস্কাৰ বিশ্ব! আজি আপুনি কেনে আছে?"),
    ("Maithili", "प्रणाम दुनिया! आइ अहाँ केहन छी?"),
    ("Santali", "ᱡᱚᱦᱟᱨ ᱫᱩᱱᱤᱭᱟᱹ! ᱛᱮᱦᱮᱸ ᱟᱢ ᱪᱮᱫ ᱢᱮᱱᱟᱢᱟ?"),
    ("Kashmiri", "ہیلو دُنیا! اَز تُہہِ کیٕہہ چھِو؟"),
    ("Nepali", "नमस्ते संसार! आज तपाईं कस्तो हुनुहुन्छ?"),
    ("Konkani", "नमस्कार संसारा! आज तूं कशी आसा?"),
    ("Sindhi", "هيلو دنيا! اڄ توهان ڪيئن آهيو؟"),
    ("Dogri", "नमस्ते दुनिया! अज्ज तुसें केह् हाल ऐ?"),
    ("Manipuri (Meitei)", "ꯍꯦꯂꯣ ꯃꯤꯆꯥꯡ! ꯅꯣꯡꯃꯗꯤ ꯀꯔꯝ ꯂꯩ?"),
    ("Sanskrit", "नमस्ते विश्व! अद्य भवान् कथम् अस्ति?"),
    ("Bodo", "नमस्कार दुनिया! आज नों माबोरै दंमोन?"),
]


def run(section_title: str, records: list[tuple[str, str]]) -> None:
    print(f"\n{'=' * 60}")
    print(section_title)
    print("=" * 60)
    for language, text in records:
        mode = _mode()
        result = process_text(text, tokenization=mode)
        print(f"\n[{language}] (tokenization={mode})")
        print(f"  original: {text}")
        print(f"  cleaned:  {result['cleaned_text']}")
        print(f"  tokens:   {result['tokens']}")


def main() -> None:
    run("12 non-Indic languages", non_indic)
    run("22 Scheduled Languages of India", indic)

    # --- Chinese: the documented limitation, shown explicitly -------
    print(f"\n{'=' * 60}")
    print("Chinese — demonstrating the known limitation")
    print("=" * 60)

    chinese_text = "你好，世界！今天天气很好。你怎么样？"

    word_result = process_text(chinese_text, tokenization="word")
    print("\n[Chinese] (tokenization=word)")
    print(f"  original: {chinese_text}")
    print(f"  cleaned:  {word_result['cleaned_text']}")
    print(f"  tokens:   {word_result['tokens']}")
    print(
        "  -> Whole sentence comes back as ONE token: Chinese has no "
        "spaces between words for `.split()` to use."
    )

    sentence_result = process_text(chinese_text, tokenization="sentence")
    print("\n[Chinese] (tokenization=sentence)")
    print(f"  original: {chinese_text}")
    print(f"  tokens:   {sentence_result['tokens']}")
    print(
        "  -> Still ONE token, and for a second, distinct reason: Lexit's "
        "sentence boundaries are the ASCII characters '.', '!', '?', but "
        "Chinese uses different, full-width punctuation marks ('。', "
        "'！', '？') at different Unicode code points, so they're never "
        "recognized as boundaries either. Both word- and sentence-level "
        "segmentation fail here, for two separate reasons. See README > "
        "Language support."
    )

    character_result = process_text(chinese_text, tokenization="character")
    print("\n[Chinese] (tokenization=character)")
    print(f"  original: {chinese_text}")
    print(f"  tokens:   {character_result['tokens']}")
    print(
        "  -> This one DOES split correctly, since character tokenization "
        "doesn't need spaces at all. But notice the full-width punctuation "
        "('，', '！', '。') shows up as its own tokens rather than being "
        "removed: punctuation-stripping only trims a token's edges, and "
        "since the whole sentence was one token, the punctuation in the "
        "middle of it was never stripped in the first place. Compare this "
        "to a space-delimited language, where the same punctuation is "
        "correctly removed before character tokenization ever runs."
    )


if __name__ == "__main__":
    main()
