Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "🏢 ZUCARMEX - Sistema de Automatización de Pruebas" -ForegroundColor Green
Write-Host "🤖 Activando entorno virtual..." -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "❌ Entorno virtual no encontrado. Creando..." -ForegroundColor Red
    python -m venv .venv
    Write-Host "✅ Entorno virtual creado." -ForegroundColor Green
}

Write-Host "🔄 Activando entorno virtual..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

Write-Host "✅ Entorno virtual activado correctamente!" -ForegroundColor Green
Write-Host "📋 Para ejecutar las pruebas, usa: python run_tests.py --feature US12_8_Crear_y_Configurar_un_Catalogo" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
