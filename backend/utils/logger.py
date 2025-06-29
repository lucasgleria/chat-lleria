import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import os
from functools import wraps

class StructuredLogger:
    """
    Sistema de logs estruturados para monitoramento e debugging.
    Gera logs em formato JSON para fácil análise.
    """
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        """
        Inicializa o StructuredLogger.
        
        Args:
            log_dir (str): Diretório para armazenar logs
            log_level (str): Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper())
        self._ensure_log_dir()
        self._setup_logger()
    
    def _ensure_log_dir(self):
        """Garante que o diretório de logs existe."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _setup_logger(self):
        """Configura o logger principal."""
        self.logger = logging.getLogger('gemini_chatbot')
        self.logger.setLevel(self.log_level)
        
        # Limpar handlers existentes
        self.logger.handlers.clear()
        
        # Handler para arquivo
        log_file = os.path.join(self.log_dir, f"chatbot_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # Formatter estruturado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _format_log_data(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Formata dados do log em estrutura JSON.
        
        Args:
            level (str): Nível do log
            message (str): Mensagem principal
            **kwargs: Dados adicionais
            
        Returns:
            Dict: Dados formatados
        """
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'service': 'gemini_chatbot'
        }
        
        # Adicionar dados extras
        for key, value in kwargs.items():
            if value is not None:
                log_data[key] = value
        
        return log_data
    
    def info(self, message: str, **kwargs):
        """Log de informação."""
        log_data = self._format_log_data('INFO', message, **kwargs)
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
    
    def warning(self, message: str, **kwargs):
        """Log de aviso."""
        log_data = self._format_log_data('WARNING', message, **kwargs)
        self.logger.warning(json.dumps(log_data, ensure_ascii=False))
    
    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        """Log de erro."""
        log_data = self._format_log_data('ERROR', message, **kwargs)
        
        if error:
            log_data['error_type'] = type(error).__name__
            log_data['error_message'] = str(error)
            log_data['error_traceback'] = self._get_traceback(error)
        
        self.logger.error(json.dumps(log_data, ensure_ascii=False))
    
    def debug(self, message: str, **kwargs):
        """Log de debug."""
        log_data = self._format_log_data('DEBUG', message, **kwargs)
        self.logger.debug(json.dumps(log_data, ensure_ascii=False))
    
    def _get_traceback(self, error: Exception) -> str:
        """Extrai traceback do erro."""
        import traceback
        return ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    
    def log_request(self, method: str, endpoint: str, status_code: int, 
                   response_time: float, user_agent: str = None, **kwargs):
        """
        Log específico para requisições HTTP.
        
        Args:
            method (str): Método HTTP
            endpoint (str): Endpoint acessado
            status_code (int): Código de status da resposta
            response_time (float): Tempo de resposta em segundos
            user_agent (str): User-Agent do cliente
            **kwargs: Dados adicionais
        """
        self.info(
            f"HTTP {method} {endpoint}",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            response_time_ms=round(response_time * 1000, 2),
            user_agent=user_agent,
            **kwargs
        )
    
    def log_chat_request(self, question: str, role: str, response_time: float, 
                        cache_hit: bool = False, error: str = None, **kwargs):
        """
        Log específico para requisições de chat.
        
        Args:
            question (str): Pergunta do usuário
            role (str): Role selecionada
            response_time (float): Tempo de resposta
            cache_hit (bool): Se houve hit no cache
            error (str): Erro se houver
            **kwargs: Dados adicionais
        """
        self.info(
            f"Chat request processed",
            question_preview=question[:100] + "..." if len(question) > 100 else question,
            role=role,
            response_time_ms=round(response_time * 1000, 2),
            cache_hit=cache_hit,
            error=error,
            **kwargs
        )
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """
        Log específico para métricas de performance.
        
        Args:
            operation (str): Nome da operação
            duration (float): Duração em segundos
            **kwargs: Dados adicionais
        """
        self.info(
            f"Performance: {operation}",
            operation=operation,
            duration_ms=round(duration * 1000, 2),
            **kwargs
        )

# Decorator para medir tempo de execução
def log_execution_time(logger: StructuredLogger, operation: str):
    """
    Decorator para medir e logar tempo de execução de funções.
    
    Args:
        logger (StructuredLogger): Instância do logger
        operation (str): Nome da operação
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.log_performance(operation, duration, success=True)
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.log_performance(operation, duration, success=False, error=str(e))
                raise
        return wrapper
    return decorator

# Instância global do logger
logger = StructuredLogger() 