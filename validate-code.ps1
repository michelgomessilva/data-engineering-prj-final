# validate-code.ps1
# Executa os hooks do pre-commit manualmente em todos os arquivos

Write-Host "Iniciando validação de código com pre-commit..." -ForegroundColor Cyan

# Verifica se pre-commit está instalado
if (-not (Get-Command pre-commit -ErrorAction SilentlyContinue)) {
    Write-Host "pre-commit não está instalado. Execute 'setup-precommit.ps1' primeiro." -ForegroundColor Red
    exit 1
}

# Executa os hooks em todos os arquivos
pre-commit run --all-files

if ($LASTEXITCODE -eq 0) {
    Write-Host "Validação concluída com sucesso. Nenhum problema encontrado." -ForegroundColor Green
} else {
    Write-Host "Validação concluída com falhas. Veja os erros acima." -ForegroundColor Yellow
    exit $LASTEXITCODE
}
