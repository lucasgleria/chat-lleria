from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import time
from utils.role_handler import RoleHandler
from utils.curriculo_handler import CurriculoHandler
from utils.cache_handler import CacheHandler
from utils.logger import logger, log_execution_time
from utils.rate_limiter import rate_limiter
import sys
import re
import unicodedata
import difflib

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# --- Initial configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Em ambiente de teste, não falhar se a chave não estiver presente
    if os.getenv("TESTING") or "pytest" in sys.modules:
        api_key = "test_key_for_testing"
        print("⚠️  Running in test mode - using dummy API key")
    else:
        # Levanta um erro se a chave API não for encontrada, impedindo que o app inicie sem ela.
        raise ValueError("GEMINI_API_KEY not found in environment variables. "
                         "Ensure it is in the .env file and you are running the script with `python main.py`.")

# Configurações de CORS para permitir requisições do frontend (localhost:3000)
# resources={r"/*": {"origins": "*"}} permite requisições de qualquer origem.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Só configurar o Gemini se não estivermos em modo de teste
if not os.getenv("TESTING") and "pytest" not in sys.modules:
    genai.configure(api_key=api_key)

# Inicializar handlers
role_handler = RoleHandler()
curriculo_handler = CurriculoHandler()
cache_handler = CacheHandler()

# --- Gemini API Key Rotation ---
class GeminiAPIKeyManager:
    def __init__(self):
        self.api_keys = [
            os.getenv("GEMINI_API_KEY"),
            os.getenv("GEMINI_KEY_API2")
        ]
        self.current_index = 0
        self.last_error = None

    def get_current_key(self):
        return self.api_keys[self.current_index]

    def switch_key(self):
        if self.current_index == 0 and self.api_keys[1]:
            self.current_index = 1
            return True
        return False

    def reset(self):
        self.current_index = 0
        self.last_error = None

# Instanciar o gerenciador de chaves
key_manager = GeminiAPIKeyManager()

# Função para gerar conteúdo com fallback de chave
from google import genai

def gemini_generate_content(system_instruction, prompt):
    """Gera conteúdo usando o Gemini, alternando a chave se necessário."""
    for attempt in range(2):
        client = genai.Client(api_key=key_manager.get_current_key())
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash-latest",
                contents=prompt,
                config={
                    "system_instruction": system_instruction
                }
            )
            return response.text
        except Exception as e:
            # Tenta identificar erro de quota excedida (429) apenas pela mensagem
            if 'quota' in str(e).lower() or '429' in str(e):
                if key_manager.switch_key():
                    continue
                else:
                    raise e
            else:
                raise e
    raise RuntimeError("Todas as chaves da API Gemini excederam a quota diária.")

# --- Here we load and build a system instruction to JSON file ---
@log_execution_time(logger, "build_system_instruction")
def build_system_instruction(instruction_data: dict) -> str:
    """
    Build a complete string of instruction system from the dict in JSON.
    This function processes a dictionary to create a structured system instruction string
    for the generative AI model, including role definition, core rules, and advanced behaviors.
    """
    instruction_parts = []
    
    # Get the first system instruction from the 'sys' array
    if "sys" in instruction_data and instruction_data["sys"]:
        sys_instruction = instruction_data["sys"][0]  # Use the first instruction
        
        if "role_definition" in sys_instruction:
            role = sys_instruction["role_definition"]
            instruction_parts.append(f"{role.get('purpose', '')}")

        instruction_parts.append("\nIMPORTANT Rules:")
        if "core_rules" in sys_instruction:
            # Itera sobre as regras principais, adicionando-as e seus exemplos.
            for key, rule_data in sys_instruction["core_rules"].items():
                # Usa len(instruction_parts) para numerar as regras dinamicamente.
                instruction_parts.append(f"{len(instruction_parts)}. {rule_data.get('title', key)}: {rule_data.get('instruction', '')}")
                if "examples" in rule_data and rule_data["examples"]:
                    instruction_parts.append("    Examples:")
                    for example in rule_data["examples"]:
                        instruction_parts.append(f"    - {example}")

        instruction_parts.append("\nAdvanced Behaviors:")
        if "advanced_behaviors" in sys_instruction:
            # Itera sobre os comportamentos avançados.
            for key, rule_data in sys_instruction["advanced_behaviors"].items():
                instruction_parts.append(f"{len(instruction_parts)}. {rule_data.get('title', key)}: {rule_data.get('instruction', '')}")

    return "\n".join(instruction_parts)

try:
    with open("data/system_instruction.json", "r", encoding="utf-8") as f:
        instruction_json_data = json.load(f)
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = build_system_instruction(instruction_json_data)

    if not SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT.strip():
        raise ValueError("System instruction built from JSON is empty.")

except FileNotFoundError:
    logger.error("System instruction file not found", error=FileNotFoundError("data/system_instruction.json"))
    # Fallback para uma instrução padrão se o arquivo não for encontrado.
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = "You are an AI assistant for Lucas's resume. Please provide relevant information."
except json.JSONDecodeError as e:
    logger.error("Invalid JSON in system instruction file", error=e)
    # Fallback se o JSON for inválido.
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = "You are an AI assistant for Lucas's resume. Please provide relevant information."
except Exception as e:
    logger.error("Error loading system instruction", error=e)
    # Fallback para qualquer outro erro.
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = "You are an AI assistant for Lucas's resume. Please provide relevant information."

def get_client_ip():
    """Extrai o IP real do cliente."""
    # Verificar headers de proxy
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

@app.before_request
def before_request():
    """Middleware para rate limiting e logging de requisições."""
    start_time = time.time()
    request.start_time = start_time
    
    # Rate limiting
    client_ip = get_client_ip()
    endpoint = request.endpoint
    
    is_allowed, rate_info = rate_limiter.check_rate_limit(client_ip, request.path)
    
    if not is_allowed:
        remaining_time = rate_limiter.get_remaining_time(client_ip, request.path)
        logger.warning(
            "Rate limit exceeded",
            ip=client_ip,
            endpoint=request.path,
            rate_info=rate_info,
            remaining_time=remaining_time
        )
        return jsonify({
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Try again in {int(remaining_time)} seconds.",
            "rate_limit_info": rate_info
        }), 429

@app.after_request
def after_request(response):
    """Middleware para logging de respostas."""
    if hasattr(request, 'start_time'):
        response_time = time.time() - request.start_time
        client_ip = get_client_ip()
        
        logger.log_request(
            method=request.method,
            endpoint=request.path,
            status_code=response.status_code,
            response_time=response_time,
            user_agent=request.headers.get('User-Agent'),
            ip=client_ip
        )
    
    return response

def filtrar_projetos_por_pergunta(projetos, pergunta):
    pergunta_lower = pergunta.lower()
    campos_busca = ["name", "description", "role", "status", "team", "technologies", "features", "highlights", "challenges", "results"]

    def projeto_relevante(projeto):
        for campo in campos_busca:
            valor = projeto.get(campo, "")
            if isinstance(valor, list):
                valor = " ".join(str(v).lower() for v in valor)
            else:
                valor = str(valor).lower()
            if pergunta_lower in valor or difflib.SequenceMatcher(None, pergunta_lower, valor).ratio() > 0.4:
                return True
        return False

    projetos_filtrados = [p for p in projetos if projeto_relevante(p)]

    if not projetos_filtrados:
        projetos_filtrados = sorted(
            projetos,
            key=lambda p: difflib.SequenceMatcher(None, pergunta_lower, p.get("description", "").lower()).ratio(),
            reverse=True
        )

    projetos_ordenados = sorted(
        projetos_filtrados,
        key=lambda p: len(p.get("technologies", [])) + p.get("year", 0),
        reverse=True
    )
    return projetos_ordenados[:5]

# --- Main Endpoint (POST /chat) ---
@app.route("/chat", methods=["POST"])
@log_execution_time(logger, "chat_endpoint")
def chat():
    start_time = time.time()
    answer = None
    cache_hit = False
    
    # Obtém os dados JSON da requisição do frontend.
    data = request.get_json()
    question = data.get("question", "").strip()
    history = data.get("history", []) # O histórico é um array de {role: "user"|"model", parts: [{text: "..."}]}
    role = data.get("role", "recruiter")  # NOVO: parâmetro role

    if not question:
        # Retorna erro se a pergunta estiver vazia.
        logger.warning("Empty question received", ip=get_client_ip())
        return jsonify({"answer": "Please provide your question."}), 400

    # Validar role
    if not role_handler.validate_role(role):
        logger.warning(f"Invalid role '{role}', using default", ip=get_client_ip())
        role = "recruiter"  # Fallback para role padrão

    try:
        # --- NOVO: Carregar apenas as seções necessárias do currículo ---
        relevant_fields = role_handler.identify_relevant_fields(question, role)
        logger.debug("Relevant fields identified", fields=relevant_fields, role=role)
        
        # Verificar cache primeiro
        cached_response = cache_handler.get(question, role, relevant_fields)
        if cached_response:
            cache_hit = True
            answer = cached_response['answer']
            logger.info("Cache hit", question_preview=question[:50])
        else:
            # Cache miss - processar normalmente
            curriculo_data = curriculo_handler.get_multiple(relevant_fields)
            logger.debug("Factual data extracted", data_keys=list(curriculo_data.keys()))
            factual_data = curriculo_data

            logger.debug("Generating role prompt")
            # Gerar prompt personalizado baseado na role
            personalized_system_instruction = role_handler.generate_role_prompt(
                role, SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT
            )
            logger.debug("Role prompt generated successfully")

            logger.debug("Gemini model initialized successfully")

            # --- NOVO: Montar resposta factual ou fallback robusto ---
            if factual_data:
                # Monta uma resposta factual clara para o modelo reescrever
                resumo = []
                for field, value in factual_data.items():
                    if isinstance(value, list):
                        if field == 'academic_background':
                            for formacao in value:
                                resumo.append(f"- {formacao.get('degree', '')} em {formacao.get('school', '')} ({formacao.get('year', '')})")
                        elif field == 'projects':
                            projetos_relevantes = filtrar_projetos_por_pergunta(value, question)
                            for proj in projetos_relevantes:
                                resumo.append(f"- Projeto: {proj.get('name', '')} - {proj.get('description', '')}")
                        else:
                            resumo.append(f"- {field.replace('_', ' ').capitalize()}: {', '.join(str(x) for x in value[:5])}")
                    elif isinstance(value, dict):
                        resumo.append(f"- {field.replace('_', ' ').capitalize()}: {', '.join([f'{k}: {v}' for k, v in value.items()])}")
                    else:
                        resumo.append(f"- {field.replace('_', ' ').capitalize()}: {value}")
                factual_summary = '\n'.join(resumo)
                logger.debug("Factual summary created", summary_length=len(factual_summary))

                # Detectar idioma da pergunta (simples: se tem acento ou palavras típicas do português)
                def is_portuguese(text):
                    # Critério simples: presença de acentos ou palavras comuns do português
                    if re.search(r'[ãáàâêéíóõôúç]', text, re.IGNORECASE):
                        return True
                    pt_keywords = ["qual", "como", "quando", "quem", "onde", "por que", "para que", "sobre", "projetos", "formação", "certificações", "habilidades", "experiência"]
                    return any(k in unicodedata.normalize('NFKD', text).lower() for k in pt_keywords)

                if is_portuguese(question):
                    prompt_estruturado = (
                        "Responda à pergunta do usuário usando apenas as informações abaixo, sem inventar nada. "
                        "Estruture sua resposta em três partes, mas NÃO utilize títulos, marcadores, separadores ou qualquer palavra como 'Introdução', 'Resposta Principal', 'Conclusão' ou variações/sinônimos no texto final. Caso utilize, use apenas em português.\n"
                        "- Comece repetindo parcialmente a pergunta respondida, mostrando ao usuário que você entendeu a questão.\n"
                        "- Em seguida, desenvolva a resposta da questão, separando por parágrafos claros.\n"
                        "- Finalize perguntando ao usuário se a resposta foi útil e/ou sugerindo uma próxima pergunta relacionada ao tema.\n"
                        "Evite saudações e não use essa estrutura para perguntas que não sejam sobre o Lucas.\n"
                        "\nPergunta: {question}\n\nInformações disponíveis:\n{factual_summary}"
                    ).format(question=question, factual_summary=factual_summary)
                else:
                    prompt_estruturado = (
                        "Answer the user's question using only the information below, without making anything up. "
                        "Structure your answer in three parts, but DO NOT use headings, bullet points, separators, or any words like 'Introduction', 'Main Answer', 'Conclusion' or similar/synonyms in the final text. If you use any, use only in English.\n"
                        "- Start by partially repeating the question, showing the user you understood it.\n"
                        "- Then, develop the main answer, using clear paragraphs.\n"
                        "- Finish by asking if the answer was helpful and/or suggesting a related follow-up question.\n"
                        "Avoid greetings and do not use this structure for questions not about Lucas.\n"
                        "\nQuestion: {question}\n\nAvailable information:\n{factual_summary}"
                    ).format(question=question, factual_summary=factual_summary)

                answer = gemini_generate_content(
                    personalized_system_instruction,
                    prompt_estruturado
                )
                answer = answer or ''

                # Pós-processamento: remover títulos de estrutura
                def remove_structural_titles(text):
                    import re
                    # Regex para títulos comuns em pt/en, com ou sem markdown
                    patterns = [
                        r'^\s*#+\s*(Introdu[cç][aã]o|Resposta Principal|Conclus[ãa]o)\s*$',
                        r'^\s*#+\s*(Introduction|Main Answer|Conclusion)\s*$',
                        r'^\s*(Introdu[cç][aã]o|Resposta Principal|Conclus[ãa]o)\s*$',
                        r'^\s*(Introduction|Main Answer|Conclusion)\s*$',
                    ]
                    lines = text.splitlines()
                    filtered = []
                    for line in lines:
                        if not any(re.match(p, line.strip(), re.IGNORECASE) for p in patterns):
                            filtered.append(line)
                    return '\n'.join(filtered).strip()

                answer = remove_structural_titles(answer)

                logger.debug("Gemini response generated successfully")
                # Armazenar no cache
                cache_handler.set(question, role, relevant_fields, answer, factual_data)
            else:
                # Fallback: não há informação factual
                available_fields = list(curriculo_handler.cache.keys()) or [
                    'academic_background', 'professional_experience', 'projects', 'skills', 'certifications', 'soft_skills', 'languages', 'intelligent_responses']
                sugestao = ', '.join([f for f in available_fields if f not in ['contact', 'name', 'title', 'summary', 'what_im_looking_for', 'additional_info']])
                answer = f"Não há informações sobre esse tema no currículo de Lucas. Posso te contar sobre: {sugestao.replace('_', ' ')}. Exemplos de perguntas: 'Qual a formação acadêmica?', 'Quais projetos ele já desenvolveu?', 'Quais certificações ele possui?'"
                logger.debug("Fallback response sent", available_fields=available_fields)

    except Exception as e:
        logger.error("Unexpected error in chat endpoint", error=e, question_preview=question[:50])
        answer = "An internal error occurred while processing your question. Please try again later."
        return jsonify({"answer": answer}), 500

    if answer is None:
        answer = "Ocorreu um erro inesperado. Tente novamente."
    
    # Log da requisição de chat
    response_time = time.time() - start_time
    logger.log_chat_request(
        question=question,
        role=role,
        response_time=response_time,
        cache_hit=cache_hit,
        relevant_fields=relevant_fields
    )
    
    # Retorna a resposta do modelo como JSON.
    return jsonify({"answer": answer, "role": role})

# Novo endpoint para obter roles disponíveis
@app.route("/roles", methods=["GET"])
def get_roles():
    """Retorna todas as roles disponíveis"""
    try:
        roles = role_handler.get_all_roles()
        return jsonify({"roles": roles})
    except Exception as e:
        logger.error("Error getting roles", error=e)
        return jsonify({"roles": []}), 500

# Novo endpoint para obter exemplos de perguntas
@app.route("/roles/<role_id>/examples", methods=["GET"])
def get_role_examples(role_id):
    """Retorna exemplos de perguntas para uma role específica"""
    try:
        examples = role_handler.get_role_examples(role_id)
        return jsonify({"examples": examples})
    except Exception as e:
        logger.error("Error getting role examples", error=e, role_id=role_id)
        return jsonify({"examples": []}), 500

# Endpoint para estatísticas do cache
@app.route("/cache/stats", methods=["GET"])
def get_cache_stats():
    """Retorna estatísticas do cache"""
    try:
        stats = cache_handler.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error("Error getting cache stats", error=e)
        return jsonify({"error": "Failed to get cache stats"}), 500

# Endpoint para limpar cache
@app.route("/cache/clear", methods=["POST"])
def clear_cache():
    """Limpa todo o cache"""
    try:
        removed_count = cache_handler.clear_all()
        logger.info("Cache cleared", removed_files=removed_count)
        return jsonify({"message": f"Cache cleared. {removed_count} files removed."})
    except Exception as e:
        logger.error("Error clearing cache", error=e)
        return jsonify({"error": "Failed to clear cache"}), 500

# Endpoint para estatísticas do rate limiter
@app.route("/rate-limit/stats", methods=["GET"])
def get_rate_limit_stats():
    """Retorna estatísticas do rate limiter"""
    try:
        stats = rate_limiter.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error("Error getting rate limit stats", error=e)
        return jsonify({"error": "Failed to get rate limit stats"}), 500

# Health check endpoint para Render
@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de health check para serviços de deploy"""
    try:
        # Verificar se a API key está configurada
        api_key_status = "configured" if os.getenv("GEMINI_API_KEY") else "missing"
        
        return jsonify({
            "status": "healthy",
            "timestamp": time.time(),
            "api_key": api_key_status,
            "version": "1.0.0"
        }), 200
    except Exception as e:
        logger.error("Health check failed", error=e)
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }), 500

if __name__ == "__main__":
    logger.info("Starting Gemini ChatBot", version="1.0.0")
    print("Iniciando Gemini ChatBot...")
    print("Servidor rodando em: http://localhost:5000")
    print("Endpoint principal: http://localhost:5000/chat")
    print("Endpoint de roles: http://localhost:5000/roles")
    print("Cache stats: http://localhost:5000/cache/stats")
    print("Rate limit stats: http://localhost:5000/rate-limit/stats")
    print("Pressione Ctrl+C para parar o servidor")
    print("-" * 50)
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=True
    )