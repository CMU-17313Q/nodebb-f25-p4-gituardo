from mock import patch
import src.llm_utils as llm_utils
from src.llm_utils import query_llm, query_llm_robust

class Resp:
    def __init__(self, content):
        class M:
            pass
        self.message = M()
        self.message.content = content

# success case
@patch('src.llm_utils.ollama.chat')
def test_normal_flow(mock_chat):
    mock_chat.side_effect = [Resp('German'), Resp('Here is your first example.') ]
    res = query_llm('Hier ist dein erstes Beispiel.')
    
    assert isinstance(res, tuple)
    assert res == (False, 'Here is your first example.')

# responds with something other than the translation
@patch('src.llm_utils.ollama.chat')
def test_unexpected_language_message(mock_chat):
    mock_chat.side_effect = [Resp("I don't understand your request"), Resp("I don't understand your request")]
    res = query_llm_robust('Hier ist dein erstes Beispiel.')
    
    assert isinstance(res, tuple)
    assert isinstance(res[0], bool) and isinstance(res[1], str)

# doesn't response/malformed response
@patch('src.llm_utils.ollama.chat')
def test_message_none(mock_chat):
    mock_chat.return_value = type('X',(object,),{'message': None})()
    res = query_llm_robust('Some post')
    
    assert res == (True, 'Some post')

# throws exception (e.g., model was not loaded in cells above)
@patch('src.llm_utils.ollama.chat')
def test_client_raises_exception(mock_chat):
    mock_chat.side_effect = RuntimeError('service down')
    res = query_llm_robust('Network failure example')
    
    assert res == (True, 'Network failure example')

# returns with something that is not a language
@patch('src.llm_utils.ollama.chat')
def test_partial_malformed_responses(mock_chat):
    mock_chat.side_effect = [Resp('NotALanguage'), Resp("")]
    res = query_llm_robust('Unusual post')
    
    assert isinstance(res, tuple)
    assert isinstance(res[0], bool) and isinstance(res[1], str)
