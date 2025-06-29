import os
import json
import pytest
import tempfile
import shutil
from utils.curriculo_handler import CurriculoHandler

@pytest.fixture
def temp_data_dir():
    """Cria um diretório temporário com dados de teste."""
    temp_dir = tempfile.mkdtemp()
    
    # Criar arquivos de teste
    test_data = {
        "academic_background.json": {
            "academic_background": {
                "degree": "Engenharia de Software",
                "university": "Universidade XYZ",
                "year": 2023
            }
        },
        "skills.json": {
            "skills": {
                "programming": ["Python", "JavaScript"],
                "frameworks": ["Flask", "React"]
            }
        },
        "invalid.json": "invalid json content",
        "empty.json": {}
    }
    
    for filename, content in test_data.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(content, dict):
                json.dump(content, f, ensure_ascii=False)
            else:
                f.write(content)
    
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def curriculo_handler(temp_data_dir):
    return CurriculoHandler(data_dir=temp_data_dir)

def test_load_section_success(curriculo_handler):
    """Testa carregamento bem-sucedido de uma seção."""
    data = curriculo_handler.load_section("academic_background")
    assert data is not None
    assert "degree" in data
    assert data["degree"] == "Engenharia de Software"

def test_load_section_cache(curriculo_handler):
    """Testa se o cache interno funciona corretamente."""
    # Primeira chamada
    data1 = curriculo_handler.load_section("academic_background")
    # Segunda chamada deve usar cache
    data2 = curriculo_handler.load_section("academic_background")
    
    assert data1 == data2
    assert id(data1) == id(data2)  # Mesmo objeto em memória

def test_load_section_not_found(curriculo_handler):
    """Testa comportamento quando arquivo não existe."""
    data = curriculo_handler.load_section("nonexistent")
    assert data is None

def test_load_section_invalid_json(curriculo_handler):
    """Testa comportamento com JSON inválido."""
    data = curriculo_handler.load_section("invalid")
    assert data is None

def test_load_section_empty_file(curriculo_handler):
    """Testa comportamento com arquivo vazio."""
    data = curriculo_handler.load_section("empty")
    assert data is not None
    assert data == {}

def test_get_method(curriculo_handler):
    """Testa o método get (alias para load_section)."""
    data = curriculo_handler.get("academic_background")
    assert data is not None
    assert "degree" in data

def test_get_multiple_sections(curriculo_handler):
    """Testa carregamento de múltiplas seções."""
    sections = ["academic_background", "skills"]
    result = curriculo_handler.get_multiple(sections)
    
    assert len(result) == 2
    assert "academic_background" in result
    assert "skills" in result
    assert result["academic_background"]["degree"] == "Engenharia de Software"
    assert "programming" in result["skills"]

def test_get_multiple_with_invalid_sections(curriculo_handler):
    """Testa get_multiple com seções inválidas."""
    sections = ["academic_background", "nonexistent", "invalid"]
    result = curriculo_handler.get_multiple(sections)
    
    assert len(result) == 1  # Apenas academic_background deve ser carregado
    assert "academic_background" in result
    assert "nonexistent" not in result
    assert "invalid" not in result

def test_get_multiple_empty_list(curriculo_handler):
    """Testa get_multiple com lista vazia."""
    result = curriculo_handler.get_multiple([])
    assert result == {}

def test_data_structure_without_section_key(curriculo_handler):
    """Testa quando o JSON não tem a chave da seção."""
    # Criar arquivo sem a chave da seção
    temp_file = os.path.join(curriculo_handler.data_dir, "direct_data.json")
    direct_data = {"name": "Lucas", "age": 25}
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(direct_data, f)
    
    # Testar carregamento
    data = curriculo_handler.load_section("direct_data")
    assert data == direct_data
    
    # Limpar arquivo temporário
    os.remove(temp_file) 