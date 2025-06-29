import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from utils.logger import logger, log_execution_time

@pytest.fixture
def temp_log_file():
    """Cria um arquivo de log temporário para testes."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
    temp_file.close()
    yield temp_file.name
    os.unlink(temp_file.name)

def test_logger_initialization():
    """Testa se o logger é inicializado corretamente."""
    assert logger is not None
    assert hasattr(logger, 'info')
    assert hasattr(logger, 'warning')
    assert hasattr(logger, 'error')
    assert hasattr(logger, 'debug')

def test_logger_info_level():
    """Testa logging no nível info."""
    with patch.object(logger.logger, 'info') as mock_info:
        logger.info("Test message", user_id=123, action="test")
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        assert log_data["message"] == "Test message"
        assert log_data["user_id"] == 123
        assert log_data["action"] == "test"

def test_logger_warning_level():
    """Testa logging no nível warning."""
    with patch.object(logger.logger, 'warning') as mock_warning:
        logger.warning("Warning message", ip="127.0.0.1", endpoint="/test")
        mock_warning.assert_called_once()
        call_args = mock_warning.call_args[0][0]
        log_data = json.loads(call_args)
        assert log_data["message"] == "Warning message"
        assert log_data["ip"] == "127.0.0.1"
        assert log_data["endpoint"] == "/test"

def test_logger_error_level():
    """Testa logging no nível error."""
    with patch.object(logger.logger, 'error') as mock_error:
        error = Exception("Test error")
        logger.error("Error occurred", error=error, user_id=456)
        mock_error.assert_called_once()
        call_args = mock_error.call_args[0][0]
        log_data = json.loads(call_args)
        assert log_data["message"] == "Error occurred"
        assert log_data["user_id"] == 456
        assert "error_type" in log_data
        assert "error_message" in log_data

def test_logger_debug_level():
    """Testa logging no nível debug."""
    with patch.object(logger.logger, 'debug') as mock_debug:
        logger.debug("Debug message", data={"key": "value"})
        mock_debug.assert_called_once()
        call_args = mock_debug.call_args[0][0]
        log_data = json.loads(call_args)
        assert log_data["message"] == "Debug message"
        assert log_data["data"]["key"] == "value"

def test_logger_with_structured_data():
    """Testa logging com dados estruturados."""
    with patch.object(logger.logger, 'info') as mock_info:
        structured_data = {
            "user_id": 123,
            "action": "login",
            "timestamp": "2024-01-01T00:00:00Z",
            "metadata": {"browser": "Chrome", "os": "Windows"}
        }
        
        logger.info("User action", **structured_data)
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == "User action"
        assert log_data["user_id"] == 123
        assert log_data["action"] == "login"
        assert "metadata" in log_data

def test_logger_log_request():
    """Testa logging de requisições HTTP."""
    with patch.object(logger.logger, 'info') as mock_info:
        logger.log_request(
            method="POST",
            endpoint="/chat",
            status_code=200,
            response_time=1.5,
            user_agent="Mozilla/5.0",
            ip="127.0.0.1"
        )
        
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == "HTTP POST /chat"
        assert log_data["method"] == "POST"
        assert log_data["endpoint"] == "/chat"
        assert log_data["status_code"] == 200
        assert log_data["response_time_ms"] == 1500.0
        assert log_data["user_agent"] == "Mozilla/5.0"
        assert log_data["ip"] == "127.0.0.1"

def test_log_execution_time_decorator():
    """Testa o decorador log_execution_time."""
    mock_logger = MagicMock()
    
    @log_execution_time(mock_logger, "test_function")
    def test_function():
        import time
        time.sleep(0.001)  # Pequeno delay para garantir tempo > 0
        return "success"
    
    result = test_function()
    
    assert result == "success"
    mock_logger.log_performance.assert_called_once()
    call_args = mock_logger.log_performance.call_args
    assert call_args[0][0] == "test_function"  # operation
    assert call_args[0][1] > 0  # duration
    assert call_args[1]["success"] is True

def test_log_execution_time_with_exception():
    """Testa o decorador log_execution_time com exceção."""
    mock_logger = MagicMock()
    
    @log_execution_time(mock_logger, "test_function_with_error")
    def test_function_with_error():
        import time
        time.sleep(0.001)  # Pequeno delay para garantir tempo > 0
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        test_function_with_error()
    
    mock_logger.log_performance.assert_called_once()
    call_args = mock_logger.log_performance.call_args
    assert call_args[0][0] == "test_function_with_error"  # operation
    assert call_args[0][1] > 0  # duration
    assert call_args[1]["success"] is False
    assert "Test error" in call_args[1]["error"]

def test_logger_with_none_values():
    """Testa logging com valores None."""
    with patch.object(logger.logger, 'info') as mock_info:
        logger.info("Test with None", user_id=None, data=None)
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == "Test with None"
        # Valores None não devem aparecer no JSON final
        assert "user_id" not in log_data
        assert "data" not in log_data

def test_logger_with_complex_objects():
    """Testa logging com objetos complexos."""
    with patch.object(logger.logger, 'info') as mock_info:
        complex_data = {
            "list": [1, 2, 3],
            "dict": {"nested": {"key": "value"}},
            "tuple": (1, 2, 3)
        }
        
        logger.info("Complex data", data=complex_data)
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == "Complex data"
        assert log_data["data"]["list"] == [1, 2, 3]
        assert log_data["data"]["dict"]["nested"]["key"] == "value"
        # Tuples são convertidos para listas no JSON
        assert log_data["data"]["tuple"] == [1, 2, 3]

def test_logger_with_special_characters():
    """Testa logging com caracteres especiais."""
    with patch.object(logger.logger, 'info') as mock_info:
        special_message = "Test with ç, ã, é, ñ, 🚀, 💻"
        logger.info(special_message, special_field="áéíóú")
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == special_message
        assert log_data["special_field"] == "áéíóú"

def test_logger_performance():
    """Testa performance do logger com múltiplas mensagens."""
    with patch.object(logger.logger, 'info') as mock_info:
        import time
        start_time = time.time()
        
        for i in range(100):
            logger.info(f"Message {i}", index=i)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert mock_info.call_count == 100
        assert execution_time < 1.0  # Deve ser rápido

def test_logger_thread_safety():
    """Testa se o logger é thread-safe."""
    import threading
    import time
    
    results = []
    
    def worker(thread_id):
        for i in range(10):
            logger.info(f"Thread {thread_id} message {i}", thread_id=thread_id, message_id=i)
            time.sleep(0.001)  # Pequena pausa
        results.append(f"Thread {thread_id} completed")
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    assert len(results) == 5
    for result in results:
        assert "completed" in result

def test_logger_log_chat_request():
    """Testa logging específico de chat."""
    with patch.object(logger.logger, 'info') as mock_info:
        logger.log_chat_request(
            question="Qual sua experiência?",
            role="recruiter",
            response_time=2.5,
            cache_hit=True,
            relevant_fields=["skills", "experience"]
        )
        
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == "Chat request processed"
        assert log_data["question_preview"] == "Qual sua experiência?"
        assert log_data["role"] == "recruiter"
        assert log_data["response_time_ms"] == 2500.0
        assert log_data["cache_hit"] is True
        assert log_data["relevant_fields"] == ["skills", "experience"]

def test_logger_log_performance():
    """Testa logging de performance."""
    with patch.object(logger.logger, 'info') as mock_info:
        logger.log_performance(
            operation="database_query",
            duration=0.5,
            query_type="SELECT",
            rows_returned=100
        )
        
        mock_info.assert_called_once()
        call_args = mock_info.call_args[0][0]
        log_data = json.loads(call_args)
        
        assert log_data["message"] == "Performance: database_query"
        assert log_data["operation"] == "database_query"
        assert log_data["duration_ms"] == 500.0
        assert log_data["query_type"] == "SELECT"
        assert log_data["rows_returned"] == 100 