import json
import os
from typing import Dict, Optional, List

class RoleHandler:
    """
    Classe para gerenciar configurações de roles personalizadas.
    Responsável por carregar, validar e gerar prompts baseados em roles.
    """
    
    def __init__(self, roles_dir: str = None):
        """
        Inicializa o RoleHandler.
        
        Args:
            roles_dir (str): Diretório onde estão os arquivos JSON das roles
        """
        # Caminho absoluto para o diretório de roles, relativo ao backend
        if roles_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            roles_dir = os.path.join(base_dir, "data", "roles")
        self.roles_dir = roles_dir
        self.roles = self.load_roles()
        self.default_role = "recruiter"
        self._cache = {}  # Cache para configurações carregadas
    
    def load_roles(self) -> Dict:
        """
        Carrega todas as roles do diretório de configuração.
        
        Returns:
            Dict: Dicionário com todas as roles carregadas
        """
        roles = {}
        if os.path.exists(self.roles_dir):
            for filename in os.listdir(self.roles_dir):
                if filename.endswith('.json'):
                    role_id = filename.replace('.json', '')
                    role_path = os.path.join(self.roles_dir, filename)
                    try:
                        with open(role_path, 'r', encoding='utf-8') as f:
                            role_config = json.load(f)
                            # Validar schema básico
                            if self._validate_role_schema(role_config):
                                roles[role_id] = role_config
                            else:
                                print(f"Warning: Role {role_id} has invalid schema")
                    except Exception as e:
                        print(f"Erro ao carregar role {role_id}: {e}")
        else:
            print(f"Warning: Diretório de roles não encontrado: {self.roles_dir}")
        
        return roles
    
    def _validate_role_schema(self, role_config: Dict) -> bool:
        """
        Valida se a configuração da role segue o schema esperado.
        
        Args:
            role_config (Dict): Configuração da role para validar
            
        Returns:
            bool: True se válido, False caso contrário
        """
        required_fields = ['id', 'name', 'description', 'icon', 'color']
        
        for field in required_fields:
            if field not in role_config:
                print(f"Campo obrigatório '{field}' não encontrado na role")
                return False
        
        # Validar tipos básicos
        if not isinstance(role_config.get('focus_areas'), list):
            print("focus_areas deve ser uma lista")
            return False
        
        if not isinstance(role_config.get('prompt_modifiers'), dict):
            print("prompt_modifiers deve ser um dicionário")
            return False
        
        return True
    
    def get_role_config(self, role_id: str) -> Optional[Dict]:
        """
        Retorna configuração específica da role.
        
        Args:
            role_id (str): ID da role desejada
            
        Returns:
            Optional[Dict]: Configuração da role ou None se não encontrada
        """
        # Verificar cache primeiro
        if role_id in self._cache:
            return self._cache[role_id]
        
        role_config = self.roles.get(role_id, self.roles.get(self.default_role))
        
        # Adicionar ao cache se encontrada
        if role_config:
            self._cache[role_id] = role_config
        
        return role_config
    
    def generate_role_prompt(self, role_id: str, base_prompt: str) -> str:
        """
        Gera prompt personalizado baseado na role.
        
        Args:
            role_id (str): ID da role
            base_prompt (str): Prompt base do sistema
            
        Returns:
            str: Prompt personalizado para a role
        """
        role_config = self.get_role_config(role_id)
        if not role_config:
            print(f"Warning: Role {role_id} não encontrada, usando role padrão")
            return base_prompt
        
        modifiers = role_config.get('prompt_modifiers', {})
        
        # Construir prompt personalizado
        personalized_prompt = base_prompt + "\n\n"
        personalized_prompt += f"CONTEXTO ESPECÍFICO PARA {role_config['name'].upper()}:\n"
        personalized_prompt += f"{modifiers.get('prefix', '')}\n\n"
        
        if 'emphasis' in modifiers and modifiers['emphasis']:
            personalized_prompt += "FOQUE EM:\n"
            for item in modifiers['emphasis']:
                personalized_prompt += f"- {item}\n"
            personalized_prompt += "\n"
        
        if 'avoid' in modifiers and modifiers['avoid']:
            personalized_prompt += "EVITE:\n"
            for item in modifiers['avoid']:
                personalized_prompt += f"- {item}\n"
            personalized_prompt += "\n"
        
        return personalized_prompt
    
    def validate_role(self, role_id: str) -> bool:
        """
        Valida se a role existe.
        
        Args:
            role_id (str): ID da role para validar
            
        Returns:
            bool: True se a role existe, False caso contrário
        """
        return role_id in self.roles
    
    def get_all_roles(self) -> List[Dict]:
        """
        Retorna lista de todas as roles disponíveis.
        
        Returns:
            List[Dict]: Lista com todas as configurações de roles
        """
        return list(self.roles.values())
    
    def get_role_examples(self, role_id: str) -> List[str]:
        """
        Retorna exemplos de perguntas para a role.
        
        Args:
            role_id (str): ID da role
            
        Returns:
            List[str]: Lista de exemplos de perguntas
        """
        role_config = self.get_role_config(role_id)
        return role_config.get('example_questions', []) if role_config else []
    
    def get_role_by_name(self, name: str) -> Optional[Dict]:
        """
        Busca role pelo nome.
        
        Args:
            name (str): Nome da role
            
        Returns:
            Optional[Dict]: Configuração da role ou None se não encontrada
        """
        for role in self.roles.values():
            if role.get('name', '').lower() == name.lower():
                return role
        return None
    
    def clear_cache(self):
        """Limpa o cache de configurações."""
        self._cache.clear()
    
    def reload_roles(self):
        """Recarrega todas as roles do diretório."""
        self.clear_cache()
        self.roles = self.load_roles()
    
    def get_available_roles(self) -> List[str]:
        """
        Retorna lista de IDs das roles disponíveis.
        
        Returns:
            List[str]: Lista de IDs das roles
        """
        return list(self.roles.keys())
    
    def get_role_summary(self, role_id: str) -> Optional[Dict]:
        """
        Retorna um resumo da role (sem prompt_modifiers).
        
        Args:
            role_id (str): ID da role
            
        Returns:
            Optional[Dict]: Resumo da role ou None se não encontrada
        """
        role_config = self.get_role_config(role_id)
        if not role_config:
            return None
        
        # Retornar apenas campos de resumo
        summary_fields = ['id', 'name', 'description', 'icon', 'color', 'focus_areas', 'tone']
        return {field: role_config.get(field) for field in summary_fields if field in role_config} 