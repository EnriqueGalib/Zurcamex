param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage
)

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "🏢 ZUCARMEX - Sistema de Automatización de Pruebas" -ForegroundColor Green
Write-Host "📤 Subiendo cambios a GitHub..." -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Cyan

Write-Host "🔄 Agregando archivos al staging..." -ForegroundColor Yellow
git add .

Write-Host "📝 Creando commit con mensaje: '$CommitMessage'" -ForegroundColor Yellow
git commit -m $CommitMessage

Write-Host "📤 Subiendo cambios a GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cambios subidos exitosamente a GitHub!" -ForegroundColor Green
    Write-Host "📋 Commit: $CommitMessage" -ForegroundColor Cyan
} else {
    Write-Host "❌ Error al subir cambios a GitHub" -ForegroundColor Red
    Write-Host "🔍 Verifica tu conexión y credenciales" -ForegroundColor Yellow
}

Write-Host "================================================================================" -ForegroundColor Cyan