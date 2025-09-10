# 🏢 ZUCARMEX - Sistema de Automatización de Pruebas

## 🤖 Credicam QA - Advanced Automated Testing Framework

### 📋 Descripción

Sistema avanzado de automatización de pruebas para la aplicación Credicam de Zucarmex, construido con Behave (BDD) y Selenium WebDriver, implementando el patrón Page Object Model (POM) con funcionalidades avanzadas de monitoreo, análisis y reportes.

### 🎯 Características Principales

-   ✅ **Framework BDD**: Behave con Gherkin para tests legibles
-   ✅ **Page Object Model**: Arquitectura mantenible y escalable
-   ✅ **Selenium WebDriver**: Automatización robusta de navegadores
-   ✅ **Sistema de Logging Avanzado**: Logs organizados por fecha/feature con análisis automático
-   ✅ **Captura de Evidencias**: Screenshots automáticos organizados por resultado
-   ✅ **Reportes Múltiples**: HTML, JSON, JUnit y PDFs profesionales
-   ✅ **Validación de Elementos**: Verificación automática antes de ejecución
-   ✅ **Reutilización de Código**: Sistema inteligente de detección de código reutilizable
-   ✅ **Gestión de 2FA**: Flujo híbrido para autenticación OKTA
-   ✅ **Configuración Flexible**: Múltiples entornos (DEV/QA)
-   ✅ **Limpieza Automática**: Gestión inteligente de archivos antiguos
-   ✅ **Análisis de Fallos**: Diagnóstico automático con recomendaciones

### 📁 Estructura del Proyecto

```
ZUCARMEX_CURSOR/
├── features/              # Tests en Gherkin (.feature)
│   ├── US12_8_Crear_y_Configurar_un_Catalogo.feature
│   ├── environment.py     # Configuración de entorno
│   └── steps/            # Implementación de steps
│       └── alta_catalogo_steps.py
├── pages/                # Page Objects (POM)
│   ├── login_page.py
│   └── catalogo_page.py
├── locators/             # Selectores web organizados
│   ├── login_locators.py
│   └── catalogo_locators.py
├── utils/                # Utilidades avanzadas del framework
│   ├── advanced_logger.py        # Sistema de logging organizado
│   ├── logger_config.py          # Configuración de logging
│   ├── element_validator.py      # Validación automática de elementos
│   ├── code_reuse_helper.py      # Detección de código reutilizable
│   ├── automation_helper.py      # Helper principal integrado
│   ├── evidence_manager.py       # Gestión de evidencias
│   ├── pdf_generator.py          # Generación de PDFs profesionales
│   ├── execution_report_generator.py
│   ├── cleanup_manager.py        # Limpieza automática
│   └── documentation_manager.py  # Documentación automática
├── logs/                 # Logs organizados por fecha/feature
│   └── 2025_01_04/
│       └── alta_catalogo/
│           └── scenario_timestamp.log
├── reports/              # Reportes HTML/JSON/JUnit
├── evidences/            # Screenshots organizados por resultado
│   └── 2025-01-04/
│       └── alta_catalogo/
│           ├── EXITOSOS/
│           ├── FALLIDOS/
│           └── PARCIALES/
├── pdfs/                 # Documentos PDF para clientes
│   └── 2025_01_04/
│       └── alta_catalogo/
│           ├── EXITOSOS/
│           ├── FALLIDOS/
│           └── PARCIALES/
├── docs/                 # Documentación automática
│   ├── EXITOSOS/
│   ├── FALLIDOS/
│   ├── PARCIALES/
│   └── DESCONOCIDOS/
├── config.json           # Configuración principal
├── behave.ini           # Configuración de Behave
├── requirements.txt     # Dependencias Python
├── run_tests.py         # Script principal de ejecución
├── setup.py            # Configuración del paquete
├── .cursorrules        # Reglas para Cursor AI
└── MANUAL_INSTALACION.md # Guía de instalación detallada
```

### 🚀 Instalación y Configuración

#### Prerrequisitos

-   Python 3.8+
-   Google Chrome
-   Git (opcional)

#### Instalación Rápida

```bash
# Clonar el repositorio
git clone <repository-url>
cd ZUCARMEX_CURSOR

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python run_tests.py --check-deps
```

#### Configuración Inicial

1. Editar `config.json` con tus credenciales y URLs
2. Verificar configuración: `python run_tests.py --check-deps`
3. Listar features: `python run_tests.py --list-features`
4. Ejecutar prueba de ejemplo: `python run_tests.py --feature alta_catalogo`

### 🧪 Ejecución de Pruebas

#### Comandos Básicos

```bash
# Ejecutar todas las pruebas
python run_tests.py

# Ejecutar feature específico
python run_tests.py --feature alta_catalogo

# Generar reporte HTML
python run_tests.py --format html

# Ejecutar con tags específicos
python run_tests.py --tags @smoke
```

#### Opciones Avanzadas

```bash
# Verificar dependencias
python run_tests.py --check-deps

# Listar features disponibles
python run_tests.py --list-features

# Modo verbose
python run_tests.py --verbose

# Combinar opciones
python run_tests.py --feature alta_catalogo --format html --verbose
```

### 🔍 Validación Automática de Elementos

#### Verificación Previa

```python
from utils.element_validator import check_elements_before_execution

# Verificar elementos antes de ejecutar
if check_elements_before_execution(driver, "alta_catalogo"):
    print("✅ Todos los elementos válidos, listo para ejecutar")
else:
    print("❌ Elementos faltantes, revisar selectores")
```

#### Validación Completa

```python
from utils.element_validator import ElementValidator

validator = ElementValidator(driver)
result = validator.validate_feature_elements("alta_catalogo")

if result['overall_status'] == 'SUCCESS':
    print("✅ Validación exitosa")
else:
    print(f"⚠️ {result['invalid_elements']} elementos inválidos")
```

### 🔄 Reutilización de Código

#### Buscar Código Reutilizable

```python
from utils.code_reuse_helper import CodeReuseHelper

helper = CodeReuseHelper()

# Buscar código para nueva funcionalidad
suggestions = helper.suggest_code_reuse("login de usuario")

print(f"Steps reutilizables: {len(suggestions['reusable_steps'])}")
print(f"Page Objects: {len(suggestions['reusable_pages'])}")
print(f"Locators: {len(suggestions['reusable_locators'])}")
```

#### Generar Template

```python
# Crear template para nueva funcionalidad
template = helper.create_reuse_template("gestión de usuarios")
print(template)
```

### 📊 Sistema de Logging Avanzado

#### Logging Estructurado

```python
from utils.advanced_logger import advanced_logger

# Obtener logger organizado por fecha/feature
logger = advanced_logger.get_test_logger("alta_catalogo", "crear_catalogo")

# Log de ejecución de step
advanced_logger.log_step_execution(
    logger, "Navegar a login", "given", "SUCCESS", 2.5
)

# Log de error con contexto
advanced_logger.log_error_details(
    logger, exception, {"page": "login", "element": "username_field"}
)
```

### 📄 Generación de PDFs Profesionales

#### PDFs Automáticos

Los PDFs se generan automáticamente al finalizar cada ejecución:

```
pdfs/
├── 2025_01_04/
│   └── alta_catalogo/
│       ├── EXITOSOS/
│       │   └── SUCCESS_crear_catalogo_20250104_101530.html
│       └── FALLIDOS/
│           └── FAILURE_ANALYSIS_crear_catalogo_20250104_102030.html
```

#### Contenido de PDFs

-   **Ejecuciones Exitosas**: Resumen de pasos, evidencias, métricas
-   **Ejecuciones Fallidas**: Análisis detallado, recomendaciones, checklist
-   **Metadatos**: Información completa de la ejecución

### 🧹 Limpieza Automática

#### Configuración de Retención

```json
{
    "evidence_management": {
        "retention_days": 30,
        "archive_after_days": 90,
        "cleanup_temp_files": true
    }
}
```

#### Limpieza Manual

```python
from utils.automation_helper import automation_helper

# Limpiar archivos antiguos (más de 30 días)
cleanup_stats = automation_helper.cleanup_old_files(30)
print(f"Archivos limpiados: {cleanup_stats}")
```

### 🎨 Integración con Cursor AI

El archivo `.cursorrules` proporciona reglas específicas para Cursor AI:

-   **Creación de Pruebas**: Proceso estándar con validación previa
-   **Reutilización de Código**: Búsqueda automática de funcionalidades existentes
-   **Validación de Elementos**: Verificación antes de ejecución
-   **Organización de Archivos**: Estructura consistente por fecha/feature

### 📊 Reportes y Evidencias

#### Tipos de Reportes

-   **HTML**: Reportes visuales detallados
-   **JSON**: Datos estructurados para análisis
-   **JUnit**: Compatible con CI/CD
-   **PDF**: Documentos profesionales para clientes
-   **Análisis de Fallos**: Diagnóstico automático con recomendaciones

#### Organización Automática

-   **Logs**: `logs/[fecha]/[feature]/[scenario]_[timestamp].log`
-   **Evidencias**: `evidences/[fecha]/[feature]/[resultado]/screenshots/`
-   **Reportes**: `reports/[fecha]_[feature]/execution_report_[timestamp].html`
-   **PDFs**: `pdfs/[fecha]_[feature]/[resultado]/[archivo].html`
-   **Documentación**: `docs/[resultado]/[archivo].md`

### 🔧 Configuración Avanzada

#### Variables de Entorno

```bash
export ZUCARMEX_ENV=qa
export ZUCARMEX_URL=https://credicam-qa.zucarmex.com/login
```

#### Configuración de Navegador

```json
{
    "driver_settings": {
        "implicit_wait": 10,
        "page_load_timeout": 30,
        "screenshot_on_failure": true,
        "maximize_window": true
    }
}
```

### 🛠️ Desarrollo y Mantenimiento

#### Agregar Nuevas Pruebas

1. **Análisis**: Usar `code_reuse_helper` para buscar código existente
2. **Validación**: Verificar elementos con `element_validator`
3. **Implementación**: Crear archivos siguiendo la estructura estándar
4. **Testing**: Ejecutar con logging avanzado

#### Patrones de Código

-   **Naming**: `snake_case` para archivos y funciones
-   **Page Objects**: Un archivo por página
-   **Locators**: Separados por funcionalidad
-   **Steps**: Implementación clara y reutilizable
-   **Logging**: Uso del sistema avanzado de logging

### 🔐 Flujo de Autenticación con 2FA

La automatización incluye un flujo híbrido para el **Two-Factor Authentication**:

1. **Login automático** con usuario y contraseña
2. **Pausa automática** para validación manual del 2FA
3. **Verificación automática** de autenticación completa
4. **Continuación automática** del flujo de catálogos

### 🐛 Solución de Problemas

#### Error: ChromeDriver no encontrado

```bash
# El proyecto usa webdriver-manager automáticamente
# Si hay problemas, instalar manualmente:
pip install webdriver-manager
```

#### Error: Elemento no encontrado

-   Usar `element_validator` para verificar elementos antes de ejecutar
-   Verificar que los locators en `locators/` sean correctos
-   Revisar si la aplicación ha cambiado su estructura

#### Error: Timeout

-   Aumentar timeouts en `environment.py`
-   Verificar conectividad a la aplicación
-   Revisar si la aplicación está lenta

### 📞 Soporte y Contacto

-   **QA Team**: qa@zucarmex.com
-   **Tech Lead**: tech-lead@zucarmex.com
-   **Documentación**: Ver carpeta `docs/` y `MANUAL_INSTALACION.md`

### 📄 Licencia

Este proyecto es propiedad de Zucarmex y está destinado para uso interno únicamente.

---

_Sistema de Automatización de Pruebas Avanzado - Zucarmex v2.0_
