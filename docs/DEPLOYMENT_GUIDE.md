# 🚀 Guia de Deploy - Gemini ChatBot

Este guia detalha como fazer o deploy gratuito do Gemini ChatBot usando **Render** para o backend e **Vercel** para o frontend.

## 📋 Pré-requisitos

### Contas Necessárias
- ✅ [GitHub](https://github.com) - Repositório do projeto
- ✅ [Google Cloud](https://console.cloud.google.com) - API Gemini
- ✅ [Render](https://render.com) - Backend (gratuito)
- ✅ [Vercel](https://vercel.com) - Frontend (gratuito)

### Chaves e Tokens
- `GEMINI_API_KEY` - Chave da API Google Gemini
- `RENDER_TOKEN` - Token do Render (opcional, para deploy automático)
- `VERCEL_TOKEN` - Token do Vercel (opcional, para deploy automático)

## 🔧 FASE 1: Deploy do Backend no Render

### 1.1 Preparar o Repositório
O projeto já está configurado com:
- ✅ `render.yaml` - Configuração do Render
- ✅ `backend/requirements.txt` - Dependências Python
- ✅ Endpoint `/health` - Health check para o Render
- ✅ Configuração de CORS para produção

### 1.2 Configurar no Render

1. **Acesse o Render Dashboard**
   - Vá para [dashboard.render.com](https://dashboard.render.com)
   - Faça login com sua conta GitHub

2. **Criar Novo Web Service**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório `Gemini-ChatBot`

3. **Configurar o Serviço**
   ```
   Name: gemini-chatbot-backend
   Environment: Python
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && python main.py
   Plan: Free
   ```

4. **Configurar Variáveis de Ambiente**
   - Vá em "Environment" → "Environment Variables"
   - Adicione:
     ```
     GEMINI_API_KEY = sua_chave_api_aqui
     FLASK_ENV = production
     PYTHON_VERSION = 3.11.0
     ```

5. **Configurar Health Check**
   - Health Check Path: `/health`
   - Auto-Deploy: ✅ Enabled

### 1.3 Deploy Automático
- O Render detectará automaticamente o `render.yaml`
- Cada push para `main` triggerará um novo deploy
- O serviço ficará disponível em: `https://gemini-chatbot-backend.onrender.com`

## 🌐 FASE 2: Deploy do Frontend no Vercel

### 2.1 Preparar o Repositório
O projeto já está configurado com:
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `frontend/src/config/api.js` - Configuração de API
- ✅ URLs dinâmicas baseadas no ambiente

### 2.2 Configurar no Vercel

1. **Acesse o Vercel Dashboard**
   - Vá para [vercel.com/dashboard](https://vercel.com/dashboard)
   - Faça login com sua conta GitHub

2. **Importar Projeto**
   - Clique em "New Project"
   - Conecte seu repositório GitHub
   - Selecione o repositório `Gemini-ChatBot`

3. **Configurar o Projeto**
   ```
   Framework Preset: Other
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Configurar Variáveis de Ambiente**
   - Vá em "Settings" → "Environment Variables"
   - Adicione:
     ```
     REACT_APP_BACKEND_URL = https://gemini-chatbot-backend.onrender.com
     ```

5. **Configurar Domínio**
   - O Vercel fornecerá um domínio `.vercel.app`
   - Você pode configurar um domínio customizado posteriormente

### 2.3 Deploy Automático
- Cada push para `main` triggerará um novo deploy
- Pull requests terão previews automáticos
- O site ficará disponível em: `https://gemini-chatbot.vercel.app`

## 🔐 FASE 3: Configurar Secrets no GitHub

### 3.1 Secrets para CI/CD
Vá em `Settings` → `Secrets and variables` → `Actions`:

```
GEMINI_API_KEY = sua_chave_api_aqui
REACT_APP_BACKEND_URL = https://gemini-chatbot-backend.onrender.com
CODECOV_TOKEN = seu_token_codecov (se usar)
```

### 3.2 Secrets Opcionais (para deploy automático)
```
RENDER_TOKEN = seu_token_render
RENDER_SERVICE_ID = id_do_servico_render
VERCEL_TOKEN = seu_token_vercel
VERCEL_ORG_ID = id_da_org_vercel
VERCEL_PROJECT_ID = id_do_projeto_vercel
```

## 🧪 FASE 4: Testar o Deploy

### 4.1 Testar Backend
```bash
# Testar health check
curl https://gemini-chatbot-backend.onrender.com/health

# Testar endpoint de roles
curl https://gemini-chatbot-backend.onrender.com/roles

# Testar chat (POST)
curl -X POST https://gemini-chatbot-backend.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Olá", "role": "recruiter"}'
```

### 4.2 Testar Frontend
- Acesse: `https://gemini-chatbot.vercel.app`
- Teste a funcionalidade completa
- Verifique se está conectando com o backend

## 📊 FASE 5: Monitoramento

### 5.1 Logs do Backend (Render)
- Dashboard do Render → Seu serviço → "Logs"
- Logs em tempo real
- Histórico de deploys

### 5.2 Logs do Frontend (Vercel)
- Dashboard do Vercel → Seu projeto → "Functions"
- Logs de build e runtime
- Analytics de performance

### 5.3 Métricas do Backend
```
https://gemini-chatbot-backend.onrender.com/cache/stats
https://gemini-chatbot-backend.onrender.com/rate-limit/stats
```

## ⚠️ Pontos de Atenção

### Limites da Camada Gratuita

#### Render (Backend)
- **750 horas/mês** - Suficiente para desenvolvimento
- **Cold start** - Primeira requisição pode ser lenta
- **Sleep após inatividade** - 15 minutos sem tráfego
- **512MB RAM** - Limite de memória

#### Vercel (Frontend)
- **Deploy ilimitado** - Para projetos pessoais
- **100GB bandwidth/mês** - Geralmente suficiente
- **Serverless functions** - 10 segundos timeout
- **Build time** - 100 minutos/mês

### Otimizações Recomendadas

1. **Backend**
   - Implementar cache Redis (se necessário)
   - Otimizar queries de dados
   - Usar CDN para assets estáticos

2. **Frontend**
   - Otimizar bundle size
   - Implementar lazy loading
   - Usar service workers para cache

### Segurança

1. **Variáveis de Ambiente**
   - Nunca commitar secrets no código
   - Usar sempre variáveis de ambiente
   - Rotacionar chaves periodicamente

2. **CORS**
   - Configurar origens específicas em produção
   - Não usar `*` em produção

3. **Rate Limiting**
   - Já implementado no backend
   - Monitorar uso e ajustar limites

## 🔄 Atualizações e Manutenção

### Deploy Automático
- Push para `main` → Deploy automático
- Pull requests → Preview automático
- Rollback fácil via dashboard

### Monitoramento
- Logs em tempo real
- Métricas de performance
- Alertas de erro (configuráveis)

### Backup
- Código versionado no GitHub
- Dados em JSON (versionados)
- Configurações em variáveis de ambiente

## 🆘 Troubleshooting

### Problemas Comuns

1. **Backend não inicia**
   - Verificar `GEMINI_API_KEY`
   - Verificar logs no Render
   - Testar localmente

2. **Frontend não conecta ao backend**
   - Verificar `REACT_APP_BACKEND_URL`
   - Verificar CORS no backend
   - Testar endpoints diretamente

3. **Cold start lento**
   - Normal no Render gratuito
   - Considerar upgrade para plano pago
   - Implementar health checks

### Comandos Úteis

```bash
# Testar backend local
cd backend
python main.py

# Testar frontend local
cd frontend
npm start

# Build de produção
cd frontend
npm run build

# Testes
cd backend && python -m pytest
cd frontend && npm test
```

## 📞 Suporte

- **Render**: [docs.render.com](https://docs.render.com)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **GitHub Actions**: [docs.github.com/en/actions](https://docs.github.com/en/actions)

---

**🎉 Parabéns! Seu Gemini ChatBot está agora deployado gratuitamente!** 