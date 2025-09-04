"""
Sistema de Validación Automática de Elementos Web
Verifica que los elementos existan antes de ejecutar pruebas para evitar fallos
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ElementValidationError(Exception):
    """Excepción personalizada para errores de validación de elementos"""

    pass


class ElementValidator:
    """Sistema avanzado de validación de elementos web"""

    def __init__(self, driver: webdriver.Chrome, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.validation_results = {}

    def validate_page_elements(
        self, locators: Dict[str, Tuple[str, str]], page_name: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Valida que todos los elementos de una página existan

        Args:
            locators: Diccionario con nombre y locator (tipo, valor)
            page_name: Nombre de la página para logging

        Returns:
            Diccionario con resultados de validación
        """
        self.logger.info(f"🔍 Validando elementos de la página: {page_name}")

        validation_result = {
            "page_name": page_name,
            "timestamp": datetime.now().isoformat(),
            "total_elements": len(locators),
            "valid_elements": 0,
            "invalid_elements": 0,
            "missing_elements": [],
            "valid_elements_list": [],
            "validation_status": "PENDING",
        }

        for element_name, (locator_type, locator_value) in locators.items():
            try:
                is_valid = self._validate_single_element(
                    locator_type, locator_value, element_name
                )

                if is_valid:
                    validation_result["valid_elements"] += 1
                    validation_result["valid_elements_list"].append(element_name)
                    self.logger.info(f"✅ {element_name}: Válido")
                else:
                    validation_result["invalid_elements"] += 1
                    validation_result["missing_elements"].append(
                        {
                            "name": element_name,
                            "locator_type": locator_type,
                            "locator_value": locator_value,
                            "reason": "Element not found or not interactable",
                        }
                    )
                    self.logger.warning(f"❌ {element_name}: No encontrado")

            except Exception as e:
                validation_result["invalid_elements"] += 1
                validation_result["missing_elements"].append(
                    {
                        "name": element_name,
                        "locator_type": locator_type,
                        "locator_value": locator_value,
                        "reason": str(e),
                    }
                )
                self.logger.error(f"❌ {element_name}: Error - {str(e)}")

        # Determinar estado final
        if validation_result["invalid_elements"] == 0:
            validation_result["validation_status"] = "SUCCESS"
            self.logger.info(
                f"✅ Validación exitosa: {page_name} - Todos los elementos válidos"
            )
        else:
            validation_result["validation_status"] = "FAILED"
            self.logger.warning(
                f"⚠️ Validación fallida: {page_name} - {validation_result['invalid_elements']} elementos faltantes"
            )

        self.validation_results[page_name] = validation_result
        return validation_result

    def _validate_single_element(
        self, locator_type: str, locator_value: str, element_name: str
    ) -> bool:
        """
        Valida un elemento individual

        Args:
            locator_type: Tipo de locator (id, xpath, css, etc.)
            locator_value: Valor del locator
            element_name: Nombre del elemento

        Returns:
            True si el elemento es válido, False en caso contrario
        """
        try:
            # Convertir string a By enum
            by_type = self._get_by_type(locator_type)

            # Esperar a que el elemento esté presente
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by_type, locator_value))
            )

            # Verificar que el elemento sea interactuable
            if element.is_displayed() and element.is_enabled():
                return True
            else:
                self.logger.warning(f"Elemento {element_name} no es interactuable")
                return False

        except TimeoutException:
            self.logger.warning(f"Timeout esperando elemento {element_name}")
            return False
        except NoSuchElementException:
            self.logger.warning(f"Elemento {element_name} no encontrado")
            return False
        except Exception as e:
            self.logger.error(f"Error validando elemento {element_name}: {str(e)}")
            return False

    def _get_by_type(self, locator_type: str) -> By:
        """Convierte string de tipo de locator a By enum"""
        locator_map = {
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
        }

        locator_type_lower = locator_type.lower()
        if locator_type_lower in locator_map:
            return locator_map[locator_type_lower]
        else:
            raise ValueError(f"Tipo de locator no válido: {locator_type}")

    def validate_feature_elements(self, feature_name: str) -> Dict[str, Any]:
        """
        Valida todos los elementos de un feature completo

        Args:
            feature_name: Nombre del feature

        Returns:
            Diccionario con resultados de validación del feature
        """
        self.logger.info(f"🔍 Validando elementos del feature: {feature_name}")

        feature_result = {
            "feature_name": feature_name,
            "timestamp": datetime.now().isoformat(),
            "pages_validated": 0,
            "total_elements": 0,
            "valid_elements": 0,
            "invalid_elements": 0,
            "page_results": {},
            "overall_status": "PENDING",
        }

        try:
            # Buscar archivos de locators del feature
            locator_files = self._find_locator_files(feature_name)

            for locator_file in locator_files:
                page_name = locator_file.stem.replace("_locators", "")
                locators = self._load_locators_from_file(locator_file)

                if locators:
                    page_result = self.validate_page_elements(locators, page_name)
                    feature_result["page_results"][page_name] = page_result
                    feature_result["pages_validated"] += 1
                    feature_result["total_elements"] += page_result["total_elements"]
                    feature_result["valid_elements"] += page_result["valid_elements"]
                    feature_result["invalid_elements"] += page_result[
                        "invalid_elements"
                    ]

            # Determinar estado general
            if feature_result["invalid_elements"] == 0:
                feature_result["overall_status"] = "SUCCESS"
                self.logger.info(f"✅ Feature {feature_name} validado exitosamente")
            else:
                feature_result["overall_status"] = "FAILED"
                self.logger.warning(
                    f"⚠️ Feature {feature_name} tiene {feature_result['invalid_elements']} elementos inválidos"
                )

        except Exception as e:
            feature_result["overall_status"] = "ERROR"
            feature_result["error"] = str(e)
            self.logger.error(f"❌ Error validando feature {feature_name}: {str(e)}")

        return feature_result

    def _find_locator_files(self, feature_name: str) -> List[Path]:
        """Encuentra archivos de locators relacionados con un feature"""
        locators_dir = Path("locators")
        if not locators_dir.exists():
            return []

        # Buscar archivos que contengan el nombre del feature
        locator_files = []
        for locator_file in locators_dir.glob("*_locators.py"):
            if feature_name.lower() in locator_file.name.lower():
                locator_files.append(locator_file)

        return locator_files

    def _load_locators_from_file(
        self, locator_file: Path
    ) -> Dict[str, Tuple[str, str]]:
        """
        Carga locators desde un archivo Python

        Args:
            locator_file: Archivo de locators

        Returns:
            Diccionario con locators
        """
        locators = {}

        try:
            with open(locator_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Buscar patrones de locators (simplificado)
            # Patrón: VARIABLE = (By.TIPO, "valor")
            pattern = r'(\w+)\s*=\s*\(By\.(\w+),\s*["\']([^"\']+)["\']\)'
            matches = re.findall(pattern, content)

            for var_name, by_type, locator_value in matches:
                locators[var_name] = (by_type.lower(), locator_value)

            self.logger.info(f"Cargados {len(locators)} locators desde {locator_file}")

        except Exception as e:
            self.logger.error(f"Error cargando locators desde {locator_file}: {str(e)}")

        return locators

    def generate_validation_report(self, output_file: Optional[str] = None) -> str:
        """
        Genera un reporte de validación en formato HTML

        Args:
            output_file: Archivo de salida (opcional)

        Returns:
            Contenido del reporte HTML
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Validación de Elementos - {timestamp}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: white;
        }}
        .success {{ background: #4CAF50; }}
        .warning {{ background: #FF9800; }}
        .error {{ background: #f44336; }}
        .info {{ background: #2196F3; }}
        .page-section {{
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .page-header {{
            background: #f8f9fa;
            padding: 15px;
            font-weight: bold;
            border-bottom: 1px solid #ddd;
        }}
        .element-list {{
            padding: 15px;
        }}
        .element-item {{
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .element-valid {{ background: #e8f5e8; color: #2e7d32; }}
        .element-invalid {{ background: #ffebee; color: #c62828; }}
        .status-badge {{
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }}
        .status-success {{ background: #4CAF50; color: white; }}
        .status-failed {{ background: #f44336; color: white; }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Reporte de Validación de Elementos</h1>
            <p>Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="summary">
            <div class="summary-card info">
                <h3>Páginas Validadas</h3>
                <h2>{len(self.validation_results)}</h2>
            </div>
            <div class="summary-card success">
                <h3>Elementos Válidos</h3>
                <h2>{sum(r.get('valid_elements', 0) for r in self.validation_results.values())}</h2>
            </div>
            <div class="summary-card warning">
                <h3>Elementos Inválidos</h3>
                <h2>{sum(r.get('invalid_elements', 0) for r in self.validation_results.values())}</h2>
            </div>
            <div class="summary-card info">
                <h3>Total Elementos</h3>
                <h2>{sum(r.get('total_elements', 0) for r in self.validation_results.values())}</h2>
            </div>
        </div>
"""

        # Agregar resultados por página
        for page_name, result in self.validation_results.items():
            status_badge = (
                "status-success"
                if result["validation_status"] == "SUCCESS"
                else "status-failed"
            )

            html_content += f"""
        <div class="page-section">
            <div class="page-header">
                📄 {page_name}
                <span class="status-badge {status_badge}">{result['validation_status']}</span>
            </div>
            <div class="element-list">
                <p><strong>Total:</strong> {result['total_elements']} |
                   <strong>Válidos:</strong> {result['valid_elements']} |
                   <strong>Inválidos:</strong> {result['invalid_elements']}</p>

                <h4>✅ Elementos Válidos:</h4>
"""

            for element_name in result.get("valid_elements_list", []):
                html_content += (
                    f'<div class="element-item element-valid">✅ '
                    f"{element_name}</div>"
                )

            if result.get("missing_elements"):
                html_content += "<h4>❌ Elementos Inválidos:</h4>"
                for element in result["missing_elements"]:
                    html_content += f"""
                    <div class="element-item element-invalid">
                        ❌ {element['name']}
                        <small>({element['locator_type']}: {element['locator_value']})</small>
                        <br><small>Razón: {element['reason']}</small>
                    </div>
                    """

            html_content += "</div></div>"

        html_content += f"""
        <div class="footer">
            <p>Reporte generado automáticamente por el Sistema de Validación de Elementos</p>
            <p>Zucarmex - Sistema de Automatización de Pruebas</p>
        </div>
    </div>
</body>
</html>
"""

        # Guardar archivo si se especifica
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            self.logger.info(f"Reporte de validación guardado: {output_path}")

        return html_content

    def save_validation_results(self, output_file: str):
        """
        Guarda los resultados de validación en formato JSON

        Args:
            output_file: Archivo de salida
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        results_data = {
            "validation_timestamp": datetime.now().isoformat(),
            "total_pages": len(self.validation_results),
            "total_elements": sum(
                r.get("total_elements", 0) for r in self.validation_results.values()
            ),
            "valid_elements": sum(
                r.get("valid_elements", 0) for r in self.validation_results.values()
            ),
            "invalid_elements": sum(
                r.get("invalid_elements", 0) for r in self.validation_results.values()
            ),
            "page_results": self.validation_results,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Resultados de validación guardados: {output_path}")

    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen de los resultados de validación

        Returns:
            Diccionario con resumen
        """
        total_pages = len(self.validation_results)
        total_elements = sum(
            r.get("total_elements", 0) for r in self.validation_results.values()
        )
        valid_elements = sum(
            r.get("valid_elements", 0) for r in self.validation_results.values()
        )
        invalid_elements = sum(
            r.get("invalid_elements", 0) for r in self.validation_results.values()
        )

        success_rate = (
            (valid_elements / total_elements * 100) if total_elements > 0 else 0
        )

        return {
            "total_pages": total_pages,
            "total_elements": total_elements,
            "valid_elements": valid_elements,
            "invalid_elements": invalid_elements,
            "success_rate": round(success_rate, 2),
            "validation_status": "SUCCESS" if invalid_elements == 0 else "FAILED",
            "timestamp": datetime.now().isoformat(),
        }


# Funciones de conveniencia
def validate_all_elements(
    driver: webdriver.Chrome, feature_name: str = None
) -> ElementValidator:
    """
    Valida todos los elementos de un feature o todos los features

    Args:
        driver: Instancia del WebDriver
        feature_name: Nombre del feature específico (opcional)

    Returns:
        Instancia de ElementValidator con resultados
    """
    validator = ElementValidator(driver)

    if feature_name:
        validator.validate_feature_elements(feature_name)
    else:
        # Validar todos los features
        locators_dir = Path("locators")
        if locators_dir.exists():
            for locator_file in locators_dir.glob("*_locators.py"):
                feature_name = locator_file.stem.replace("_locators", "")
                validator.validate_feature_elements(feature_name)

    return validator


def check_elements_before_execution(
    driver: webdriver.Chrome, feature_name: str
) -> bool:
    """
    Verifica elementos antes de ejecutar una prueba

    Args:
        driver: Instancia del WebDriver
        feature_name: Nombre del feature a validar

    Returns:
        True si todos los elementos son válidos, False en caso contrario
    """
    validator = ElementValidator(driver)
    result = validator.validate_feature_elements(feature_name)

    return result["overall_status"] == "SUCCESS"
