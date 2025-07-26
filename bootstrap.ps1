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
    $versionOutput = & $pythonFullPath --version 2>&1
    # Remove "Python " do início
    $pythonVersion = $versionOutput -replace '^Python\s+', ''

    if ($pythonVersion.StartsWith("3.10")) {
        Write-Host "Python 3.10 encontrado: $pythonVersion" -ForegroundColor Green
        Write-Host "Forçando Poetry a usar: $pythonFullPath" -ForegroundColor Yellow
        poetry env use $pythonFullPath
    } else {
        Write-Host "Python encontrado, mas a versão é $pythonVersion. Requerido: 3.10.x" -ForegroundColor Red
        Write-Host "Instale a versão correta com Chocolatey:" -ForegroundColor DarkYellow
        Write-Host "    choco install python --version=3.10.11 -y --allow-downgrade" -ForegroundColor DarkYellow
        exit 1
    }
} else {
    Write-Host "Python não encontrado no sistema. Instale a versão 3.10 com Chocolatey:" -ForegroundColor Red
    Write-Host "    choco install python --version=3.10.11 -y --allow-downgrade" -ForegroundColor DarkYellow
    exit 1
}


# -----------------------------------------
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
# 7.5 Instalar DBT (core + BigQuery adapter)
Write-Host "Verificando se dbt-core e dbt-bigquery estão instalados..." -ForegroundColor Cyan

$hasDbtCore = poetry show | Select-String "dbt-core"
$hasDbtBQ = poetry show | Select-String "dbt-bigquery"

if (-not $hasDbtCore -or -not $hasDbtBQ) {
    Write-Host "Instalando dbt-core e dbt-bigquery via Poetry..." -ForegroundColor Yellow
    poetry add dbt-core dbt-bigquery
    Write-Host "DBT (core + BigQuery adapter) instalado com sucesso." -ForegroundColor Green
} else {
    Write-Host "dbt-core e dbt-bigquery já estão instalados." -ForegroundColor Green
}

# ----------------------------------------
# 7.6 Criar alias dbt para usar com Poetry
Write-Host "Criando alias 'dbt' para 'poetry run dbt'" -ForegroundColor Cyan
Set-Alias dbt "poetry run dbt"


# ----------------------------------------
# 8. Configurar variáveis para compatibilidade com Spark
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
$env:PYSPARK_PYTHON = $pythonPath
$env:PYSPARK_DRIVER_PYTHON = $pythonPath

Write-Host "PYSPARK_PYTHON configurada: $env:PYSPARK_PYTHON" -ForegroundColor Cyan
Write-Host "PYSPARK_DRIVER_PYTHON configurada: $env:PYSPARK_DRIVER_PYTHON" -ForegroundColor Cyan

# ----------------------------------------
# 9. Configurar GOOGLE_APPLICATION_CREDENTIALS
Write-Host "Carregando variável do .env..." -ForegroundColor Cyan

$envPath = ".env"
if (-Not (Test-Path $envPath)) {
    Write-Host "Arquivo .env não encontrado." -ForegroundColor Red
    exit 1
}

$googleCredsPath = Get-Content $envPath | Where-Object { $_ -match "^GOOGLE_APPLICATION_CREDENTIALS=" } |
    ForEach-Object { ($_ -split '=', 2)[1].Trim('"') }

if ($googleCredsPath) {
    $env:GOOGLE_APPLICATION_CREDENTIALS = $googleCredsPath
    Write-Host "GOOGLE_APPLICATION_CREDENTIALS definido para: $googleCredsPath" -ForegroundColor Green
} else {
    Write-Host "Variável GOOGLE_APPLICATION_CREDENTIALS não encontrada no .env" -ForegroundColor Red
    exit 1
}

# ----------------------------------------
Write-Host "Ambiente configurado com sucesso!" -ForegroundColor Green
# ----------------------------------------
