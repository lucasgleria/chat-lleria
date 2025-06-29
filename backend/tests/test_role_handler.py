import os
import json
import pytest
import tempfile
import shutil
from utils.role_handler import RoleHandler

@pytest.fixture
def temp_roles_dir():
    """Cria um diretório temporário com roles de teste."""
    temp_dir = tempfile.mkdtemp()
    roles_dir = os.path.join(temp_dir, "roles")
    os.makedirs(roles_dir)
    
    # Criar roles de teste
    test_roles = {
        "recruiter.json": {
            "id": "recruiter",
            "name": "Recruiter",
            "description": "Para recrutadores",
            "icon": "👔",
            "color": "#3B82F6",
            "focus_areas": ["academic_background", "professional_experience", "skills"],
            "prompt_modifiers": {
                "prefix": "Foque em experiência profissional e habilidades técnicas",
                "emphasis": ["Experiência relevante", "Habilidades técnicas"],
                "avoid": ["Informações pessoais desnecessárias"]
            },
            "example_questions": [
                "Qual sua experiência com Python?",
                "Quais projetos você desenvolveu?"
            ]
        },
        "developer.json": {
            "id": "developer",
            "name": "Developer",
            "description": "Para desenvolvedores",
            "icon": "💻",
            "color": "#10B981",
            "focus_areas": ["skills", "projects", "technical_background"],
            "prompt_modifiers": {
                "prefix": "Foque em aspectos técnicos e projetos",
                "emphasis": ["Stack tecnológico", "Projetos open source"],
                "avoid": ["Informações não técnicas"]
            },
            "example_questions": [
                "Como você resolveria este problema?",
                "Qual sua stack preferida?"
            ]
        },
        "invalid.json": {
            "id": "invalid",
            "name": "Invalid",
            # Faltando campos obrigatórios
        },
        "malformed.json": "invalid json content"
    }
    
    for filename, content in test_roles.items():
        filepath = os.path.join(roles_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(content, dict):
                json.dump(content, f, ensure_ascii=False)
            else:
                f.write(content)
    
    yield roles_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def role_handler(temp_roles_dir):
    return RoleHandler(roles_dir=temp_roles_dir)

def test_load_roles_success(role_handler):
    """Testa carregamento bem-sucedido de roles."""
    roles = role_handler.roles
    assert len(roles) == 2  # Apenas recruiter e developer devem ser carregados
    assert "recruiter" in roles
    assert "developer" in roles
    assert "invalid" not in roles  # Role inválida não deve ser carregada

def test_validate_role_schema_valid(role_handler):
    """Testa validação de schema válido."""
    valid_role = {
        "id": "test",
        "name": "Test",
        "description": "Test role",
        "icon": "🧪",
        "color": "#000000",
        "focus_areas": ["skills"],
        "prompt_modifiers": {"prefix": "test"}
    }
    assert role_handler._validate_role_schema(valid_role) is True

def test_validate_role_schema_invalid(role_handler):
    """Testa validação de schema inválido."""
    invalid_roles = [
        {"id": "test"},  # Faltando campos obrigatórios
        {"id": "test", "name": "Test", "description": "Test", "icon": "🧪", "color": "#000", "focus_areas": "not_a_list"},  # focus_areas não é lista
        {"id": "test", "name": "Test", "description": "Test", "icon": "🧪", "color": "#000", "focus_areas": [], "prompt_modifiers": "not_a_dict"}  # prompt_modifiers não é dict
    ]
    
    for invalid_role in invalid_roles:
        assert role_handler._validate_role_schema(invalid_role) is False

def test_get_role_config_existing(role_handler):
    """Testa obtenção de configuração de role existente."""
    config = role_handler.get_role_config("recruiter")
    assert config is not None
    assert config["id"] == "recruiter"
    assert config["name"] == "Recruiter"

def test_get_role_config_nonexistent(role_handler):
    """Testa obtenção de configuração de role inexistente."""
    config = role_handler.get_role_config("nonexistent")
    assert config is not None  # Deve retornar role padrão (recruiter)
    assert config["id"] == "recruiter"

def test_get_role_config_cache(role_handler):
    """Testa se o cache de configurações funciona."""
    # Primeira chamada
    config1 = role_handler.get_role_config("recruiter")
    # Segunda chamada deve usar cache
    config2 = role_handler.get_role_config("recruiter")
    
    assert config1 == config2
    assert id(config1) == id(config2)  # Mesmo objeto em memória

def test_generate_role_prompt(role_handler):
    """Testa geração de prompt personalizado."""
    base_prompt = "Você é um assistente de currículo."
    personalized = role_handler.generate_role_prompt("recruiter", base_prompt)
    
    assert base_prompt in personalized
    assert "RECRUITER" in personalized.upper()
    assert "Foque em experiência profissional" in personalized
    assert "Experiência relevante" in personalized
    assert "Informações pessoais desnecessárias" in personalized

def test_generate_role_prompt_nonexistent(role_handler):
    """Testa geração de prompt para role inexistente."""
    base_prompt = "Você é um assistente de currículo."
    personalized = role_handler.generate_role_prompt("nonexistent", base_prompt)
    
    # Deve retornar prompt base + contexto da role padrão
    assert base_prompt in personalized
    # Como não existe, usa a role padrão (recruiter)
    assert "RECRUITER" in personalized.upper()

def test_validate_role(role_handler):
    """Testa validação de roles."""
    assert role_handler.validate_role("recruiter") is True
    assert role_handler.validate_role("developer") is True
    assert role_handler.validate_role("nonexistent") is False

def test_get_all_roles(role_handler):
    """Testa obtenção de todas as roles."""
    all_roles = role_handler.get_all_roles()
    assert len(all_roles) == 2
    role_ids = [role["id"] for role in all_roles]
    assert "recruiter" in role_ids
    assert "developer" in role_ids

def test_get_role_examples(role_handler):
    """Testa obtenção de exemplos de perguntas."""
    examples = role_handler.get_role_examples("recruiter")
    assert len(examples) == 2
    assert "Qual sua experiência com Python?" in examples
    assert "Quais projetos você desenvolveu?" in examples

def test_get_role_examples_nonexistent(role_handler):
    """Testa obtenção de exemplos para role inexistente."""
    examples = role_handler.get_role_examples("nonexistent")
    # Como não existe, usa a role padrão (recruiter)
    assert len(examples) == 2
    assert "Qual sua experiência com Python?" in examples

def test_get_role_by_name(role_handler):
    """Testa busca de role por nome."""
    role = role_handler.get_role_by_name("Recruiter")
    assert role is not None
    assert role["id"] == "recruiter"
    
    role = role_handler.get_role_by_name("nonexistent")
    assert role is None

def test_clear_cache(role_handler):
    """Testa limpeza do cache."""
    # Carregar uma role para popular o cache
    role_handler.get_role_config("recruiter")
    assert len(role_handler._cache) > 0
    
    # Limpar cache
    role_handler.clear_cache()
    assert len(role_handler._cache) == 0

def test_reload_roles(role_handler):
    """Testa recarregamento de roles."""
    initial_count = len(role_handler.roles)
    
    # Recarregar
    role_handler.reload_roles()
    
    # Verificar se ainda tem o mesmo número de roles
    assert len(role_handler.roles) == initial_count

def test_identify_relevant_fields(role_handler):
    """Testa identificação de campos relevantes."""
    question = "Qual sua experiência com Python?"
    role = "recruiter"
    
    fields = role_handler.identify_relevant_fields(question, role)
    assert isinstance(fields, list)
    assert len(fields) > 0

def test_identify_relevant_fields_nonexistent_role(role_handler):
    """Testa identificação de campos para role inexistente."""
    question = "Qual sua experiência?"
    role = "nonexistent"
    
    fields = role_handler.identify_relevant_fields(question, role)
    assert isinstance(fields, list)
    # Deve retornar campos padrão ou vazio

def test_get_available_roles(role_handler):
    """Testa obtenção de IDs de roles disponíveis."""
    available = role_handler.get_available_roles()
    assert isinstance(available, list)
    assert "recruiter" in available
    assert "developer" in available
    assert len(available) == 2

def test_get_role_summary(role_handler):
    """Testa obtenção de resumo da role."""
    summary = role_handler.get_role_summary("recruiter")
    assert summary is not None
    assert "id" in summary
    assert "name" in summary
    assert "description" in summary

def test_get_role_summary_nonexistent(role_handler):
    """Testa obtenção de resumo para role inexistente."""
    summary = role_handler.get_role_summary("nonexistent")
    # Como não existe, usa a role padrão (recruiter)
    assert summary is not None
    assert summary["id"] == "recruiter" 