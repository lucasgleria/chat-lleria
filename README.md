# 🤖 Gemini ChatBot - Sistema de Chat Inteligente com IA

**Sistema de chatbot inteligente que utiliza a API Google Gemini para fornecer respostas personalizadas sobre currículos profissionais, com sistema de roles para diferentes contextos de interação**

[![Licença](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)]()
[![Status](https://img.shields.io/badge/status-produção-green.svg)]()
[![Deploy](https://img.shields.io/badge/deploy-active-green.svg)]()
[![Backend CI](https://github.com/lucasgleria/chat-lleria/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/lucasgleria/chat-lleria/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/lucasgleria/chat-lleria/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/lucasgleria/chat-lleria/actions/workflows/frontend-ci.yml)

## 📌 Sumário

1. [Sobre o Projeto](#-sobre-o-projeto)  
2. [Funcionalidades](#-funcionalidades)  
3. [Tecnologias](#-tecnologias)  
4. [Arquitetura](#-arquitetura)
5. [Sistema de Roles](#-sistema-de-roles)
6. [Pré-requisitos](#-pré-requisitos)  
7. [Instalação](#-instalação)  
8. [Como Utilizar](#-como-utilizar)
9. [Deploy](#-deploy)
10. [Estrutura do Projeto](#-estrutura-do-projeto)
11. [API Endpoints](#-api-endpoints)
12. [Contribuição](#-contribuição)  
13. [Licença](#-licença)  
14. [Contato](#-contato)  

## 💻 Sobre o Projeto  

O **Gemini ChatBot** é um sistema avançado de chatbot inteligente que utiliza a API Google Gemini para fornecer respostas contextualizadas sobre currículos profissionais. O sistema implementa um mecanismo de roles que permite personalizar a experiência de interação baseada no contexto do usuário (recrutador, desenvolvedor, cliente, estudante).

### 🎯 Características Principais
- **IA Avançada**: Integração com Google Gemini 1.5 Flash para processamento de linguagem natural
- **Sistema de Roles**: 4 perfis personalizados com contextos específicos
- **Interface Moderna**: Design responsivo com React e Tailwind CSS
- **Backend Robusto**: API Flask com cache, rate limiting e logging
- **Deploy Automatizado**: Configuração completa para Render e Vercel

### 🎯 Público-Alvo
- **Recrutadores e RH**: Buscam informações profissionais e soft skills
- **Desenvolvedores**: Interessados em aspectos técnicos e projetos
- **Clientes**: Focam em resultados e valor de negócio
- **Estudantes**: Procuram inspiração e orientação de carreira

## ✨ Funcionalidades  

### 🤖 IA e Processamento
- ✅ **Integração Gemini API**: Processamento avançado de linguagem natural
- ✅ **Sistema de Cache**: Otimização de performance com cache inteligente
- ✅ **Rate Limiting**: Proteção contra spam e abuso
- ✅ **Validação de Dados**: Filtros para perguntas fora do escopo
- ✅ **Suporte Multilíngue**: Português, Inglês e Espanhol

### 🎭 Sistema de Roles
- ✅ **4 Perfis Personalizados**: Recrutador, Desenvolvedor, Cliente, Estudante
- ✅ **Contextos Específicos**: Cada role tem foco, tom e exemplos únicos
- ✅ **Seleção Visual**: Cards animados para escolha de perfil
- ✅ **Persistência**: Lembrança do perfil selecionado
- ✅ **Exemplos Dinâmicos**: Sugestões específicas para cada perfil

### 🎨 Interface do Usuário
- ✅ **Interface Multi-tela**: Welcome → Question → Role Selection → Chat
- ✅ **Design Responsivo**: Adaptativo para desktop, tablet e mobile
- ✅ **Animações Suaves**: Transições e feedback visual
- ✅ **Chat Interativo**: Interface moderna com histórico de conversas
- ✅ **Estados de Loading**: Feedback visual durante processamento

### 🔧 Backend Avançado
- ✅ **Logging Completo**: Sistema de logs estruturado
- ✅ **Health Checks**: Monitoramento de saúde da aplicação
- ✅ **Error Handling**: Tratamento robusto de erros
- ✅ **CORS Configurado**: Suporte para diferentes origens
- ✅ **Rotação de API Keys**: Fallback automático para múltiplas chaves

## 🚀 Tecnologias  

### **Backend**
- **Python 3.11+** - Linguagem principal
- **Flask** - Framework web
- **Google Generative AI** - API Gemini 1.5 Flash
- **Flask-CORS** - Cross-origin resource sharing
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

### **Frontend**
- **React 19.1.0** - Framework JavaScript
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP
- **Context API** - Gerenciamento de estado

### **Infraestrutura**
- **JSON** - Armazenamento de dados estruturados
- **Render** - Deploy do backend (gratuito)
- **Vercel** - Deploy do frontend (gratuito)
- **GitHub Actions** - CI/CD automatizado

## 🏗️ Arquitetura

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│   Frontend      │ ◄─────────────► │    Backend      │
│   (React)       │                 │   (Flask)       │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  Google Gemini  │
                                    │      API        │
                                    └─────────────────┘
```

### **Componentes Principais**

#### Frontend (React)
- **RoleContext**: Gerenciamento global de roles
- **RoleSelector**: Interface de seleção de perfis
- **ChatWindow**: Interface principal do chat
- **BaseLayout**: Layout responsivo base

#### Backend (Flask)
- **RoleHandler**: Gerenciamento de roles e prompts
- **CurriculoHandler**: Processamento de dados do currículo
- **CacheHandler**: Sistema de cache inteligente
- **RateLimiter**: Controle de taxa de requisições
- **Logger**: Sistema de logging estruturado

## 🎭 Sistema de Roles

O sistema oferece 4 perfis diferentes de interação, cada um com foco, tom e exemplos específicos:

### 👔 **Recrutador/HR**
- **Foco**: Recrutamento e seleção profissional
- **Áreas**: Experiência profissional, soft skills, projetos, certificações
- **Tom**: Profissional e objetivo
- **Exemplos**: "Quais são os principais projetos?", "Como você trabalha em equipe?"

### 💻 **Desenvolvedor**
- **Foco**: Aspectos técnicos e desenvolvimento
- **Áreas**: Tecnologias, arquitetura, metodologias, código
- **Tom**: Técnico e detalhado
- **Exemplos**: "Quais tecnologias você domina?", "Como você resolve problemas técnicos?"

### 👥 **Cliente**
- **Foco**: Resultados e valor de negócio
- **Áreas**: Entregas, prazos, comunicação, impacto
- **Tom**: Orientado a resultados
- **Exemplos**: "Como você garante qualidade?", "Qual sua experiência com prazos?"

### 🎓 **Estudante**
- **Foco**: Aprendizado e desenvolvimento pessoal
- **Áreas**: Educação, projetos acadêmicos, crescimento
- **Tom**: Motivacional e educacional
- **Exemplos**: "Como você aprendeu programação?", "Quais são seus objetivos?"

## ⚙️ Pré-requisitos  

- **Node.js** (versão LTS 18+)
- **Python 3.11+**
- **Git**
- **Conta Google Cloud** com API Gemini habilitada
- **Conexão estável à internet**

## 🛠️ Instalação  

### 1. Clone o Repositório
```bash
git clone https://github.com/lucasgleria/chat-lleria.git
cd chat-lleria
```

### 2. Configure o Backend
```bash
cd backend

# Instale as dependências Python
pip install -r requirements.txt
pip install -r requirements.txt

# Crie arquivo .env
echo "GEMINI_API_KEY=sua_chave_api_aqui" > .env

# (Opcional) Configure chave secundária para fallback
echo "GEMINI_KEY_API2=sua_chave_secundaria" >> .env
```

### 3. Configure o Frontend
```bash
cd frontend

# Instale as dependências Node.js
npm install
```

### 4. Configure a API Gemini
- Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
- Crie uma nova chave API
- Adicione a chave no arquivo `.env` do backend

## ❗ Como Utilizar

### Desenvolvimento Local

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Acesso
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

### ▶️ Demonstração

![Gemini ChatBot](frontend/public/Icon2.gif)

## 🚀 Deploy

### Deploy Automatizado
O projeto está configurado para deploy automático:

- **Backend**: Render (gratuito) - `https://chat-lleria.onrender.com`
- **Frontend**: Vercel (gratuito) - `https://gemini-chatbot.vercel.app`

### Configuração Manual
Veja o [Guia de Deploy](docs/DEPLOYMENT_GUIDE.md) para instruções detalhadas.

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
│   │   ├── curriculo.json             # Dados principais do currículo
│   │   ├── intelligent_responses.json # Respostas inteligentes
│   │   ├── skills.json                # Habilidades técnicas
│   │   ├── projects.json              # Projetos detalhados
│   │   ├── professional_experience.json # Experiência profissional
│   │   ├── certifications.json        # Certificações
│   │   ├── academic_background.json   # Formação acadêmica
│   │   ├── languages.json             # Idiomas
│   │   ├── soft_skills.json           # Soft skills
│   │   └── system_instruction.json    # Instruções do sistema
│   ├── utils/
│   │   ├── role_handler.py            # Gerenciador de roles
│   │   ├── curriculo_handler.py       # Processamento de dados
│   │   ├── cache_handler.py           # Sistema de cache
│   │   ├── rate_limiter.py            # Controle de taxa
│   │   └── logger.py                  # Sistema de logs
│   ├── tests/                         # Testes automatizados
│   ├── logs/                          # Logs da aplicação
│   ├── cache/                         # Cache de respostas
│   ├── main.py                        # Servidor Flask
│   └── requirements.txt               # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/                # Componentes React
│   │   │   ├── RoleCard.js
│   │   │   ├── RoleContext.js
│   │   │   ├── RoleSelector.js
│   │   │   ├── BaseLayout.js
│   │   │   └── SuggestedQuestions.js
│   │   ├── config/
│   │   │   └── api.js                 # Configuração da API
│   │   ├── data/
│   │   │   └── roles.js               # Dados das roles (frontend)
│   │   ├── chatWindow.js              # Interface do chat
│   │   ├── openingWindow.js           # Tela de boas-vindas
│   │   ├── questionWindow.js          # Tela de pergunta
│   │   ├── App.js                     # Componente principal
│   │   └── index.js                   # Ponto de entrada
│   ├── public/                        # Assets públicos
│   └── package.json                   # Dependências Node.js
├── docs/                              # Documentação técnica
├── scripts/                           # Scripts de deploy
├── render.yaml                        # Configuração Render
├── vercel.json                        # Configuração Vercel
└── README.md                          # Este arquivo
```

## 🔌 API Endpoints

### **Chat**
- `POST /chat` - Envia mensagem e recebe resposta
- `GET /roles` - Lista todas as roles disponíveis
- `GET /roles/<role_id>/examples` - Exemplos para role específica

### **Monitoramento**
- `GET /health` - Health check da aplicação
- `GET /cache/stats` - Estatísticas do cache
- `GET /rate-limit/stats` - Estatísticas de rate limiting

### **Exemplo de Uso**
```bash
# Enviar mensagem
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Quais são seus principais projetos?", "role": "recruiter"}'

# Listar roles
curl http://localhost:5000/roles

# Exemplos de uma role
curl http://localhost:5000/roles/recruiter/examples
```

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estas etapas:

### **1. Reporte Bugs**
- Abra uma [issue](https://github.com/lucasgleria/chat-lleria/issues) no GitHub
- Descreva o problema detalhadamente
- Inclua logs e screenshots se possível

### **2. Sugira Melhorias**
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

## 📞 Contato

- **Autor**: [Lucas Leria](https://github.com/lucasgleria)  
- **LinkedIn**: [Lucas Leria](https://www.linkedin.com/in/lucasleria/)  
- **Colaborador**: [Hamza Nouman](https://github.com/HamzaNouman)  
- **LinkedIn do colaborador**: [Hamza Nouman](https://www.linkedin.com/in/hamzanouman)  

## 🔍 Recursos Adicionais

- [Documentação Técnica](docs/TECHNICAL_DOCS.md) - Arquitetura e implementação
- [Guia de Deploy](docs/DEPLOYMENT_GUIDE.md) - Instruções de deploy
- [Documentação de Roles](docs/ROLE_DOCUMENTATION.md) - Sistema de roles
- [Roadmap](docs/ROADMAP.md) - Planejamento do projeto
- [Google Gemini API](https://ai.google.dev/) - Documentação oficial
- [React](https://react.dev/) - Documentação oficial
- [Flask](https://flask.palletsprojects.com/) - Documentação oficial
- [Tailwind CSS](https://tailwindcss.com/docs) - Documentação oficial
- [Google AI Studio](https://makersuite.google.com/) - Ferramenta de desenvolvimento

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!**
