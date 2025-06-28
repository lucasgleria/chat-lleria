import json
import os

class CurriculoHandler:
    def __init__(self, data_dir=None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
        self.data_dir = data_dir
        self.cache = {}

    def load_section(self, section):
        """Carrega uma seção específica do currículo a partir do arquivo modular."""
        filename = os.path.join(self.data_dir, f"{section}.json")
        
        # Verificar cache primeiro
        if section in self.cache:
            return self.cache[section]
        
        # Verificar se o arquivo existe
        if not os.path.exists(filename):
            print(f"Warning: Arquivo {filename} não encontrado")
            return None
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Para arquivos modulares, o dado está na chave com o nome da seção
            if section in data:
                self.cache[section] = data[section]
                return self.cache[section]
            else:
                # Se não encontrar a chave específica, retorna o dado completo
                self.cache[section] = data
                return self.cache[section]
                
        except json.JSONDecodeError as e:
            print(f"Error: JSON inválido no arquivo {filename}: {e}")
            return None
        except Exception as e:
            print(f"Error: Erro ao carregar arquivo {filename}: {e}")
            return None

    def get(self, section):
        return self.load_section(section)

    def get_multiple(self, sections):
        result = {}
        for section in sections:
            value = self.load_section(section)
            if value is not None:
                result[section] = value
        return result 