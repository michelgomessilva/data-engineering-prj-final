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
    Invoke-WebRequest -Uri "https://install.python-poetry.org" -OutFile $installerPath -UseBasicParsing -Encoding UTF8

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
# 3. Instalar dependências com Poetry
Write-Host "Instalando dependências do projeto..." -ForegroundColor Cyan
poetry install

# ----------------------------------------
# 4. Garantir que pre-commit está presente no projeto
Write-Host "Garantindo que pre-commit está listado..." -ForegroundColor Cyan
$hasPreCommit = poetry show --only=dev | Select-String "pre-commit"

if (-not $hasPreCommit) {
    poetry add --group dev pre-commit
    Write-Host "pre-commit adicionado às dependências de desenvolvimento." -ForegroundColor Green
} else {
    Write-Host "pre-commit já está listado como dependência." -ForegroundColor Green
}

# ----------------------------------------
# 5. Instalar os hooks do pre-commit
Write-Host "Instalando hooks do pre-commit..." -ForegroundColor Cyan
poetry run pre-commit install

# Garantir que o ambiente virtual usa Python 3.12
Write-Host "Garantindo que Poetry usa Python 3.12..." -ForegroundColor Cyan
poetry env use python3.12

# Ativar ambiente virtual após bootstrap
$venvPath = poetry env info --path
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
Write-Host "Ativando ambiente virtual: $activateScript" -ForegroundColor Cyan
& $activateScript

# ----------------------------------------
Write-Host "Ambiente configurado com sucesso!" -ForegroundColor Cyan
