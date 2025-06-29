import time
from typing import Dict, Tuple, Optional
from collections import defaultdict
import threading

class RateLimiter:
    """
    Sistema de rate limiting para proteger contra spam e abuso.
    Implementa sliding window rate limiting.
    """
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Inicializa o RateLimiter.
        
        Args:
            max_requests (int): Número máximo de requisições por janela
            window_seconds (int): Tamanho da janela em segundos
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # IP -> lista de timestamps
        self.lock = threading.Lock()
    
    def _clean_old_requests(self, ip: str):
        """
        Remove requisições antigas da janela de tempo.
        
        Args:
            ip (str): IP do cliente
        """
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        # Filtrar requisições dentro da janela
        self.requests[ip] = [
            timestamp for timestamp in self.requests[ip]
            if timestamp > cutoff_time
        ]
    
    def is_allowed(self, ip: str) -> Tuple[bool, Dict[str, int]]:
        """
        Verifica se uma requisição é permitida.
        
        Args:
            ip (str): IP do cliente
            
        Returns:
            Tuple[bool, Dict]: (permitido, informações do rate limit)
        """
        with self.lock:
            self._clean_old_requests(ip)
            
            current_requests = len(self.requests[ip])
            is_allowed = current_requests < self.max_requests
            
            if is_allowed:
                self.requests[ip].append(time.time())
            
            return is_allowed, {
                'current_requests': current_requests,
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'remaining_requests': max(0, self.max_requests - current_requests)
            }
    
    def get_remaining_time(self, ip: str) -> Optional[float]:
        """
        Retorna o tempo restante até a próxima requisição ser permitida.
        
        Args:
            ip (str): IP do cliente
            
        Returns:
            Optional[float]: Tempo restante em segundos ou None se permitido
        """
        with self.lock:
            self._clean_old_requests(ip)
            
            if len(self.requests[ip]) < self.max_requests:
                return None
            
            # Tempo da requisição mais antiga
            oldest_request = min(self.requests[ip])
            return max(0, oldest_request + self.window_seconds - time.time())
    
    def reset(self, ip: str):
        """
        Reseta o rate limit para um IP específico.
        
        Args:
            ip (str): IP do cliente
        """
        with self.lock:
            self.requests[ip].clear()
    
    def get_stats(self) -> Dict[str, int]:
        """
        Retorna estatísticas do rate limiter.
        
        Returns:
            Dict: Estatísticas
        """
        with self.lock:
            total_ips = len(self.requests)
            total_requests = sum(len(requests) for requests in self.requests.values())
            
            return {
                'total_ips': total_ips,
                'total_requests': total_requests,
                'max_requests_per_window': self.max_requests,
                'window_seconds': self.window_seconds
            }

class IPRateLimiter:
    """
    Rate limiter específico para IPs com diferentes limites por tipo de endpoint.
    """
    
    def __init__(self):
        """Inicializa o IPRateLimiter com diferentes limites."""
        # Rate limiters para diferentes endpoints
        self.chat_limiter = RateLimiter(max_requests=5, window_seconds=60)  # 5 req/min para chat
        self.roles_limiter = RateLimiter(max_requests=20, window_seconds=60)  # 20 req/min para roles
        self.general_limiter = RateLimiter(max_requests=30, window_seconds=60)  # 30 req/min geral
    
    def check_rate_limit(self, ip: str, endpoint: str) -> Tuple[bool, Dict[str, int]]:
        """
        Verifica rate limit baseado no endpoint.
        
        Args:
            ip (str): IP do cliente
            endpoint (str): Endpoint acessado
            
        Returns:
            Tuple[bool, Dict]: (permitido, informações do rate limit)
        """
        if endpoint == '/chat':
            return self.chat_limiter.is_allowed(ip)
        elif endpoint == '/roles':
            return self.roles_limiter.is_allowed(ip)
        else:
            return self.general_limiter.is_allowed(ip)
    
    def get_remaining_time(self, ip: str, endpoint: str) -> Optional[float]:
        """
        Retorna tempo restante para um endpoint específico.
        
        Args:
            ip (str): IP do cliente
            endpoint (str): Endpoint acessado
            
        Returns:
            Optional[float]: Tempo restante em segundos
        """
        if endpoint == '/chat':
            return self.chat_limiter.get_remaining_time(ip)
        elif endpoint == '/roles':
            return self.roles_limiter.get_remaining_time(ip)
        else:
            return self.general_limiter.get_remaining_time(ip)
    
    def reset(self, ip: str, endpoint: str = None):
        """
        Reseta rate limit para um IP.
        
        Args:
            ip (str): IP do cliente
            endpoint (str): Endpoint específico ou None para todos
        """
        if endpoint == '/chat':
            self.chat_limiter.reset(ip)
        elif endpoint == '/roles':
            self.roles_limiter.reset(ip)
        elif endpoint is None:
            self.chat_limiter.reset(ip)
            self.roles_limiter.reset(ip)
            self.general_limiter.reset(ip)
        else:
            self.general_limiter.reset(ip)
    
    def get_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Retorna estatísticas de todos os rate limiters.
        
        Returns:
            Dict: Estatísticas organizadas por endpoint
        """
        return {
            'chat': self.chat_limiter.get_stats(),
            'roles': self.roles_limiter.get_stats(),
            'general': self.general_limiter.get_stats()
        }

# Instância global do rate limiter
rate_limiter = IPRateLimiter() 