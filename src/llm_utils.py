import ollama

MODEL_NAME = "gemma3:270m"

CLASSIFICATION_CONTEXT = """\
You are a language identifier.
Your task is to detect the primary language of the given text input and respond only with the English name of that language.

Rules:
- Do not translate or explain.
- Do not guess based on previous examples--decide only from the current input.
- If the text appears to be random characters, symbols, or nonsense, respond with "English".

Output format: a single word--the English name of the detected language.

Examples:
INPUT: Bonjour, je m'appelle Sarah
OUTPUT: French

INPUT: Können Sie mir bitte helfen?
OUTPUT: German

INPUT: %#$%#%#%#%#%@#!#!@#
OUTPUT: English"""

TRANSLATION_CONTEXT = """\
You are a translation model. Your only task is to translate any non-English input into natural, fluent English.
Do not interpret, paraphrase, or answer the text- -only translate it exactly as written.
Respond only with the English translation, and nothing else.

Example:
INPUT: Bonjour, je m'appelle Sarah
OUTPUT: Hello, my name is Sarah

INPUT: Il fait très chaud aujourd'hui, n'est-ce pas ?
OUTPUT: It is very hot today, isn't it?
"""

def get_translation(post: str) -> str:
    try:
        messages = [
            {"role": "system", "content": TRANSLATION_CONTEXT},
            {"role": "user", "content": post},
        ]
        resp = ollama.chat(model=MODEL_NAME, messages=messages)
        text = getattr(resp, 'message', None)
        if text is None:
            return post
        return resp.message.content.strip()
    except Exception as e:
        return post

def get_language(post: str) -> str:
    try:
        messages = [
            {"role": "system", "content": CLASSIFICATION_CONTEXT},
            {"role": "user", "content": post},
        ]
        resp = ollama.chat(model=MODEL_NAME, messages=messages)
        if not hasattr(resp, 'message') or resp.message is None:
            return 'English'
        lang = resp.message.content.strip()
        return lang
    except Exception:
        return 'English'

def query_llm(post: str) -> tuple[bool, str]:
    """(is_english: bool, translation: str)"""
    try:
        lang = get_language(post)
    except Exception:
        lang = 'English'

    if isinstance(lang, str) and lang.strip().lower() == 'english':
        return (True, post)

    try:
        translation = get_translation(post)
    except Exception:
        translation = post

    return (False, translation)

def query_llm_robust(post: str) -> tuple[bool, str]:
    try:
        result = query_llm(post)

        # type checking
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool) and isinstance(result[1], str):
            return result

        is_eng = None
        text = None

        if isinstance(result, tuple) and len(result) >= 1:
            is_eng = bool(result[0]) if isinstance(result[0], (bool, int)) else None

        if isinstance(result, tuple) and len(result) >= 2:
            text = str(result[1]) if result[1] is not None else None
 
        if is_eng is None:
            try:
                is_eng = (get_language(post).strip().lower() == 'english')
            except Exception:
                is_eng = True

        if text is None:
            try:
                text = get_translation(post) if not is_eng else post
            except Exception:
                text = post

        return (is_eng, text)

    except Exception:
        return (True, post)

