@echo off
echo ================================================================================
echo 🏢 ZUCARMEX - Sistema de Automatización de Pruebas
echo 📤 Subiendo cambios a GitHub...
echo ================================================================================

if "%1"=="" (
    echo ❌ Error: Debes proporcionar un mensaje de commit
    echo Uso: git_push.bat "mensaje del commit"
    echo Ejemplo: git_push.bat "Mejoras en el flujo de 2FA"
    pause
    exit /b 1
)

set COMMIT_MESSAGE=%1

echo 🔄 Agregando archivos al staging...
git add .

echo 📝 Creando commit con mensaje: "%COMMIT_MESSAGE%"
git commit -m "%COMMIT_MESSAGE%"

echo 📤 Subiendo cambios a GitHub...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo ✅ Cambios subidos exitosamente a GitHub!
    echo 📋 Commit: %COMMIT_MESSAGE%
) else (
    echo ❌ Error al subir cambios a GitHub
    echo 🔍 Verifica tu conexión y credenciales
)

echo ================================================================================
pause
