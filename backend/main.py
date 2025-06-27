from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os
import json
from utils.role_handler import RoleHandler

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
        # ---  Load the curriculo content---
        # Tenta carregar o conteúdo do currículo de um arquivo JSON.
        try:
            print("DEBUG: Attempting to load curriculo.json...")
            with open("data/curriculo.json", "r", encoding="utf-8") as f:
                print("DEBUG: File opened successfully")
                curriculo_data = json.load(f)
                print("DEBUG: JSON parsed successfully")
            curriculo_json_string = json.dumps(curriculo_data, indent=2, ensure_ascii=False)
            print("DEBUG: JSON converted to string successfully")

        except FileNotFoundError:
            print("Error: 'data/curriculo.json' not found. Check the path.")
            return jsonify({"answer": "Sorry, Lucas's résumé is not available at the moment. Please try again later."}), 500
        except json.JSONDecodeError as e:
            print(f"Error: 'data/curriculo.json' contains invalid JSON: {e}")
            return jsonify({"answer": "Sorry, there's a problem with Lucas's résumé data. Please try again later."}), 500
        except Exception as e:
            print(f"Error reading or processing 'data/curriculo.json': {e}")
            return jsonify({"answer": "An issue occurred while loading Lucas's résumé information. Please try again later."}), 500

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

        # --- Here we prepare the historic (context) for Gemini---
        gemini_history = []

        if not history: # Se é o início de uma conversa, injeta o currículo como contexto inicial.
            print("DEBUG: No history, adding curriculum as initial context...")
            gemini_history.append({
                "role": "user",
                "parts": [{"text": f"Here is the detailed résumé information in JSON format. Use this as your primary knowledge base for all responses about Lucas:\n{curriculo_json_string}"}]
            })
            # Adiciona a pergunta inicial do usuário ao histórico.
            gemini_history.append({"role": "user", "parts": [{"text": question}]})

        else: # Se já tem histórico, adiciona as mensagens anteriores ao contexto do Gemini.
            print("DEBUG: Processing existing history...")
            for msg in history:
                # CORREÇÃO AQUI: msg["parts"] já é um array de objetos {text: "..."}.
                # Precisamos verificar se ele é um array e pegar o conteúdo de texto.
                if isinstance(msg.get("parts"), list) and msg["parts"]:
                    # Assume que há pelo menos um objeto com a chave 'text'
                    content_text = ""
                    for part in msg["parts"]:
                        if isinstance(part, dict) and "text" in part:
                            content_text += part["text"] + " " # Concatena textos se houver múltiplas partes
                    gemini_history.append({"role": msg["role"], "parts": [{"text": content_text.strip()}]})
                else:
                    # Fallback caso a estrutura seja inesperada (e.g., se for apenas uma string)
                    gemini_history.append({"role": msg["role"], "parts": [{"text": str(msg.get("parts", ""))}]})

        print("DEBUG: About to start chat session...")
        # Inicia a sessão de chat com o histórico preparado.
        chat_session = chat_model.start_chat(history=gemini_history)
        print("DEBUG: Chat session started successfully")

        print("DEBUG: About to send message to Gemini...")
        # Envia a pergunta atual para o modelo.
        response = chat_session.send_message(question)
        answer = response.text
        print("DEBUG: Message sent and response received successfully")

    except Exception as e:
        print(f"Unexpected error in /chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        answer = "An internal error occurred while processing your question. Please try again later."
        return jsonify({"answer": answer}), 500

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