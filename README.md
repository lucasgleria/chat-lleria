# 🤖 Chat lleria - Sistema de Chat Inteligente com Roles

**Sistema de chatbot inteligente que utiliza a API Google Gemini para fornecer respostas personalizadas sobre mim, com sistema de roles para diferentes contextos de interação**

[![Licença](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-7.5.1-green.svg)]()
[![Status](https://img.shields.io/badge/status-concluído-green.svg)]()
[![deploy](https://img.shields.io/badge/deploy-inactive-red.svg)]()

## 📌 Sumário

1. [Sobre o Projeto](#-sobre-o-projeto)  
2. [Objetivos](#-objetivos)  
3. [Tecnologias](#-tecnologias)  
4. [Funcionalidades](#-funcionalidades)  
5. [Pré-requisitos](#-pré-requisitos)  
6. [Instalação](#-instalação)  
7. [Como utilizar](#-como-utilizar)
8. [Estrutura do Projeto](#-estrutura-do-projeto)
9. [Contribuição](#-contribuição)  
10. [Licença](#-licença)  
11. [Contato](#-contato)  
12. [Recursos Adicionais](#-recursos-adicionais)  

## 💻 Sobre o Projeto  

O **Chat lleria** é um projeto que implementa um chatbot inteligente utilizando a API Google Gemini para fornecer respostas contextualizadas sobre mim. O sistema inclui um mecanismo de roles que permite personalizar a experiência de interação baseada no contexto do usuário (recrutador, desenvolvedor, cliente, estudante).

- *Motivação*: Criar um sistema de chatbot inteligente que se adapte ao perfil do usuário, fornecendo respostas mais relevantes e contextualizadas sobre currículos profissionais.
- *Público-alvo*: Recrutadores, desenvolvedores, clientes e estudantes interessados em obter informações personalizadas sobre currículos.

## 🎯 Objetivos  

### 🛠️ Técnicos  
- Integrar a API Google Gemini 1.5 Flash para processamento de linguagem natural.
- Implementar sistema de roles dinâmico com 4 perfis diferentes de interação.
- Desenvolver interface responsiva e moderna com React e Tailwind CSS.
- Criar backend robusto com Flask e validação de dados.
- Garantir escalabilidade e manutenibilidade do código.
- Implementar sistema de cache e otimização de performance.

## 🚀 Tecnologias  

**Backend**
- Python
- Flask
- Google Generative AI (Gemini API)
- Pipenv

**Frontend**
- React
- Tailwind CSS
- Axios
- Context API

**Infraestrutura**
- JSON (armazenamento de dados)

## ✨ Funcionalidades  

- ✅ **Sistema de Roles**: 4 perfis personalizados (Recrutador, Desenvolvedor, Cliente, Estudante)
- ✅ **Integração com Gemini API**: Processamento avançado de linguagem natural
- ✅ **Interface Multi-tela**: Welcome → Question → Role Selection → Chat
- ✅ **Seleção Visual de Roles**: Cards animados para escolha de perfil
- ✅ **Chat Interativo**: Interface moderna com animações e feedback visual
- ✅ **Responsividade**: Design adaptativo para desktop, tablet e mobile
- ✅ **Validação de Dados**: Filtros para perguntas fora do escopo
- ✅ **Histórico de Conversas**: Manutenção do contexto da conversa
- ✅ **Exemplos de Perguntas**: Sugestões específicas para cada perfil
- ✅ **Persistência de Dados**: Lembrança do perfil selecionado

## ⚙️ Pré-requisitos  

- **Node.js** (versão LTS)
- **Python 3.9+**
- **Pipenv**
- **Conta Google Cloud** com API Gemini habilitada
- **Conexão estável à internet**

## 🛠️ Instalação  

1. Clone o repositório:
```bash
git clone https://github.com/your-username/Gemini-ChatBot.git
cd Gemini-ChatBot
```

2. Configure o Backend:
```bash
cd backend

# Instale as dependências Python
pipenv install

# Crie arquivo .env
echo "GEMINI_API_KEY=sua_chave_api_aqui" > .env

# Ative o ambiente virtual
pipenv shell
```

3. Configure o Frontend:
```bash
cd frontend

# Instale as dependências Node.js
npm install
```

4. Configure a API Gemini:
- Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
- Crie uma nova chave API
- Adicione a chave no arquivo `.env` do backend

## ❗ Como Utilizar

### Iniciar o Projeto

```bash
# Terminal 1 - Backend
cd backend
pipenv run python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### ▶️ Demonstração

![Chat lleria](frontend/public/Icon2.gif)

_(Gif icon do projeto)_

## 📂 Estrutura do Projeto  
```plaintext
Gemini-ChatBot/
├── backend/
│   ├── data/
│   │   ├── roles/                     # Configurações das roles
│   │   │   ├── recruiter.json
│   │   │   ├── developer.json
│   │   │   ├── client.json
│   │   │   └── student.json
│   │   ├── curriculo.json             # Dados do currículo
│   │   ├── intelligent_responses.json # Respostas inteligentes
│   │   ├── ...*.json                  # Jsons particionados do curriculo
│   │   └── system_instruction.json    # Prompt de regras
│   ├── utils/
│   │   ├── role_handler.py            # Gerenciador de roles
│   │   └── curriculo_handler.py       # Middleware para análise dos jsons
│   └── main.py                        # Servidor Flask
├── frontend/
│   ├── src/
│   │   ├── components/                # Componentes React
│   │   │   ├── RoleCard.js
│   │   │   ├── RoleContext.js
│   │   │   └── RoleSelector.js
│   │   ├── chatWindow.js              # Interface do chat
│   │   ├── openingWindow.js           # Tela de boas-vindas
│   │   └── questionWindow.js          # Tela de pergunta
│   ├── public/                        # Assets públicos
│   └── package.json
├── docs/                              # Documentação
└── README.md                          # Esse arquivo
```

## 🎭 Sistema de Roles

O sistema oferece 4 perfis diferentes de interação:

### 👔 Recrutador/HR
- **Foco**: Recrutamento e seleção
- **Áreas**: Experiência profissional, soft skills, projetos
- **Tom**: Profissional e objetivo
- **Exemplos**: "Quais são os principais projetos?", "Como você trabalha em equipe?"

### 💻 Desenvolvedor
- **Foco**: Aspectos técnicos e código
- **Áreas**: Tecnologias, arquitetura, metodologias
- **Tom**: Técnico e detalhado
- **Exemplos**: "Quais tecnologias você domina?", "Como você resolve problemas técnicos?"

### 👥 Cliente
- **Foco**: Resultados e valor de negócio
- **Áreas**: Entregas, prazos, comunicação
- **Tom**: Orientado a resultados
- **Exemplos**: "Como você garante qualidade?", "Qual sua experiência com prazos?"

### 🎓 Estudante
- **Foco**: Aprendizado e desenvolvimento
- **Áreas**: Educação, projetos acadêmicos, crescimento
- **Tom**: Motivacional e educacional
- **Exemplos**: "Como você aprendeu programação?", "Quais são seus objetivos?"

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estas etapas:

### **1. Reporte bugs**
- Abra uma [issue](https://github.com/lucasgleria/chat-lleria/issues) no GitHub
- Descreva o problema detalhadamente
- Inclua logs e screenshots se possível

### **2. Sugira melhorias**
- Envie ideias através de issues
- Proponha novas funcionalidades
- Discuta melhorias de arquitetura

### **3. Desenvolva**
- Faça um fork do projeto
- Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
- Faça suas alterações seguindo os padrões do projeto
- Adicione testes para novas funcionalidades
- Faça commit (`git commit -m 'feat: nova funcionalidade'`)
- Envie um Pull Request

### **4. Padrões de Código**
- Siga PEP 8 para estilo Python
- Use type hints quando possível
- Documente funções e classes
- Mantenha a arquitetura modular
- Adicione testes para novas funcionalidades

## 📜 Licença  

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 📞 Contato & Evidências

- **Autor**: [Lucas Leria](https://github.com/lucasgleria)  
- **LinkedIn**: [Lucas Leria](https://www.linkedin.com/in/lucasleria/)  
- **Autor**: [Hamza](https://github.com/your-username)  
- **LinkedIn**: [Hamza](https://www.linkedin.com/in/seu-linkedin/)  

## 🔍 Recursos Adicionais

- [Google Gemini API](https://ai.google.dev/) - Documentação oficial
- [React](https://react.dev/) - Documentação oficial
- [Flask](https://flask.palletsprojects.com/) - Documentação oficial
- [Tailwind CSS](https://tailwindcss.com/docs) - Documentação oficial
- [Google AI Studio](https://makersuite.google.com/) - Ferramenta de desenvolvimento 