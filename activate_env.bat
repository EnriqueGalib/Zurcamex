@echo off
echo ================================================================================
echo 🏢 ZUCARMEX - Sistema de Automatización de Pruebas
echo 🤖 Activando entorno virtual...
echo ================================================================================

if not exist ".venv" (
    echo ❌ Entorno virtual no encontrado. Creando...
    python -m venv .venv
    echo ✅ Entorno virtual creado.
)

echo 🔄 Activando entorno virtual...
call .venv\Scripts\activate.bat

echo ✅ Entorno virtual activado correctamente!
echo 📋 Para ejecutar las pruebas, usa: python run_tests.py --feature alta_catalogo
echo ================================================================================
