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

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# --- Initial configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Levanta um erro se a chave API não for encontrada, impedindo que o app inicie sem ela.
    raise ValueError("GEMINI_API_KEY not found in environment variables. "
                     "Ensure it is in the .env file and you are running the script with `python main.py`.")

# Configurações de CORS para permitir requisições do frontend (localhost:3000)
# resources={r"/*": {"origins": "*"}} permite requisições de qualquer origem.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
genai.configure(api_key=api_key)

# Inicializar handlers
role_handler = RoleHandler()
curriculo_handler = CurriculoHandler()
cache_handler = CacheHandler()

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

            logger.debug("Initializing Gemini model")
            # Inicializar modelo com prompt personalizado (versão 0.8.5+ suporta system_instruction)
            chat_model = genai.GenerativeModel(
                "gemini-1.5-flash-latest",
                system_instruction=personalized_system_instruction
            )
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
                            for proj in value[:3]:
                                resumo.append(f"- Projeto: {proj.get('name', '')} - {proj.get('description', '')}")
                        else:
                            resumo.append(f"- {field.replace('_', ' ').capitalize()}: {', '.join(str(x) for x in value[:5])}")
                    elif isinstance(value, dict):
                        resumo.append(f"- {field.replace('_', ' ').capitalize()}: {', '.join([f'{k}: {v}' for k, v in value.items()])}")
                    else:
                        resumo.append(f"- {field.replace('_', ' ').capitalize()}: {value}")
                factual_summary = '\n'.join(resumo)
                logger.debug("Factual summary created", summary_length=len(factual_summary))
                
                # Gerar resposta usando o Gemini
                try:
                    response = chat_model.generate_content(
                        f"Responda à pergunta do usuário usando apenas as informações abaixo, sem inventar nada. Seja claro, objetivo e profissional.\n\nPergunta: {question}\n\nInformações disponíveis:\n{factual_summary}"
                    )
                    answer = response.text
                    logger.debug("Gemini response generated successfully")
                    
                    # Armazenar no cache
                    cache_handler.set(question, role, relevant_fields, answer, factual_data)
                    
                except Exception as gemini_error:
                    logger.error("Gemini API error", error=gemini_error, question_preview=question[:50])
                    # Fallback se o Gemini falhar
                    answer = f"Com base nas informações disponíveis:\n{factual_summary}\n\nResposta à pergunta '{question}': As informações estão disponíveis acima."
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