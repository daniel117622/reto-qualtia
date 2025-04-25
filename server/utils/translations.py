
def translate_boolean(value: bool) -> str:
    return "Verdadero" if value is True else "Falso"

def translate_lang(lang_code: str) -> str:
    return {
        "en-CR": "English (Costa Rica)",
        "es-CR": "Español (Costa Rica)"
    }.get(lang_code, lang_code)

def translate_cop_to_mxn(price : int) -> str:
    exchange_rate = 0.0045  
    mxn = price * exchange_rate
    return f"${mxn:,.2f} MXN"