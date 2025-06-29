import time
import pytest
from utils.rate_limiter import RateLimiter, IPRateLimiter

def test_rate_limiter_basic():
    limiter = RateLimiter(max_requests=3, window_seconds=2)
    ip = '127.0.0.1'
    # Deve permitir as 3 primeiras
    assert limiter.is_allowed(ip)[0]
    assert limiter.is_allowed(ip)[0]
    assert limiter.is_allowed(ip)[0]
    # A quarta deve ser bloqueada
    allowed, info = limiter.is_allowed(ip)
    assert not allowed
    assert info['remaining_requests'] == 0
    # Espera expirar
    time.sleep(2.1)
    assert limiter.is_allowed(ip)[0]

def test_rate_limiter_reset():
    limiter = RateLimiter(max_requests=2, window_seconds=10)
    ip = '192.168.0.1'
    assert limiter.is_allowed(ip)[0]
    assert limiter.is_allowed(ip)[0]
    assert not limiter.is_allowed(ip)[0]
    limiter.reset(ip)
    assert limiter.is_allowed(ip)[0]

def test_ip_rate_limiter():
    ip_limiter = IPRateLimiter()
    ip = '10.0.0.1'
    # Testa limites diferentes para endpoints
    for _ in range(5):
        assert ip_limiter.check_rate_limit(ip, '/chat')[0]
    assert not ip_limiter.check_rate_limit(ip, '/chat')[0]
    ip_limiter.reset(ip, '/chat')
    assert ip_limiter.check_rate_limit(ip, '/chat')[0]
    for _ in range(20):
        assert ip_limiter.check_rate_limit(ip, '/roles')[0]
    assert not ip_limiter.check_rate_limit(ip, '/roles')[0]
    ip_limiter.reset(ip, '/roles')
    assert ip_limiter.check_rate_limit(ip, '/roles')[0]
    for _ in range(30):
        assert ip_limiter.check_rate_limit(ip, '/outro')[0]
    assert not ip_limiter.check_rate_limit(ip, '/outro')[0]
    ip_limiter.reset(ip)
    assert ip_limiter.check_rate_limit(ip, '/chat')[0]
    assert ip_limiter.check_rate_limit(ip, '/roles')[0]
    assert ip_limiter.check_rate_limit(ip, '/outro')[0] 