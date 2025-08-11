import json
import os
from typing import Dict, Optional, List
import re

class RoleHandler:
    def __init__(self, roles_dir: str = None):
        if roles_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            roles_dir = os.path.join(base_dir, "data", "roles")
        self.roles_dir = roles_dir
        self.roles = self.load_roles()
        self.default_role = "recruiter"
        self._cache = {} 
    
    def load_roles(self) -> Dict:
        roles = {}
        if os.path.exists(self.roles_dir):
            for filename in os.listdir(self.roles_dir):
                if filename.endswith('.json'):
                    role_id = filename.replace('.json', '')
                    role_path = os.path.join(self.roles_dir, filename)
                    try:
                        with open(role_path, 'r', encoding='utf-8') as f:
                            role_config = json.load(f)
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
        required_fields = ['id', 'name', 'description', 'icon', 'color']
        
        for field in required_fields:
            if field not in role_config:
                print(f"Campo obrigatório '{field}' não encontrado na role")
                return False
        
        if not isinstance(role_config.get('focus_areas'), list):
            print("focus_areas deve ser uma lista")
            return False
        
        if not isinstance(role_config.get('prompt_modifiers'), dict):
            print("prompt_modifiers deve ser um dicionário")
            return False
        
        return True
    
    def get_role_config(self, role_id: str) -> Optional[Dict]:
        if role_id in self._cache:
            return self._cache[role_id]
        
        role_config = self.roles.get(role_id, self.roles.get(self.default_role))
        
        if role_config:
            self._cache[role_id] = role_config
        
        return role_config
    
    def generate_role_prompt(self, role_id: str, base_prompt: str) -> str:
        role_config = self.get_role_config(role_id)
        if not role_config:
            print(f"Warning: Role {role_id} não encontrada, usando role padrão")
            return base_prompt
        
        modifiers = role_config.get('prompt_modifiers', {})
        
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
        return role_id in self.roles
    
    def get_all_roles(self) -> List[Dict]:
        return list(self.roles.values())
    
    def get_role_examples(self, role_id: str) -> List[str]:
        role_config = self.get_role_config(role_id)
        return role_config.get('example_questions', []) if role_config else []
    
    def get_role_by_name(self, name: str) -> Optional[Dict]:
        for role in self.roles.values():
            if role.get('name', '').lower() == name.lower():
                return role
        return None
    
    def clear_cache(self):
        self._cache.clear()
    
    def reload_roles(self):
        self.clear_cache()
        self.roles = self.load_roles()
    
    def get_available_roles(self) -> List[str]:
        return list(self.roles.keys())
    
    def get_role_summary(self, role_id: str) -> Optional[Dict]:
        role_config = self.get_role_config(role_id)
        if not role_config:
            return None
        
        summary_fields = ['id', 'name', 'description', 'icon', 'color', 'focus_areas', 'tone']
        return {field: role_config.get(field) for field in summary_fields if field in role_config}
    
    def identify_relevant_fields(self, question: str, role_id: str) -> list:
        context_patterns = {
            'academic_background': [r'formou.*em', r'graduou.*em', r'fez.*faculdade', r'estudou.*na'],
            'professional_experience': [r'trabalhou.*na', r'atuou.*como', r'experiência.*com', r'empresa.*onde'],
            'projects': [r'projeto.*chamado', r'projeto.*envolvendo', r'desenvolveu.*um', r'criou.*um'],
            'skills': [r'conhecimento.*em', r'habilidade.*com', r'domina.*', r'experiência.*com'],
            'certifications': [r'certificado.*em', r'certificação.*de', r'curso.*sobre'],
            'soft_skills': [r'habilidade.*comportamental', r'comunicação.*com', r'trabalho.*equipe'],
            'intelligent_responses': [r'conquista.*importante', r'resultado.*alcançado', r'aprendizado.*com']
        }
        
        keywords_map = {
            'academic_background': ['formação', 'formacao', 'academic', 'educação', 'education', 'graduação', 'graduacao', 'universidade', 'college', 'school', 'curso', 'diploma'],
            'professional_experience': ['experiência', 'experiencia', 'trabalho', 'emprego', 'cargo', 'empresa', 'profissional', 'job', 'work', 'role', 'position', 'company'],
            'projects': ['projeto', 'project', 'portfolio', 'case study', 'desenvolvimento de projeto', 'projeto de sistema', 'projeto desenvolvido'],
            'skills': ['habilidade', 'skill', 'competência', 'competencia', 'tecnologia', 'tecnologias', 'stack', 'linguagem', 'framework', 'ferramenta'],
            'certifications': ['certificado', 'certificação', 'certification', 'course', 'curso', 'licença', 'licenca'],
            'soft_skills': ['soft skill', 'comportamental', 'liderança', 'lideranca', 'comunicação', 'comunicacao', 'trabalho em equipe', 'teamwork', 'colaboração', 'collaboration'],
            'intelligent_responses': ['conquista', 'achievement', 'impacto', 'impact', 'resolução', 'solução', 'problem', 'solution', 'aprendizado', 'learning', 'adaptação', 'adaptability', 'progressão', 'progression', 'evolução', 'growth', 'mentoria', 'mentorship']
        }
        
        # Prioridade por role
        role_priority = {
            'recruiter': ['professional_experience', 'soft_skills', 'certifications', 'intelligent_responses', 'academic_background'],
            'developer': ['skills', 'professional_experience', 'projects', 'intelligent_responses'],
            'client': ['professional_experience', 'projects', 'intelligent_responses'],
            'student': ['academic_background', 'skills', 'projects', 'intelligent_responses']
        }
        
        found_fields = set()
        q_lower = question.lower()
        
        # 1. Verificar padrões contextuais (maior prioridade)
        context_matches = {}
        for field, patterns in context_patterns.items():
            for pattern in patterns:
                if re.search(pattern, q_lower):
                    found_fields.add(field)
                    context_matches[field] = True
                    break
        
        # 2. Se não encontrou padrões contextuais, verificar keywords com word boundaries
        if not found_fields:
            for field, keywords in keywords_map.items():
                for kw in keywords:
                    # Usar regex para corresponder apenas a palavras inteiras
                    pattern = r'\b' + re.escape(kw) + r'\b'
                    if re.search(pattern, q_lower):
                        found_fields.add(field)
                        break
        
        # 3. Se ainda não encontrou campos, usar prioridade da role
        if not found_fields and role_id in role_priority:
            found_fields.update(role_priority[role_id])
        
        # Limitar o número de campos para não sobrecarregar o modelo
        if len(found_fields) > 3:
            # Priorizar campos que corresponderam a padrões contextuais
            priority_list = []
            
            # Primeiro adicionar campos com correspondência contextual
            for field in context_matches:
                if field in found_fields:
                    priority_list.append(field)
            
            # Depois adicionar outros campos de acordo com a prioridade da role
            role_priority_order = role_priority.get(role_id, list(keywords_map.keys()))
            for field in role_priority_order:
                if field in found_fields and field not in priority_list:
                    priority_list.append(field)
                    if len(priority_list) >= 3:
                        break
            
            # Se ainda não temos 3 campos, adicionar os restantes
            for field in found_fields:
                if field not in priority_list:
                    priority_list.append(field)
                    if len(priority_list) >= 3:
                        break
            
            found_fields = set(priority_list[:3])
        
        # Logging para depuração
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Question: {question}")
        logger.info(f"Found fields: {found_fields}")
        if not found_fields and role_id in role_priority:
            logger.info(f"Using fallback for role {role_id}: {role_priority[role_id]}")
        
        return list(found_fields)