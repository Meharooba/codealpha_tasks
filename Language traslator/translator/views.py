import html
import requests

from django.shortcuts import render


LANGUAGES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bn": "Bengali",
    "bg": "Bulgarian",
    "zh-TW": "Chinese (Traditional)",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ms": "Malay",
    "ne": "Nepali",
    "no": "Norwegian",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sr": "Serbian",
    "si": "Sinhala",
    "sk": "Slovak",
    "es": "Spanish",
    "sw": "Swahili",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
}

MAX_TEXT_BYTES = 500
REQUEST_TIMEOUT = 12


def clean_translation(value):
    """Normalize a translation returned by an external service."""
    if not isinstance(value, str):
        return ""

    value = html.unescape(value).strip()

    
    if not value or len(value) > 10000:
        return ""

    if "\x00" in value:
        return ""

    return value


def is_usable_translation(translated, original, target_lang):
    """
    Reject empty results and obvious service errors.
    This cannot determine whether a translation is semantically correct.
    """
    translated = clean_translation(translated)

    if not translated:
        return False
    
    if translated.casefold() == LANGUAGES[target_lang].casefold():
        return False

  
    return True


def google_translate(text, source_lang, target_lang):
    """Try the unofficial Google Translate endpoint."""
    response = requests.get(
        "https://translate.googleapis.com/translate_a/single",
        params={
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text,
        },
        timeout=REQUEST_TIMEOUT,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list) or not data:
        return ""

    segments = data[0]

    if not isinstance(segments, list):
        return ""

    parts = []

    for segment in segments:
        if (
            isinstance(segment, list)
            and segment
            and isinstance(segment[0], str)
        ):
            parts.append(segment[0])

    translated = clean_translation("".join(parts))

    if is_usable_translation(translated, text, target_lang):
        return translated

    return ""


def fallback_translate(text, source_lang, target_lang):
    """Try MyMemory when the primary translation service fails."""
    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": f"{source_lang}|{target_lang}",
            },
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "LanguageTranslator/1.0"},
        )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            return ""

        if data.get("responseStatus") != 200:
            return ""

        response_data = data.get("responseData")

        if not isinstance(response_data, dict):
            return ""

        translated = clean_translation(
            response_data.get("translatedText", "")
        )

        if is_usable_translation(translated, text, target_lang):
            return translated

    except (
        requests.RequestException,
        ValueError,
        TypeError,
        AttributeError,
    ):
        return ""

    return ""


def translate_text(request):
    translated_text = ""
    error = ""
    input_text = ""
    source_lang = "en"
    target_lang = "ml"

    if request.method == "POST":
        input_text = request.POST.get("text", "").strip()
        source_lang = request.POST.get("source_lang", "en")
        target_lang = request.POST.get("target_lang", "ml")

        if source_lang not in LANGUAGES:
            error = "Please select a valid source language."

        elif target_lang not in LANGUAGES:
            error = "Please select a valid target language."

        elif not input_text:
            error = "Please enter some text to translate."

        elif len(input_text.encode("utf-8")) > MAX_TEXT_BYTES:
            error = (
                f"Please keep your text within "
                f"{MAX_TEXT_BYTES} UTF-8 bytes."
            )

        elif source_lang == target_lang:
            translated_text = input_text

        else:
            try:
                translated_text = google_translate(
                    input_text,
                    source_lang,
                    target_lang,
                )
            except (
                requests.RequestException,
                ValueError,
                TypeError,
                IndexError,
                KeyError,
            ):
                translated_text = ""

            if not translated_text:
                translated_text = fallback_translate(
                    input_text,
                    source_lang,
                    target_lang,
                )

            if not translated_text:
                error = (
                    "We couldn't translate your text right now. "
                    "The translation services may be unavailable "
                    "or may not support this language pair. "
                    "Please try again later."
                )

    return render(
        request,
        "translator/index.html",
        {
            "languages": LANGUAGES,
            "input_text": input_text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "error": error,
        },
    )