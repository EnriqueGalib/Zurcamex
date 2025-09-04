"""
Utilidad para ayudar a encontrar código reutilizable en el proyecto
Sistema avanzado de reutilización de código para automatización de pruebas
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CodeReuseHelper:
    """Helper para encontrar código reutilizable en el proyecto"""

    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.features_dir = self.project_root / "features"
        self.pages_dir = self.project_root / "pages"
        self.locators_dir = self.project_root / "locators"
        self.utils_dir = self.project_root / "utils"
        self.logger = logging.getLogger(__name__)

        # Cache para optimizar búsquedas
        self._code_cache = {}
        self._last_scan = None

    def find_similar_steps(self, step_text):
        """
        Busca steps similares en los archivos existentes

        Args:
            step_text (str): Texto del step a buscar

        Returns:
            list: Lista de steps similares encontrados
        """
        similar_steps = []

        if not self.features_dir.exists():
            return similar_steps

        # Buscar en archivos de steps
        steps_files = list(self.features_dir.rglob("*_steps.py"))

        for steps_file in steps_files:
            try:
                with open(steps_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Buscar decoradores de steps
                step_pattern = r'@(given|when|then)\s*\(\s*["\']([^"\']+)["\']'
                matches = re.findall(step_pattern, content, re.IGNORECASE)

                for step_type, step_content in matches:
                    # Verificar similitud
                    if self._is_similar_step(step_text, step_content):
                        similar_steps.append(
                            {
                                "file": str(steps_file),
                                "type": step_type,
                                "content": step_content,
                                "similarity": self._calculate_similarity(
                                    step_text, step_content
                                ),
                            }
                        )

            except (IOError, OSError) as e:
                print(f"Error leyendo {steps_file}: {e}")

        # Ordenar por similitud
        similar_steps.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_steps

    def find_reusable_page_objects(self, functionality):
        """
        Busca Page Objects que puedan ser reutilizados

        Args:
            functionality (str): Funcionalidad que se necesita

        Returns:
            list: Lista de Page Objects reutilizables
        """
        reusable_pages = []

        if not self.pages_dir.exists():
            return reusable_pages

        # Buscar archivos de Page Objects
        page_files = list(self.pages_dir.glob("*_page.py"))

        for page_file in page_files:
            try:
                with open(page_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Buscar métodos que puedan ser útiles
                method_pattern = r"def\s+(\w+)\s*\("
                methods = re.findall(method_pattern, content)

                # Verificar si algún método es relevante
                relevant_methods = []
                for method in methods:
                    if self._is_relevant_method(method, functionality):
                        relevant_methods.append(method)

                if relevant_methods:
                    reusable_pages.append(
                        {
                            "file": str(page_file),
                            "class_name": page_file.stem.replace("_page", "Page"),
                            "methods": relevant_methods,
                            "relevance": len(relevant_methods),
                        }
                    )

            except (IOError, OSError) as e:
                print(f"Error leyendo {page_file}: {e}")

        # Ordenar por relevancia
        reusable_pages.sort(key=lambda x: x["relevance"], reverse=True)
        return reusable_pages

    def find_reusable_locators(self, element_type):
        """
        Busca Locators que puedan ser reutilizados

        Args:
            element_type (str): Tipo de elemento que se necesita

        Returns:
            list: Lista de Locators reutilizables
        """
        reusable_locators = []

        if not self.locators_dir.exists():
            return reusable_locators

        # Buscar archivos de Locators
        locator_files = list(self.locators_dir.glob("*_locators.py"))

        for locator_file in locator_files:
            try:
                with open(locator_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Buscar constantes de locators
                locator_pattern = r'(\w+)\s*=\s*["\']([^"\']+)["\']'
                matches = re.findall(locator_pattern, content)

                relevant_locators = []
                for locator_name, locator_value in matches:
                    if self._is_relevant_locator(locator_name, element_type):
                        relevant_locators.append(
                            {"name": locator_name, "value": locator_value}
                        )

                if relevant_locators:
                    reusable_locators.append(
                        {
                            "file": str(locator_file),
                            "class_name": locator_file.stem.replace(
                                "_locators", "Locators"
                            ),
                            "locators": relevant_locators,
                            "relevance": len(relevant_locators),
                        }
                    )

            except (IOError, OSError) as e:
                print(f"Error leyendo {locator_file}: {e}")

        # Ordenar por relevancia
        reusable_locators.sort(key=lambda x: x["relevance"], reverse=True)
        return reusable_locators

    def find_reusable_utilities(self, utility_type):
        """
        Busca utilidades que puedan ser reutilizadas

        Args:
            utility_type (str): Tipo de utilidad que se necesita

        Returns:
            list: Lista de utilidades reutilizables
        """
        reusable_utilities = []

        if not self.utils_dir.exists():
            return reusable_utilities

        # Buscar archivos de utilidades
        utility_files = list(self.utils_dir.glob("*.py"))

        for utility_file in utility_files:
            try:
                with open(utility_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Buscar funciones que puedan ser útiles
                function_pattern = r"def\s+(\w+)\s*\("
                functions = re.findall(function_pattern, content)

                relevant_functions = []
                for function in functions:
                    if self._is_relevant_function(function, utility_type):
                        relevant_functions.append(function)

                if relevant_functions:
                    reusable_utilities.append(
                        {
                            "file": str(utility_file),
                            "functions": relevant_functions,
                            "relevance": len(relevant_functions),
                        }
                    )

            except (IOError, OSError) as e:
                print(f"Error leyendo {utility_file}: {e}")

        # Ordenar por relevancia
        reusable_utilities.sort(key=lambda x: x["relevance"], reverse=True)
        return reusable_utilities

    def _is_similar_step(self, step1, step2):
        """Verifica si dos steps son similares"""
        # Normalizar textos
        step1_norm = step1.lower().strip()
        step2_norm = step2.lower().strip()

        # Verificar palabras clave comunes
        keywords1 = set(step1_norm.split())
        keywords2 = set(step2_norm.split())

        # Calcular intersección
        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)

        # Calcular similitud
        similarity = len(intersection) / len(union) if union else 0

        return similarity > 0.3  # 30% de similitud

    def _calculate_similarity(self, step1, step2):
        """Calcula la similitud entre dos steps"""
        step1_norm = step1.lower().strip()
        step2_norm = step2.lower().strip()

        keywords1 = set(step1_norm.split())
        keywords2 = set(step2_norm.split())

        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)

        return len(intersection) / len(union) if union else 0

    def _is_relevant_method(self, method_name, functionality):
        """Verifica si un método es relevante para la funcionalidad"""
        method_lower = method_name.lower()
        functionality_lower = functionality.lower()

        # Palabras clave relevantes
        relevant_keywords = [
            "login",
            "navigate",
            "click",
            "fill",
            "save",
            "create",
            "edit",
            "delete",
            "search",
            "select",
            "wait",
            "verify",
        ]

        # Verificar si el método contiene palabras clave relevantes
        for keyword in relevant_keywords:
            if keyword in method_lower and keyword in functionality_lower:
                return True

        return False

    def _is_relevant_locator(self, locator_name, element_type):
        """Verifica si un locator es relevante para el tipo de elemento"""
        locator_lower = locator_name.lower()
        element_lower = element_type.lower()

        # Palabras clave relevantes
        relevant_keywords = [
            "button",
            "input",
            "field",
            "menu",
            "link",
            "text",
            "form",
            "table",
            "list",
            "dropdown",
            "checkbox",
            "radio",
        ]

        # Verificar si el locator contiene palabras clave relevantes
        for keyword in relevant_keywords:
            if keyword in locator_lower and keyword in element_lower:
                return True

        return False

    def _is_relevant_function(self, function_name, utility_type):
        """Verifica si una función es relevante para el tipo de utilidad"""
        function_lower = function_name.lower()
        utility_lower = utility_type.lower()

        # Palabras clave relevantes
        relevant_keywords = [
            "screenshot",
            "wait",
            "log",
            "report",
            "evidence",
            "cleanup",
            "format",
            "validate",
            "parse",
            "convert",
        ]

        # Verificar si la función contiene palabras clave relevantes
        for keyword in relevant_keywords:
            if keyword in function_lower and keyword in utility_lower:
                return True

        return False

    def generate_reuse_report(
        self, step_text, functionality, element_type, utility_type
    ):
        """
        Genera un reporte completo de código reutilizable

        Args:
            step_text (str): Texto del step
            functionality (str): Funcionalidad necesaria
            element_type (str): Tipo de elemento
            utility_type (str): Tipo de utilidad

        Returns:
            dict: Reporte completo de reutilización
        """
        reuse_report = {
            "similar_steps": self.find_similar_steps(step_text),
            "reusable_pages": self.find_reusable_page_objects(functionality),
            "reusable_locators": self.find_reusable_locators(element_type),
            "reusable_utilities": self.find_reusable_utilities(utility_type),
        }

        return reuse_report

    def analyze_code_patterns(self) -> Dict[str, List[str]]:
        """
        Analiza patrones de código en el proyecto para identificar reutilización

        Returns:
            Dict con patrones encontrados por categoría
        """
        patterns = {
            "common_steps": [],
            "common_methods": [],
            "common_locators": [],
            "common_utilities": [],
        }

        try:
            # Analizar steps comunes
            patterns["common_steps"] = self._analyze_step_patterns()

            # Analizar métodos comunes
            patterns["common_methods"] = self._analyze_method_patterns()

            # Analizar locators comunes
            patterns["common_locators"] = self._analyze_locator_patterns()

            # Analizar utilidades comunes
            patterns["common_utilities"] = self._analyze_utility_patterns()

            self.logger.info(
                f"Análisis de patrones completado: {len(patterns)} categorías"
            )

        except Exception as e:
            self.logger.error(f"Error analizando patrones: {e}")

        return patterns

    def suggest_code_reuse(self, new_requirement: str) -> Dict[str, any]:
        """
        Sugiere código reutilizable basado en un nuevo requerimiento

        Args:
            new_requirement: Descripción del nuevo requerimiento

        Returns:
            Dict con sugerencias de reutilización
        """
        suggestions = {
            "requirement": new_requirement,
            "timestamp": datetime.now().isoformat(),
            "reusable_steps": [],
            "reusable_pages": [],
            "reusable_locators": [],
            "reusable_utilities": [],
            "recommendations": [],
        }

        try:
            # Extraer palabras clave del requerimiento
            keywords = self._extract_keywords(new_requirement)

            # Buscar código relacionado
            for keyword in keywords:
                # Buscar steps similares
                similar_steps = self.find_similar_steps(keyword)
                suggestions["reusable_steps"].extend(similar_steps[:3])  # Top 3

                # Buscar page objects
                reusable_pages = self.find_reusable_page_objects(keyword)
                suggestions["reusable_pages"].extend(reusable_pages[:3])

                # Buscar locators
                reusable_locators = self.find_reusable_locators(keyword)
                suggestions["reusable_locators"].extend(reusable_locators[:3])

                # Buscar utilidades
                reusable_utilities = self.find_reusable_utilities(keyword)
                suggestions["reusable_utilities"].extend(reusable_utilities[:3])

            # Generar recomendaciones
            suggestions["recommendations"] = self._generate_recommendations(suggestions)

            self.logger.info(f"Sugerencias generadas para: {new_requirement}")

        except Exception as e:
            self.logger.error(f"Error generando sugerencias: {e}")

        return suggestions

    def create_reuse_template(self, functionality: str) -> str:
        """
        Crea un template de código reutilizable para una funcionalidad específica

        Args:
            functionality: Nombre de la funcionalidad

        Returns:
            String con el template generado
        """
        template = f"""
# Template generado para: {functionality}
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class {functionality.title().replace(' ', '')}Page(BasePage):
    \"\"\"Page Object para {functionality}\"\"\"

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {functionality.title().replace(' ', '')}Locators()

    def navigate_to_{functionality.lower().replace(' ', '_')}(self):
        \"\"\"Navegar a la página de {functionality}\"\"\"
        # Implementar navegación
        pass

    def perform_{functionality.lower().replace(' ', '_')}_action(self):
        \"\"\"Realizar acción principal de {functionality}\"\"\"
        # Implementar acción principal
        pass

class {functionality.title().replace(' ', '')}Locators:
    \"\"\"Locators para {functionality}\"\"\"

    # Agregar locators específicos aquí
    pass

# Steps para Behave
@given('que estoy en la página de {functionality.lower()}')
def step_navigate_to_{functionality.lower().replace(' ', '_')}(context):
    \"\"\"Step para navegar a {functionality}\"\"\"
    context.{functionality.lower().replace(' ', '_')}_page = {functionality.title().replace(' ', '')}Page(context.driver)
    context.{functionality.lower().replace(' ', '_')}_page.navigate_to_{functionality.lower().replace(' ', '_')}()

@when('realizo la acción de {functionality.lower()}')
def step_perform_{functionality.lower().replace(' ', '_')}_action(context):
    \"\"\"Step para realizar acción de {functionality}\"\"\"
    context.{functionality.lower().replace(' ', '_')}_page.perform_{functionality.lower().replace(' ', '_')}_action()

@then('debería ver el resultado de {functionality.lower()}')
def step_verify_{functionality.lower().replace(' ', '_')}_result(context):
    \"\"\"Step para verificar resultado de {functionality}\"\"\"
    # Implementar verificación
    pass
"""
        return template

    def validate_code_consistency(self) -> Dict[str, List[str]]:
        """
        Valida la consistencia del código en el proyecto

        Returns:
            Dict con inconsistencias encontradas
        """
        inconsistencies = {
            "naming_conventions": [],
            "missing_docstrings": [],
            "duplicate_code": [],
            "unused_imports": [],
        }

        try:
            # Validar convenciones de nombres
            inconsistencies["naming_conventions"] = self._check_naming_conventions()

            # Validar docstrings faltantes
            inconsistencies["missing_docstrings"] = self._check_missing_docstrings()

            # Validar código duplicado
            inconsistencies["duplicate_code"] = self._check_duplicate_code()

            # Validar imports no utilizados
            inconsistencies["unused_imports"] = self._check_unused_imports()

            self.logger.info(f"Validación de consistencia completada")

        except Exception as e:
            self.logger.error(f"Error validando consistencia: {e}")

        return inconsistencies

    def generate_reuse_documentation(self) -> str:
        """
        Genera documentación de código reutilizable

        Returns:
            String con la documentación generada
        """
        doc = f"""
# 📚 Documentación de Código Reutilizable
# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 Objetivo
Este documento identifica código reutilizable en el proyecto de automatización de Zucarmex.

## 📋 Código Disponible para Reutilización

### 🔧 Page Objects Reutilizables
"""

        try:
            # Analizar page objects
            page_files = (
                list(self.pages_dir.glob("*_page.py"))
                if self.pages_dir.exists()
                else []
            )

            for page_file in page_files:
                doc += f"\n#### {page_file.stem}\n"
                doc += f"- **Archivo**: `{page_file}`\n"
                doc += f"- **Métodos disponibles**: Ver archivo para detalles\n"

            doc += "\n### 🎯 Locators Reutilizables\n"

            # Analizar locators
            locator_files = (
                list(self.locators_dir.glob("*_locators.py"))
                if self.locators_dir.exists()
                else []
            )

            for locator_file in locator_files:
                doc += f"\n#### {locator_file.stem}\n"
                doc += f"- **Archivo**: `{locator_file}`\n"
                doc += f"- **Elementos disponibles**: Ver archivo para detalles\n"

            doc += "\n### 🛠️ Utilidades Reutilizables\n"

            # Analizar utilidades
            utility_files = (
                list(self.utils_dir.glob("*.py")) if self.utils_dir.exists() else []
            )

            for utility_file in utility_files:
                if utility_file.name != "__init__.py":
                    doc += f"\n#### {utility_file.stem}\n"
                    doc += f"- **Archivo**: `{utility_file}`\n"
                    doc += f"- **Funciones disponibles**: Ver archivo para detalles\n"

            doc += f"""
## 📝 Cómo Usar Este Código

### 1. Antes de Crear Código Nuevo
1. Revisar esta documentación
2. Buscar funcionalidades similares
3. Evaluar si se puede reutilizar código existente

### 2. Reutilización de Page Objects
```python
from pages.{page_files[0].stem if page_files else 'ejemplo'}_page import {page_files[0].stem.replace('_page', 'Page').title() if page_files else 'EjemploPage'}

# Usar en tus tests
page = {page_files[0].stem.replace('_page', 'Page').title() if page_files else 'EjemploPage'}(driver)
```

### 3. Reutilización de Locators
```python
from locators.{locator_files[0].stem if locator_files else 'ejemplo'}_locators import {locator_files[0].stem.replace('_locators', 'Locators').title() if locator_files else 'EjemploLocators'}

# Usar en tus page objects
locators = {locator_files[0].stem.replace('_locators', 'Locators').title() if locator_files else 'EjemploLocators'}()
```

### 4. Reutilización de Utilidades
```python
from utils.{utility_files[0].stem if utility_files else 'ejemplo'} import {utility_files[0].stem if utility_files else 'funcion_ejemplo'}

# Usar en tus tests
result = {utility_files[0].stem if utility_files else 'funcion_ejemplo'}()
```

## 🔄 Mantenimiento
- Actualizar esta documentación cuando se agregue nuevo código reutilizable
- Revisar periódicamente para identificar nuevas oportunidades de reutilización
- Mantener consistencia en naming conventions

---
*Documentación generada automáticamente por el Sistema de Automatización Zucarmex*
"""

        except Exception as e:
            self.logger.error(f"Error generando documentación: {e}")
            doc += f"\nError generando documentación: {e}"

        return doc

    def _analyze_step_patterns(self) -> List[str]:
        """Analiza patrones comunes en steps"""
        patterns = []
        try:
            if self.features_dir.exists():
                steps_files = list(self.features_dir.rglob("*_steps.py"))
                for steps_file in steps_files:
                    with open(steps_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Buscar patrones comunes
                    step_patterns = re.findall(
                        r'@(given|when|then)\s*\(\s*["\']([^"\']+)["\']', content
                    )
                    for step_type, step_content in step_patterns:
                        if (
                            len(step_content.split()) >= 3
                        ):  # Steps con al menos 3 palabras
                            patterns.append(f"{step_type}: {step_content}")
        except Exception as e:
            self.logger.error(f"Error analizando patrones de steps: {e}")
        return patterns[:10]  # Top 10

    def _analyze_method_patterns(self) -> List[str]:
        """Analiza patrones comunes en métodos"""
        patterns = []
        try:
            if self.pages_dir.exists():
                page_files = list(self.pages_dir.glob("*_page.py"))
                for page_file in page_files:
                    with open(page_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Buscar métodos comunes
                    method_patterns = re.findall(r"def\s+(\w+)\s*\(", content)
                    for method in method_patterns:
                        if len(method) > 3:  # Métodos con nombres significativos
                            patterns.append(f"{page_file.stem}: {method}")
        except Exception as e:
            self.logger.error(f"Error analizando patrones de métodos: {e}")
        return patterns[:10]  # Top 10

    def _analyze_locator_patterns(self) -> List[str]:
        """Analiza patrones comunes en locators"""
        patterns = []
        try:
            if self.locators_dir.exists():
                locator_files = list(self.locators_dir.glob("*_locators.py"))
                for locator_file in locator_files:
                    with open(locator_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Buscar locators comunes
                    locator_patterns = re.findall(
                        r'(\w+)\s*=\s*["\']([^"\']+)["\']', content
                    )
                    for locator_name, locator_value in locator_patterns:
                        if len(locator_name) > 3:  # Locators con nombres significativos
                            patterns.append(f"{locator_file.stem}: {locator_name}")
        except Exception as e:
            self.logger.error(f"Error analizando patrones de locators: {e}")
        return patterns[:10]  # Top 10

    def _analyze_utility_patterns(self) -> List[str]:
        """Analiza patrones comunes en utilidades"""
        patterns = []
        try:
            if self.utils_dir.exists():
                utility_files = list(self.utils_dir.glob("*.py"))
                for utility_file in utility_files:
                    if utility_file.name != "__init__.py":
                        with open(utility_file, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Buscar funciones comunes
                        function_patterns = re.findall(r"def\s+(\w+)\s*\(", content)
                        for function in function_patterns:
                            if (
                                len(function) > 3
                            ):  # Funciones con nombres significativos
                                patterns.append(f"{utility_file.stem}: {function}")
        except Exception as e:
            self.logger.error(f"Error analizando patrones de utilidades: {e}")
        return patterns[:10]  # Top 10

    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave de un texto"""
        # Palabras comunes a ignorar
        stop_words = {
            "el",
            "la",
            "de",
            "que",
            "y",
            "a",
            "en",
            "un",
            "es",
            "se",
            "no",
            "te",
            "lo",
            "le",
            "da",
            "su",
            "por",
            "son",
            "con",
            "para",
            "al",
            "del",
            "los",
            "las",
            "una",
            "como",
            "pero",
            "sus",
            "más",
            "muy",
            "ya",
            "todo",
            "esta",
            "está",
            "están",
            "estas",
            "estos",
            "puede",
            "pueden",
            "ser",
            "hacer",
            "tener",
            "ver",
            "saber",
            "decir",
            "ir",
            "venir",
            "dar",
            "tomar",
            "poner",
            "salir",
            "entrar",
            "buscar",
            "encontrar",
            "crear",
            "eliminar",
            "modificar",
            "actualizar",
            "guardar",
            "cargar",
            "navegar",
            "hacer",
            "clic",
            "escribir",
            "seleccionar",
            "verificar",
            "validar",
            "confirmar",
            "cancelar",
            "aceptar",
            "rechazar",
        }

        # Extraer palabras
        words = re.findall(r"\b\w+\b", text.lower())

        # Filtrar palabras comunes y mantener solo las significativas
        keywords = [word for word in words if word not in stop_words and len(word) > 2]

        return list(set(keywords))  # Remover duplicados

    def _generate_recommendations(self, suggestions: Dict) -> List[str]:
        """Genera recomendaciones basadas en las sugerencias"""
        recommendations = []

        if suggestions["reusable_steps"]:
            recommendations.append(
                "✅ Se encontraron steps similares que puedes reutilizar"
            )

        if suggestions["reusable_pages"]:
            recommendations.append("✅ Se encontraron Page Objects que puedes extender")

        if suggestions["reusable_locators"]:
            recommendations.append("✅ Se encontraron Locators que puedes reutilizar")

        if suggestions["reusable_utilities"]:
            recommendations.append("✅ Se encontraron Utilidades que puedes usar")

        if not any(
            [
                suggestions["reusable_steps"],
                suggestions["reusable_pages"],
                suggestions["reusable_locators"],
                suggestions["reusable_utilities"],
            ]
        ):
            recommendations.append(
                "⚠️ No se encontró código reutilizable. Considera crear nuevo código siguiendo los patrones existentes."
            )

        return recommendations

    def _check_naming_conventions(self) -> List[str]:
        """Verifica convenciones de nombres"""
        issues = []
        try:
            # Verificar archivos de pages
            if self.pages_dir.exists():
                page_files = list(self.pages_dir.glob("*.py"))
                for page_file in page_files:
                    if (
                        not page_file.name.endswith("_page.py")
                        and page_file.name != "__init__.py"
                    ):
                        issues.append(
                            f"Page file should end with '_page.py': {page_file}"
                        )

            # Verificar archivos de locators
            if self.locators_dir.exists():
                locator_files = list(self.locators_dir.glob("*.py"))
                for locator_file in locator_files:
                    if (
                        not locator_file.name.endswith("_locators.py")
                        and locator_file.name != "__init__.py"
                    ):
                        issues.append(
                            f"Locator file should end with '_locators.py': {locator_file}"
                        )

            # Verificar archivos de steps
            if self.features_dir.exists():
                steps_files = list(self.features_dir.rglob("*_steps.py"))
                for steps_file in steps_files:
                    if not steps_file.name.endswith("_steps.py"):
                        issues.append(
                            f"Steps file should end with '_steps.py': {steps_file}"
                        )

        except Exception as e:
            self.logger.error(f"Error verificando convenciones de nombres: {e}")

        return issues

    def _check_missing_docstrings(self) -> List[str]:
        """Verifica docstrings faltantes"""
        issues = []
        try:
            # Verificar en pages
            if self.pages_dir.exists():
                page_files = list(self.pages_dir.glob("*_page.py"))
                for page_file in page_files:
                    with open(page_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Buscar clases sin docstring
                    class_pattern = r"class\s+(\w+).*?:"
                    classes = re.findall(class_pattern, content)
                    for class_name in classes:
                        if (
                            f"class {class_name}" in content
                            and f'"""{class_name}' not in content
                        ):
                            issues.append(
                                f"Missing docstring for class {class_name} in {page_file}"
                            )

        except Exception as e:
            self.logger.error(f"Error verificando docstrings: {e}")

        return issues

    def _check_duplicate_code(self) -> List[str]:
        """Verifica código duplicado"""
        issues = []
        # Implementación básica - se puede expandir
        return issues

    def _check_unused_imports(self) -> List[str]:
        """Verifica imports no utilizados"""
        issues = []
        # Implementación básica - se puede expandir
        return issues


# Función de conveniencia para usar el helper
def find_reusable_code(
    step_text="", functionality="", element_type="", utility_type=""
):
    """
    Función de conveniencia para encontrar código reutilizable

    Args:
        step_text (str): Texto del step a buscar
        functionality (str): Funcionalidad necesaria
        element_type (str): Tipo de elemento
        utility_type (str): Tipo de utilidad

    Returns:
        dict: Reporte de código reutilizable
    """
    helper = CodeReuseHelper()
    return helper.generate_reuse_report(
        step_text, functionality, element_type, utility_type
    )


if __name__ == "__main__":
    # Ejemplo de uso
    code_helper = CodeReuseHelper()

    # Buscar código reutilizable para login
    example_report = code_helper.generate_reuse_report(
        step_text="estoy en la página de inicio de sesión",
        functionality="login",
        element_type="button",
        utility_type="screenshot",
    )

    print("Reporte de código reutilizable:")
    print(f"Steps similares: {len(example_report['similar_steps'])}")
    print(f"Page Objects reutilizables: {len(example_report['reusable_pages'])}")
    print(f"Locators reutilizables: {len(example_report['reusable_locators'])}")
    print(f"Utilidades reutilizables: {len(example_report['reusable_utilities'])}")
