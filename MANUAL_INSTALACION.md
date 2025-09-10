# 🚀 Manual de Instalación y Configuración

## Sistema de Automatización Zucarmex - Credicam QA

### 📋 Prerrequisitos

#### Software Requerido

-   **Python 3.8 o superior** - [Descargar aquí](https://www.python.org/downloads/)
-   **Google Chrome** - [Descargar aquí](https://www.google.com/chrome/)
-   **Git** (opcional) - [Descargar aquí](https://git-scm.com/)

#### Verificación de Python

```bash
python --version
# Debe mostrar Python 3.8.x o superior
```

### 🛠️ Instalación Paso a Paso

#### 1. Preparar el Entorno

```bash
# Crear directorio para el proyecto
mkdir zucarmex_automation
cd zucarmex_automation

# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate
```

#### 2. Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

#### 3. Configurar ChromeDriver

El sistema usa `webdriver-manager` que descarga automáticamente el ChromeDriver correcto, pero puedes verificar:

```bash
# Verificar que Chrome está instalado
chrome --version

# El sistema descargará automáticamente el driver compatible
```

### ⚙️ Configuración Inicial

#### 1. Verificar Archivos de Configuración

Asegúrate de que existen estos archivos:

-   ✅ `config.json` - Configuración principal
-   ✅ `behave.ini` - Configuración de Behave
-   ✅ `requirements.txt` - Dependencias Python

#### 2. Personalizar Configuración

Edita `config.json` según tu entorno:

```json
{
    "env": "qa",
    "urls": {
        "dev": "https://credicam-dev.zucarmex.com/login",
        "qa": "https://credicam-qa.zucarmex.com/login"
    },
    "test_data": {
        "usuario_qa": "tu-usuario@zucarmex.com",
        "password_qa": "tu-contraseña"
    }
}
```

#### 3. Verificar Estructura de Directorios

El sistema creará automáticamente estos directorios:

```
ZUCARMEX_CURSOR/
├── features/           ✅ Tests en Gherkin
├── pages/              ✅ Page Objects
├── locators/           ✅ Selectores web
├── utils/              ✅ Utilidades
├── logs/               📁 Se crea automáticamente
├── reports/            📁 Se crea automáticamente
├── evidences/          📁 Se crea automáticamente
├── pdfs/               📁 Se crea automáticamente
└── docs/               📁 Se crea automáticamente
```

### 🧪 Verificación de Instalación

#### 1. Verificar Dependencias

```bash
python run_tests.py --check-deps
```

#### 2. Listar Features Disponibles

```bash
python run_tests.py --list-features
```

#### 3. Ejecutar Test de Prueba

```bash
# Ejecutar con formato pretty (por defecto)
python run_tests.py --feature US12_8_Crear_y_Configurar_un_Catalogo

# Ejecutar con reporte HTML
python run_tests.py --feature US12_8_Crear_y_Configurar_un_Catalogo --format html
```

### 🔧 Solución de Problemas Comunes

#### Problema: "behave no encontrado"

```bash
# Solución: Instalar behave
pip install behave

# O reinstalar todas las dependencias
pip install -r requirements.txt
```

#### Problema: "ChromeDriver no compatible"

```bash
# Solución: Actualizar webdriver-manager
pip install --upgrade webdriver-manager

# O limpiar caché de drivers
rm -rf ~/.wdm
```

#### Problema: "Selenium WebDriverException"

```bash
# Solución: Verificar Chrome
chrome --version

# Actualizar Chrome si es necesario
# Reiniciar el sistema si acabas de instalar Chrome
```

#### Problema: Permisos en Windows

```powershell
# Ejecutar PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# O usar Command Prompt en lugar de PowerShell
```

### 🎯 Configuración Avanzada

#### 1. Variables de Entorno (Opcional)

```bash
# Configurar variables de entorno
export ZUCARMEX_ENV=qa
export ZUCARMEX_URL=https://credicam-qa.zucarmex.com/login
export CHROME_DRIVER_PATH=/path/to/chromedriver
```

#### 2. Configuración de IDE

##### Visual Studio Code

Extensiones recomendadas:

-   Python
-   Cucumber (Gherkin) Full Support
-   Python Test Explorer

##### PyCharm

1. Marcar `features` como Sources Root
2. Configurar intérprete Python del venv
3. Instalar plugin Gherkin

#### 3. Configuración de Logging

Personalizar en `config.json`:

```json
{
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file_logging": true,
        "console_logging": true
    }
}
```

### 📊 Configuración de Reportes

#### 1. Reportes HTML

```bash
# Generar reporte HTML
python run_tests.py --format html

# El reporte se genera en: reports/execution_[timestamp]/report.html
```

#### 2. Reportes JSON

```bash
# Generar reporte JSON
python run_tests.py --format json

# El reporte se genera en: reports/execution_[timestamp]/report.json
```

#### 3. Reportes JUnit (Para CI/CD)

```bash
# Generar reporte JUnit
python run_tests.py --format junit

# Los reportes se generan en: reports/execution_[timestamp]/
```

### 🔄 Integración con CI/CD

#### GitHub Actions

```yaml
name: Zucarmex Automation Tests

on: [push, pull_request]

jobs:
    test:
        runs-on: ubuntu-latest

        steps:
            - uses: actions/checkout@v2

            - name: Set up Python
              uses: actions/setup-python@v2
              with:
                  python-version: '3.9'

            - name: Install dependencies
              run: |
                  pip install -r requirements.txt

            - name: Run tests
              run: |
                  python run_tests.py --format junit

            - name: Upload test results
              uses: actions/upload-artifact@v2
              with:
                  name: test-results
                  path: reports/
```

#### Jenkins

```groovy
pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python run_tests.py --format junit'
            }
        }
    }

    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: '*.html',
                reportName: 'Automation Report'
            ])
        }
    }
}
```

### 📱 Configuración para Diferentes Entornos

#### Desarrollo Local

```json
{
    "env": "dev",
    "driver_settings": {
        "headless": false,
        "maximize_window": true,
        "implicit_wait": 10
    }
}
```

#### Servidor de CI/CD

```json
{
    "env": "ci",
    "driver_settings": {
        "headless": true,
        "window_size": "1920,1080",
        "implicit_wait": 15
    }
}
```

### 📞 Soporte y Contacto

#### Documentación

-   **README.md**: Información general del proyecto
-   **docs/**: Documentación detallada por carpetas
-   **Código comentado**: Todos los archivos incluyen documentación

#### Logs y Debugging

-   **Logs detallados**: `logs/[feature]/[scenario]/test_[timestamp].log`
-   **Screenshots**: `evidences/[fecha]/[feature]/[resultado]/screenshots/`
-   **Reportes HTML**: `reports/[fecha]_[feature]/execution_report_[timestamp].html`

#### Contacto del Equipo

-   **QA Team**: qa@zucarmex.com
-   **Tech Lead**: tech-lead@zucarmex.com
-   **Soporte**: soporte@zucarmex.com

### ✅ Checklist Final

Antes de considerar la instalación completa, verifica:

-   [ ] Python 3.8+ instalado y funcionando
-   [ ] Chrome browser instalado y actualizado
-   [ ] Entorno virtual creado y activado
-   [ ] Todas las dependencias instaladas sin errores
-   [ ] `python run_tests.py --check-deps` pasa exitosamente
-   [ ] `python run_tests.py --list-features` muestra los features
-   [ ] Configuración personalizada en `config.json`
-   [ ] Al menos un test ejecutado exitosamente
-   [ ] Reportes generándose correctamente
-   [ ] Evidencias capturándose en `evidences/`

### 🎉 ¡Instalación Completa!

Si todos los checks anteriores pasan, tu instalación está completa y lista para usar.

**Próximos pasos recomendados:**

1. Ejecutar todos los tests: `python run_tests.py`
2. Revisar reportes generados
3. Personalizar configuración según necesidades
4. Integrar con tu pipeline de CI/CD
5. Capacitar al equipo en el uso del framework

---

_Manual de instalación para Sistema de Automatización Zucarmex v1.0_
