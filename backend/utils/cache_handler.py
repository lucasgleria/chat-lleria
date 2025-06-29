import json
import hashlib
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import os

class CacheHandler:
    """
    Sistema de cache para armazenar respostas frequentes do chatbot.
    Reduz chamadas à API do Gemini e melhora performance.
    """
    
    def __init__(self, cache_dir: str = "cache", max_age_hours: int = 24):
        """
        Inicializa o CacheHandler.
        
        Args:
            cache_dir (str): Diretório para armazenar cache
            max_age_hours (int): Tempo máximo de vida do cache em horas
        """
        self.cache_dir = cache_dir
        self.max_age_seconds = max_age_hours * 3600
        self._ensure_cache_dir()
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    def _ensure_cache_dir(self):
        """Garante que o diretório de cache existe."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _generate_cache_key(self, question: str, role: str, relevant_fields: list) -> str:
        """
        Gera uma chave única para o cache baseada na pergunta, role e campos relevantes.
        
        Args:
            question (str): Pergunta do usuário
            role (str): Role selecionada
            relevant_fields (list): Campos relevantes identificados
            
        Returns:
            str: Chave única para o cache
        """
        # Normalizar a pergunta (lowercase, remover espaços extras)
        normalized_question = question.lower().strip()
        
        # Criar string para hash
        cache_string = f"{normalized_question}|{role}|{','.join(sorted(relevant_fields))}"
        
        # Gerar hash MD5
        return hashlib.md5(cache_string.encode('utf-8')).hexdigest()
    
    def _get_cache_file_path(self, cache_key: str) -> str:
        """Retorna o caminho completo do arquivo de cache."""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, question: str, role: str, relevant_fields: list) -> Optional[Dict[str, Any]]:
        """
        Busca uma resposta no cache.
        
        Args:
            question (str): Pergunta do usuário
            role (str): Role selecionada
            relevant_fields (list): Campos relevantes identificados
            
        Returns:
            Optional[Dict]: Dados do cache ou None se não encontrado/expirado
        """
        cache_key = self._generate_cache_key(question, role, relevant_fields)
        cache_file = self._get_cache_file_path(cache_key)
        
        try:
            if not os.path.exists(cache_file):
                self._cache_stats['misses'] += 1
                return None
            
            # Verificar se o cache não expirou
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age > self.max_age_seconds:
                os.remove(cache_file)
                self._cache_stats['evictions'] += 1
                self._cache_stats['misses'] += 1
                return None
            
            # Ler dados do cache
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            self._cache_stats['hits'] += 1
            print(f"DEBUG: Cache HIT for question: {question[:50]}...")
            return cache_data
            
        except Exception as e:
            print(f"DEBUG: Cache error: {e}")
            self._cache_stats['misses'] += 1
            return None
    
    def set(self, question: str, role: str, relevant_fields: list, 
            answer: str, factual_data: Dict[str, Any]) -> bool:
        """
        Armazena uma resposta no cache.
        
        Args:
            question (str): Pergunta do usuário
            role (str): Role selecionada
            relevant_fields (list): Campos relevantes identificados
            answer (str): Resposta gerada
            factual_data (Dict): Dados factuais usados
            
        Returns:
            bool: True se armazenado com sucesso
        """
        try:
            cache_key = self._generate_cache_key(question, role, relevant_fields)
            cache_file = self._get_cache_file_path(cache_key)
            
            cache_data = {
                'question': question,
                'role': role,
                'relevant_fields': relevant_fields,
                'answer': answer,
                'factual_data': factual_data,
                'created_at': datetime.now().isoformat(),
                'cache_key': cache_key
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"DEBUG: Cache SET for question: {question[:50]}...")
            return True
            
        except Exception as e:
            print(f"DEBUG: Cache SET error: {e}")
            return False
    
    def clear_expired(self) -> int:
        """
        Remove arquivos de cache expirados.
        
        Returns:
            int: Número de arquivos removidos
        """
        removed_count = 0
        current_time = time.time()
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    file_age = current_time - os.path.getmtime(file_path)
                    
                    if file_age > self.max_age_seconds:
                        os.remove(file_path)
                        removed_count += 1
            
            if removed_count > 0:
                print(f"DEBUG: Removed {removed_count} expired cache files")
                
        except Exception as e:
            print(f"DEBUG: Cache cleanup error: {e}")
        
        return removed_count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache.
        
        Returns:
            Dict: Estatísticas do cache
        """
        total_requests = self._cache_stats['hits'] + self._cache_stats['misses']
        hit_rate = (self._cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        # Contar arquivos de cache
        cache_files = 0
        try:
            cache_files = len([f for f in os.listdir(self.cache_dir) if f.endswith('.json')])
        except:
            pass
        
        return {
            'hits': self._cache_stats['hits'],
            'misses': self._cache_stats['misses'],
            'evictions': self._cache_stats['evictions'],
            'hit_rate': round(hit_rate, 2),
            'cache_files': cache_files,
            'max_age_hours': self.max_age_seconds / 3600
        }
    
    def clear_all(self) -> int:
        """
        Remove todos os arquivos de cache.
        
        Returns:
            int: Número de arquivos removidos
        """
        removed_count = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    os.remove(file_path)
                    removed_count += 1
            
            print(f"DEBUG: Cleared all cache files ({removed_count} files)")
            
        except Exception as e:
            print(f"DEBUG: Cache clear error: {e}")
        
        return removed_count 