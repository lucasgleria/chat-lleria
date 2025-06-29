import os
import shutil
import pytest
from utils.cache_handler import CacheHandler

@pytest.fixture(scope="function")
def temp_cache_dir():
    cache_dir = "test_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    os.makedirs(cache_dir)
    yield cache_dir
    shutil.rmtree(cache_dir)

@pytest.fixture
def cache_handler(temp_cache_dir):
    return CacheHandler(cache_dir=temp_cache_dir, max_age_hours=0.001)  # 3.6 segundos para expirar

def test_cache_set_and_get(cache_handler):
    question = "Qual a formação acadêmica?"
    role = "recruiter"
    relevant_fields = ["academic_background"]
    answer = "Lucas é formado em ..."
    factual_data = {"academic_background": ["Engenharia"]}

    # Deve estar vazio inicialmente
    assert cache_handler.get(question, role, relevant_fields) is None

    # Armazenar no cache
    assert cache_handler.set(question, role, relevant_fields, answer, factual_data)

    # Recuperar do cache
    cached = cache_handler.get(question, role, relevant_fields)
    assert cached is not None
    assert cached['answer'] == answer
    assert cached['factual_data'] == factual_data


def test_cache_expiration(cache_handler):
    question = "Qual a formação acadêmica?"
    role = "recruiter"
    relevant_fields = ["academic_background"]
    answer = "Lucas é formado em ..."
    factual_data = {"academic_background": ["Engenharia"]}

    cache_handler.set(question, role, relevant_fields, answer, factual_data)
    assert cache_handler.get(question, role, relevant_fields) is not None

    # Espera expirar
    import time
    time.sleep(4)
    assert cache_handler.get(question, role, relevant_fields) is None


def test_cache_clear_all(cache_handler):
    question = "Qual a formação acadêmica?"
    role = "recruiter"
    relevant_fields = ["academic_background"]
    answer = "Lucas é formado em ..."
    factual_data = {"academic_background": ["Engenharia"]}

    cache_handler.set(question, role, relevant_fields, answer, factual_data)
    assert cache_handler.get(question, role, relevant_fields) is not None
    removed = cache_handler.clear_all()
    assert removed == 1
    assert cache_handler.get(question, role, relevant_fields) is None


def test_cache_stats(cache_handler):
    question = "Pergunta?"
    role = "recruiter"
    relevant_fields = ["academic_background"]
    answer = "Resposta"
    factual_data = {"academic_background": ["Engenharia"]}

    cache_handler.set(question, role, relevant_fields, answer, factual_data)
    cache_handler.get(question, role, relevant_fields)
    stats = cache_handler.get_stats()
    assert stats['hits'] >= 1
    assert stats['cache_files'] == 1
    assert stats['max_age_hours'] > 0 