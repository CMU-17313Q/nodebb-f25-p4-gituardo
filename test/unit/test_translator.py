from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    # A normal English sentence
    is_english, translated_content = translate_content("This is an English message")
    assert is_english == True
    assert translated_content == "This is an English message"

def test_llm_gibberish_response():
    # A gibberish or unrecognized message
    is_english, translated_content = translate_content("asldkjasldkj123!@#")
    # Since it's not a known foreign message, we assume it's English
    assert is_english == True
    assert translated_content == "asldkjasldkj123!@#"
