from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os
import json
from utils.role_handler import RoleHandler
from utils.curriculo_handler import CurriculoHandler

app = Flask(__name__)

# --- Initial configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Levanta um erro se a chave API não for encontrada, impedindo que o app inicie sem ela.
    raise ValueError("GEMINI_API_KEY not found in environment variables. "
                     "Ensure it is in the .env file and you are running the script with `pipenv run`.")

# Configurações de CORS para permitir requisições do frontend (localhost:3000)
# resources={r"/*": {"origins": "*"}} permite requisições de qualquer origem.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
genai.configure(api_key=api_key)

# Inicializar RoleHandler
role_handler = RoleHandler()

# Inicializar CurriculoHandler
curriculo_handler = CurriculoHandler()

# --- Here we load and build a system instruction to JSON file ---
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
    print("Error: 'data/system_instruction.json' not found. Please create this file with the system instruction.")
    # Fallback para uma instrução padrão se o arquivo não for encontrado.
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = "You are an AI assistant for Lucas's resume. Please provide relevant information."
except json.JSONDecodeError:
    print("Error: 'data/system_instruction.json' contains invalid JSON.")
    # Fallback se o JSON for inválido.
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = "You are an AI assistant for Lucas's resume. Please provide relevant information."
except Exception as e:
    print(f"Error loading or building system_instruction.json: {e}")
    # Fallback para qualquer outro erro.
    SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT = "You are an AI assistant for Lucas's resume. Please provide relevant information."

# --- Main Endpoint (POST /chat) ---
@app.route("/chat", methods=["POST"])
def chat():
    answer = None  # Inicializa a variável answer
    # Obtém os dados JSON da requisição do frontend.
    data = request.get_json()
    question = data.get("question", "").strip()
    history = data.get("history", []) # O histórico é um array de {role: "user"|"model", parts: [{text: "..."}]}
    role = data.get("role", "recruiter")  # NOVO: parâmetro role

    if not question:
        # Retorna erro se a pergunta estiver vazia.
        return jsonify({"answer": "Please provide your question."}), 400

    # Validar role
    if not role_handler.validate_role(role):
        print(f"Warning: Invalid role '{role}', using default role 'recruiter'")
        role = "recruiter"  # Fallback para role padrão

    try:
        # --- NOVO: Carregar apenas as seções necessárias do currículo ---
        relevant_fields = role_handler.identify_relevant_fields(question, role)
        print(f"DEBUG: Campos relevantes identificados para a pergunta: {relevant_fields}")
        curriculo_data = curriculo_handler.get_multiple(relevant_fields)
        print(f"DEBUG: Dados factuais extraídos do currículo modular: {list(curriculo_data.keys())}")
        factual_data = curriculo_data

        print("DEBUG: About to generate role prompt...")
        # Gerar prompt personalizado baseado na role
        personalized_system_instruction = role_handler.generate_role_prompt(
            role, SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT
        )
        print("DEBUG: Role prompt generated successfully")

        print("DEBUG: About to initialize Gemini model...")
        # Inicializar modelo com prompt personalizado
        chat_model = genai.GenerativeModel(
            "gemini-1.5-flash-latest",
            system_instruction=personalized_system_instruction
        )
        print("DEBUG: Gemini model initialized successfully")

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
            print(f"DEBUG: Resumo factual para o modelo: {factual_summary}")
            
            # Gerar resposta usando o Gemini
            try:
                response = chat_model.generate_content(
                    f"Responda à pergunta do usuário usando apenas as informações abaixo, sem inventar nada. Seja claro, objetivo e profissional.\n\nPergunta: {question}\n\nInformações disponíveis:\n{factual_summary}"
                )
                answer = response.text
                print("DEBUG: Resposta do Gemini gerada com sucesso")
            except Exception as gemini_error:
                print(f"DEBUG: Erro ao gerar resposta do Gemini: {gemini_error}")
                # Fallback se o Gemini falhar
                answer = f"Com base nas informações disponíveis:\n{factual_summary}\n\nResposta à pergunta '{question}': As informações estão disponíveis acima."
        else:
            # Fallback: não há informação factual
            available_fields = list(curriculo_handler.cache.keys()) or [
                'academic_background', 'professional_experience', 'projects', 'skills', 'certifications', 'soft_skills', 'languages', 'intelligent_responses']
            sugestao = ', '.join([f for f in available_fields if f not in ['contact', 'name', 'title', 'summary', 'what_im_looking_for', 'additional_info']])
            answer = f"Não há informações sobre esse tema no currículo de Lucas. Posso te contar sobre: {sugestao.replace('_', ' ')}. Exemplos de perguntas: 'Qual a formação acadêmica?', 'Quais projetos ele já desenvolveu?', 'Quais certificações ele possui?'"
            print("DEBUG: Fallback acionado - resposta padrão enviada.")

    except Exception as e:
        print(f"Unexpected error in /chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        answer = "An internal error occurred while processing your question. Please try again later."
        return jsonify({"answer": answer}), 500

    if answer is None:
        answer = "Ocorreu um erro inesperado. Tente novamente."
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
        print(f"Error getting roles: {e}")
        return jsonify({"roles": []}), 500

# Novo endpoint para obter exemplos de perguntas
@app.route("/roles/<role_id>/examples", methods=["GET"])
def get_role_examples(role_id):
    """Retorna exemplos de perguntas para uma role específica"""
    try:
        examples = role_handler.get_role_examples(role_id)
        return jsonify({"examples": examples})
    except Exception as e:
        print(f"Error getting role examples: {e}")
        return jsonify({"examples": []}), 500

# --- Application execution ---
if __name__ == "__main__":
    # Inicia o servidor Flask na porta 5000, acessível de qualquer IP (0.0.0.0).
    # debug=True habilita o modo de depuração (recarregamento automático, mensagens de erro detalhadas).
    app.run(debug=True, host="0.0.0.0", port=5000)