#!/bin/bash

# 🚀 Script de Deploy Automatizado - Gemini ChatBot
# Este script facilita o processo de deploy para Render e Vercel

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  🚀 Gemini ChatBot Deploy${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Verificar se estamos no diretório raiz do projeto
check_project_root() {
    if [ ! -f "render.yaml" ] || [ ! -f "vercel.json" ]; then
        print_error "Este script deve ser executado no diretório raiz do projeto!"
        exit 1
    fi
}

# Verificar dependências
check_dependencies() {
    print_message "Verificando dependências..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 não encontrado!"
        exit 1
    fi
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js não encontrado!"
        exit 1
    fi
    
    # Verificar npm
    if ! command -v npm &> /dev/null; then
        print_error "npm não encontrado!"
        exit 1
    fi
    
    print_message "✅ Todas as dependências estão instaladas"
}

# Testar backend localmente
test_backend() {
    print_message "Testando backend localmente..."
    
    cd backend
    
    # Verificar se requirements.txt existe
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt não encontrado!"
        exit 1
    fi
    
    # Instalar dependências
    print_message "Instalando dependências Python..."
    pip install -r requirements.txt
    
    # Verificar se .env existe
    if [ ! -f ".env" ]; then
        print_warning ".env não encontrado. Criando arquivo de exemplo..."
        echo "GEMINI_API_KEY=your_api_key_here" > .env
        print_warning "⚠️  Configure sua GEMINI_API_KEY no arquivo .env"
    fi
    
    # Testar se o servidor inicia
    print_message "Testando inicialização do servidor..."
    timeout 10s python main.py &
    SERVER_PID=$!
    
    sleep 3
    
    # Testar health check
    if curl -s http://localhost:5000/health > /dev/null; then
        print_message "✅ Backend funcionando corretamente"
        kill $SERVER_PID 2>/dev/null || true
    else
        print_error "❌ Backend não está respondendo"
        kill $SERVER_PID 2>/dev/null || true
        exit 1
    fi
    
    cd ..
}

# Testar frontend localmente
test_frontend() {
    print_message "Testando frontend localmente..."
    
    cd frontend
    
    # Verificar se package.json existe
    if [ ! -f "package.json" ]; then
        print_error "package.json não encontrado!"
        exit 1
    fi
    
    # Instalar dependências
    print_message "Instalando dependências Node.js..."
    npm install
    
    # Testar build
    print_message "Testando build de produção..."
    npm run build
    
    if [ -d "build" ]; then
        print_message "✅ Build de produção criado com sucesso"
    else
        print_error "❌ Falha no build de produção"
        exit 1
    fi
    
    cd ..
}

# Verificar configuração do Git
check_git() {
    print_message "Verificando configuração do Git..."
    
    if [ ! -d ".git" ]; then
        print_error "Este não é um repositório Git!"
        exit 1
    fi
    
    # Verificar se há mudanças não commitadas
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "⚠️  Há mudanças não commitadas no repositório"
        read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_message "Deploy cancelado. Commit suas mudanças primeiro."
            exit 1
        fi
    fi
    
    # Verificar branch atual
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "main" ]; then
        print_warning "⚠️  Você está na branch '$CURRENT_BRANCH', não na 'main'"
        read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_message "Deploy cancelado. Mude para a branch main primeiro."
            exit 1
        fi
    fi
    
    print_message "✅ Configuração do Git OK"
}

# Verificar configuração dos serviços
check_services() {
    print_message "Verificando configuração dos serviços..."
    
    # Verificar render.yaml
    if [ ! -f "render.yaml" ]; then
        print_error "render.yaml não encontrado!"
        exit 1
    fi
    
    # Verificar vercel.json
    if [ ! -f "vercel.json" ]; then
        print_error "vercel.json não encontrado!"
        exit 1
    fi
    
    print_message "✅ Arquivos de configuração encontrados"
}

# Deploy para GitHub (trigger automático)
deploy_to_github() {
    print_message "Fazendo push para GitHub (deploy automático)..."
    
    # Verificar se há mudanças para fazer push
    if [ -z "$(git status --porcelain)" ]; then
        print_warning "Não há mudanças para fazer push"
        return
    fi
    
    # Adicionar todas as mudanças
    git add .
    
    # Commit com timestamp
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "🚀 Deploy automático - $TIMESTAMP"
    
    # Push para main
    git push origin main
    
    print_message "✅ Push realizado com sucesso"
    print_message "🔗 Render e Vercel farão deploy automático"
}

# Mostrar status dos deploys
show_deploy_status() {
    print_message "Status dos deploys:"
    echo
    echo "📊 Backend (Render):"
    echo "   - URL: https://chat-lleria.onrender.com"
    echo "   - Health Check: https://chat-lleria.onrender.com/health"
    echo
    echo "🌐 Frontend (Vercel):"
    echo "   - URL: https://gemini-chatbot.vercel.app"
    echo
    echo "📝 Logs:"
    echo "   - Render: https://dashboard.render.com"
    echo "   - Vercel: https://vercel.com/dashboard"
    echo
    print_warning "⚠️  Os deploys podem levar alguns minutos para completar"
}

# Função principal
main() {
    print_header
    
    # Verificar se estamos no diretório correto
    check_project_root
    
    # Verificar dependências
    check_dependencies
    
    # Verificar configuração do Git
    check_git
    
    # Verificar configuração dos serviços
    check_services
    
    # Testar backend
    test_backend
    
    # Testar frontend
    test_frontend
    
    # Deploy para GitHub
    deploy_to_github
    
    # Mostrar status
    show_deploy_status
    
    print_message "🎉 Deploy iniciado com sucesso!"
    print_message "Acompanhe o progresso nos dashboards dos serviços"
}

# Executar função principal
main "$@" 