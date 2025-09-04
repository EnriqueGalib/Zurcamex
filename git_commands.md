# 📤 Comandos Git para ZUCARMEX

## 🚀 Subir Cambios a GitHub

### Opción 1: Script PowerShell (Recomendado)

```powershell
.\git_push.ps1 "Tu mensaje de commit aquí"
```

### Opción 2: Script Batch

```cmd
git_push.bat "Tu mensaje de commit aquí"
```

### Opción 3: Comandos Manuales

```bash
git add .
git commit -m "Tu mensaje de commit aquí"
git push origin main
```

## 📋 Ejemplos de Mensajes de Commit

### Para Mejoras de Funcionalidad:

-   "Mejoras en el flujo de 2FA con detección automática del HOME"
-   "Corrección de errores en environment.py y configuración de driver"
-   "Implementación de detección automática del HOME después del 2FA"

### Para Correcciones de Errores:

-   "Fix: Corregido error de \_cleanup_done en before_scenario"
-   "Fix: Solucionado problema con driver de Chrome"
-   "Fix: Corregidos errores de sintaxis en archivos Python"

### Para Nuevas Características:

-   "Feat: Agregado sistema de detección automática del HOME"
-   "Feat: Implementado timeout y fallback manual para 2FA"
-   "Feat: Mejorado sistema de logging y evidencias"

### Para Configuración:

-   "Config: Configurado entorno virtual y dependencias"
-   "Config: Actualizada configuración de Behave"
-   "Config: Mejorada configuración del driver de Chrome"

## 🔧 Comandos Útiles

### Ver Estado del Repositorio:

```bash
git status
```

### Ver Historial de Commits:

```bash
git log --oneline
```

### Ver Diferencias:

```bash
git diff
```

### Deshacer Último Commit (antes de push):

```bash
git reset --soft HEAD~1
```

## 📝 Notas Importantes

1. **Siempre revisa** los cambios antes de hacer commit
2. **Usa mensajes descriptivos** que expliquen qué se cambió
3. **Haz commits frecuentes** para mantener un historial claro
4. **No subas archivos sensibles** como contraseñas o tokens
5. **Verifica que el push sea exitoso** antes de continuar

## 🎯 Flujo Recomendado

1. Realizar cambios en el código
2. Probar que funcionen correctamente
3. Usar: `.\git_push.ps1 "Descripción de los cambios"`
4. Verificar que se subió correctamente
5. Continuar con el desarrollo
