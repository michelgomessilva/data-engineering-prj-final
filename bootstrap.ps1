# Configura o terminal para UTF-8 (resolvendo problemas de acentuação de comandos como poetry e pre-commit)
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "`n==> Bootstrap do ambiente de desenvolvimento Poetry" -ForegroundColor Cyan

# ----------------------------------------
# Função para verificar se um comando existe
function Command-Exists {
    param ([string]$cmd)
    return $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

# ----------------------------------------
# 1. Verificar se Python está instalado
if (Command-Exists "python") {
    $pyVersion = python --version
    Write-Host "Python instalado: $pyVersion" -ForegroundColor Green
} else {
    Write-Host "Python não encontrado. Por favor instale manualmente." -ForegroundColor Red
    exit 1
}

# ----------------------------------------
# 2. Verificar ou instalar Poetry
if (Command-Exists "poetry") {
    $poetryVersion = poetry --version
    Write-Host "Poetry já instalado: $poetryVersion" -ForegroundColor Green
} else {
    Write-Host "Instalando Poetry..." -ForegroundColor Yellow

    $installerPath = "$env:TEMP\install-poetry.py"
    Invoke-WebRequest -Uri "https://install.python-poetry.org" -OutFile $installerPath -UseBasicParsing
    python $installerPath

    $poetryPath = "$env:APPDATA\Python\Scripts"
    if ($env:PATH -notlike "*$poetryPath*") {
        $env:PATH += ";$poetryPath"
        Write-Host "Adicionado $poetryPath ao PATH temporário." -ForegroundColor Cyan
    }

    if (Command-Exists "poetry") {
        $poetryVersion = poetry --version
        Write-Host "Poetry instalado: $poetryVersion" -ForegroundColor Green
    } else {
        Write-Host "Erro ao instalar o Poetry." -ForegroundColor Red
        exit 1
    }
}

# ----------------------------------------
# 3. Garantir que Poetry usa Python 3.10
Write-Host "Garantindo que Poetry usa Python 3.10..." -ForegroundColor Cyan
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($null -ne $pythonCmd) {
    $pythonFullPath = $pythonCmd.Source
    Write-Host "Forçando Poetry a usar: $pythonFullPath" -ForegroundColor Yellow
    poetry env use $pythonFullPath
} else {
    Write-Host "Python 3.10 não encontrado. Aborte o bootstrap ou instale com Chocolatey:" -ForegroundColor Red
    Write-Host "    choco install python --version=3.10.11 -y --allow-downgrade" -ForegroundColor DarkYellow
    exit 1
}

# ----------------------------------------
# 4. Corrigir e instalar dependências com Poetry
Write-Host "Verificando lockfile..." -ForegroundColor Cyan
poetry lock

Write-Host "Instalando dependências do projeto..." -ForegroundColor Cyan
poetry install

# ----------------------------------------
# 5. Garantir que pre-commit está presente no projeto
Write-Host "Garantindo que pre-commit está listado..." -ForegroundColor Cyan
$hasPreCommit = poetry show --only=dev | Select-String "pre-commit"

if (-not $hasPreCommit) {
    poetry add --group dev pre-commit
    Write-Host "pre-commit adicionado às dependências de desenvolvimento." -ForegroundColor Green
} else {
    Write-Host "pre-commit já está listado como dependência." -ForegroundColor Green
}

# ----------------------------------------
# 6. Ativar ambiente virtual após bootstrap
$venvPath = poetry env info --path
if (-not $venvPath) {
    Write-Host "Erro ao obter o caminho do ambiente virtual do Poetry." -ForegroundColor Red
    exit 1
}

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
Write-Host "Ativando ambiente virtual: $activateScript" -ForegroundColor Cyan
& $activateScript

# ----------------------------------------
# 7. Instalar hooks do pre-commit (após ativar o ambiente)
Write-Host "Instalando hooks do pre-commit..." -ForegroundColor Cyan
pre-commit install

# ----------------------------------------
# 8. Configurar variáveis para compatibilidade com Spark
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
$env:PYSPARK_PYTHON = $pythonPath
$env:PYSPARK_DRIVER_PYTHON = $pythonPath

Write-Host "PYSPARK_PYTHON configurada: $env:PYSPARK_PYTHON" -ForegroundColor Cyan
Write-Host "PYSPARK_DRIVER_PYTHON configurada: $env:PYSPARK_DRIVER_PYTHON" -ForegroundColor Cyan

# ----------------------------------------
# 9. Configurar GOOGLE_APPLICATION_CREDENTIALS
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:/Users/miche/AppData/Roaming/gcloud/application_default_credentials.json"
Write-Host "GOOGLE_APPLICATION_CREDENTIALS configurada: $env:GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Cyan

# ----------------------------------------
Write-Host "Ambiente configurado com sucesso!" -ForegroundColor Green
# ----------------------------------------
