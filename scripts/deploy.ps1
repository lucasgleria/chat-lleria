# 🚀 Script de Deploy Automatizado - Gemini ChatBot (PowerShell)
# Este script facilita o processo de deploy para Render e Vercel no Windows

param(
    [switch]$SkipTests,
    [switch]$Force
)

# Configurar para parar em caso de erro
$ErrorActionPreference = "Stop"

# Função para imprimir mensagens coloridas
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Header {
    Write-Host "================================" -ForegroundColor Blue
    Write-Host "  🚀 Gemini ChatBot Deploy" -ForegroundColor Blue
    Write-Host "================================" -ForegroundColor Blue
}

# Verificar se estamos no diretório raiz do projeto
function Test-ProjectRoot {
    if (-not (Test-Path "render.yaml") -or -not (Test-Path "vercel.json")) {
        Write-Error "Este script deve ser executado no diretório raiz do projeto!"
        exit 1
    }
}

# Verificar dependências
function Test-Dependencies {
    Write-Info "Verificando dependências..."
    
    # Verificar Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Info "Python encontrado: $pythonVersion"
    }
    catch {
        Write-Error "Python não encontrado! Instale Python 3.11+"
        exit 1
    }
    
    # Verificar Node.js
    try {
        $nodeVersion = node --version 2>&1
        Write-Info "Node.js encontrado: $nodeVersion"
    }
    catch {
        Write-Error "Node.js não encontrado! Instale Node.js 18+"
        exit 1
    }
    
    # Verificar npm
    try {
        $npmVersion = npm --version 2>&1
        Write-Info "npm encontrado: $npmVersion"
    }
    catch {
        Write-Error "npm não encontrado!"
        exit 1
    }
    
    Write-Info "✅ Todas as dependências estão instaladas"
}

# Testar backend localmente
function Test-Backend {
    Write-Info "Testando backend localmente..."
    
    Push-Location backend
    
    # Verificar se requirements.txt existe
    if (-not (Test-Path "requirements.txt")) {
        Write-Error "requirements.txt não encontrado!"
        exit 1
    }
    
    # Instalar dependências
    Write-Info "Instalando dependências Python..."
    pip install -r requirements.txt
    
    # Verificar se .env existe
    if (-not (Test-Path ".env")) {
        Write-Warning ".env não encontrado. Criando arquivo de exemplo..."
        "GEMINI_API_KEY=your_api_key_here" | Out-File -FilePath ".env" -Encoding UTF8
        Write-Warning "⚠️  Configure sua GEMINI_API_KEY no arquivo .env"
    }
    
    # Testar se o servidor inicia
    Write-Info "Testando inicialização do servidor..."
    
    # Iniciar servidor em background
    $serverJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        python main.py
    }
    
    # Aguardar um pouco
    Start-Sleep -Seconds 3
    
    # Testar health check
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Info "✅ Backend funcionando corretamente"
        }
    }
    catch {
        Write-Error "❌ Backend não está respondendo"
        Stop-Job $serverJob -ErrorAction SilentlyContinue
        Remove-Job $serverJob -ErrorAction SilentlyContinue
        exit 1
    }
    finally {
        Stop-Job $serverJob -ErrorAction SilentlyContinue
        Remove-Job $serverJob -ErrorAction SilentlyContinue
    }
    
    Pop-Location
}

# Testar frontend localmente
function Test-Frontend {
    Write-Info "Testando frontend localmente..."
    
    Push-Location frontend
    
    # Verificar se package.json existe
    if (-not (Test-Path "package.json")) {
        Write-Error "package.json não encontrado!"
        exit 1
    }
    
    # Instalar dependências
    Write-Info "Instalando dependências Node.js..."
    npm install
    
    # Testar build
    Write-Info "Testando build de produção..."
    npm run build
    
    if (Test-Path "build") {
        Write-Info "✅ Build de produção criado com sucesso"
    }
    else {
        Write-Error "❌ Falha no build de produção"
        exit 1
    }
    
    Pop-Location
}

# Verificar configuração do Git
function Test-Git {
    Write-Info "Verificando configuração do Git..."
    
    if (-not (Test-Path ".git")) {
        Write-Error "Este não é um repositório Git!"
        exit 1
    }
    
    # Verificar se há mudanças não commitadas
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Warning "⚠️  Há mudanças não commitadas no repositório"
        if (-not $Force) {
            $response = Read-Host "Deseja continuar mesmo assim? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Info "Deploy cancelado. Commit suas mudanças primeiro."
                exit 1
            }
        }
    }
    
    # Verificar branch atual
    $currentBranch = git branch --show-current
    if ($currentBranch -ne "main") {
        Write-Warning "⚠️  Você está na branch '$currentBranch', não na 'main'"
        if (-not $Force) {
            $response = Read-Host "Deseja continuar mesmo assim? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Info "Deploy cancelado. Mude para a branch main primeiro."
                exit 1
            }
        }
    }
    
    Write-Info "✅ Configuração do Git OK"
}

# Verificar configuração dos serviços
function Test-Services {
    Write-Info "Verificando configuração dos serviços..."
    
    # Verificar render.yaml
    if (-not (Test-Path "render.yaml")) {
        Write-Error "render.yaml não encontrado!"
        exit 1
    }
    
    # Verificar vercel.json
    if (-not (Test-Path "vercel.json")) {
        Write-Error "vercel.json não encontrado!"
        exit 1
    }
    
    Write-Info "✅ Arquivos de configuração encontrados"
}

# Deploy para GitHub (trigger automático)
function Deploy-ToGitHub {
    Write-Info "Fazendo push para GitHub (deploy automático)..."
    
    # Verificar se há mudanças para fazer push
    $gitStatus = git status --porcelain
    if (-not $gitStatus) {
        Write-Warning "Não há mudanças para fazer push"
        return
    }
    
    # Adicionar todas as mudanças
    git add .
    
    # Commit com timestamp
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "🚀 Deploy automático - $timestamp"
    
    # Push para main
    git push origin main
    
    Write-Info "✅ Push realizado com sucesso"
    Write-Info "🔗 Render e Vercel farão deploy automático"
}

# Mostrar status dos deploys
function Show-DeployStatus {
    Write-Info "Status dos deploys:"
    Write-Host ""
    Write-Host "📊 Backend (Render):"
    Write-Host "   - URL: https://chat-lleria.onrender.com"
    Write-Host "   - Health Check: https://chat-lleria.onrender.com/health"
    Write-Host ""
    Write-Host "🌐 Frontend (Vercel):"
    Write-Host "   - URL: https://gemini-chatbot.vercel.app"
    Write-Host ""
    Write-Host "📝 Logs:"
    Write-Host "   - Render: https://dashboard.render.com"
    Write-Host "   - Vercel: https://vercel.com/dashboard"
    Write-Host ""
    Write-Warning "⚠️  Os deploys podem levar alguns minutos para completar"
}

# Função principal
function Main {
    Write-Header
    
    # Verificar se estamos no diretório correto
    Test-ProjectRoot
    
    # Verificar dependências
    Test-Dependencies
    
    # Verificar configuração do Git
    Test-Git
    
    # Verificar configuração dos serviços
    Test-Services
    
    # Testar backend (se não pular testes)
    if (-not $SkipTests) {
        Test-Backend
    }
    else {
        Write-Warning "⚠️  Testes do backend pulados"
    }
    
    # Testar frontend (se não pular testes)
    if (-not $SkipTests) {
        Test-Frontend
    }
    else {
        Write-Warning "⚠️  Testes do frontend pulados"
    }
    
    # Deploy para GitHub
    Deploy-ToGitHub
    
    # Mostrar status
    Show-DeployStatus
    
    Write-Info "🎉 Deploy iniciado com sucesso!"
    Write-Info "Acompanhe o progresso nos dashboards dos serviços"
}

# Executar função principal
Main 