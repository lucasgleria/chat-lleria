import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configuração base"""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    
    # Configurações de CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Configurações de cache
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hora padrão
    
    # Configurações de rate limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))  # 100 requests
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hora
    
    # Configurações de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/chatbot.log")

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    # Em produção, CORS_ORIGINS deve ser configurado via variável de ambiente
    # Exemplo: CORS_ORIGINS=https://seu-frontend.vercel.app,https://seu-dominio.com

# Configuração baseada no ambiente
def get_config():
    """Retorna a configuração apropriada baseada no ambiente"""
    env = os.getenv("FLASK_ENV", "development")
    
    if env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig() 