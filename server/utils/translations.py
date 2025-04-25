
def translate_boolean(value: bool) -> str:
    return "Verdadero" if value is True else "Falso"

def translate_lang(lang_code: str) -> str:
    return {
        "en-CR": "English (Costa Rica)",
        "es-CR": "Español (Costa Rica)"
    }.get(lang_code, lang_code)