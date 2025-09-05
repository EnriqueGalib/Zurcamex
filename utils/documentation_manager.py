"""
Gestor de Documentación - Organización por Carpetas y Análisis de Fallos
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path

from .pdf_generator import PDFGenerator


class DocumentationManager:
    """Gestor de documentación con organización por carpetas y análisis de fallos"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.docs_dir = Path("docs")
        self.docs_dir.mkdir(exist_ok=True)

        # Inicializar generador de PDFs
        self.pdf_generator = PDFGenerator()

        # Crear estructura de documentación
        self._create_docs_structure()

    def _create_docs_structure(self):
        """Crea la estructura de carpetas para documentación"""
        try:
            # Carpetas principales
            self.success_docs_dir = self.docs_dir / "EXITOSOS"
            self.failed_docs_dir = self.docs_dir / "FALLIDOS"
            self.partial_docs_dir = self.docs_dir / "PARCIALES"
            self.unknown_docs_dir = self.docs_dir / "DESCONOCIDOS"

            # Crear directorios
            for doc_dir in [
                self.success_docs_dir,
                self.failed_docs_dir,
                self.partial_docs_dir,
                self.unknown_docs_dir,
            ]:
                doc_dir.mkdir(exist_ok=True)

            self.logger.info("Estructura de documentación creada")

        except Exception as e:
            self.logger.error(f"Error creando estructura de documentación: {str(e)}")

    def generate_execution_documentation(self, execution_data, log_file_path=None):
        """Genera documentación específica según el resultado de la ejecución"""
        try:
            overall_status = execution_data.get("execution_info", {}).get(
                "overall_status", "UNKNOWN"
            )

            # Determinar directorio de destino
            if overall_status == "SUCCESS":
                target_dir = self.success_docs_dir
                doc_type = "EXITOSO"
            elif overall_status == "FAILED":
                target_dir = self.failed_docs_dir
                doc_type = "FALLIDO"
            elif overall_status == "PARTIAL":
                target_dir = self.partial_docs_dir
                doc_type = "PARCIAL"
            else:
                target_dir = self.unknown_docs_dir
                doc_type = "DESCONOCIDO"

            # Generar documentación Markdown
            if overall_status == "FAILED":
                # Para fallos, generar análisis detallado
                doc_path = self._generate_failure_analysis(
                    execution_data, target_dir, log_file_path
                )
            else:
                # Para exitosos, generar documentación estándar
                doc_path = self._generate_success_documentation(
                    execution_data, target_dir
                )

            # Generar documento PDF para el cliente
            pdf_path, _ = self.pdf_generator.generate_execution_pdf(
                execution_data, log_file_path
            )

            self.logger.info(f"Documentación {doc_type} generada: {doc_path}")
            if pdf_path:
                self.logger.info(f"Documento PDF generado: {pdf_path}")

            return doc_path, pdf_path

        except Exception as e:
            self.logger.error(f"Error generando documentación: {str(e)}")
            return None, None

    def _generate_success_documentation(self, execution_data, target_dir):
        """Genera documentación para ejecuciones exitosas"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = execution_data.get("execution_info", {}).get(
                "test_name", "test"
            )
            safe_name = re.sub(r"[^\w\s-]", "", test_name).strip()
            safe_name = re.sub(r"[-\s]+", "_", safe_name)

            doc_filename = f"SUCCESS_{safe_name}_{timestamp}.md"
            doc_path = target_dir / doc_filename

            # Crear contenido de documentación exitosa
            content = self._create_success_content(execution_data)

            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(content)

            return str(doc_path)

        except Exception as e:
            self.logger.error(f"Error generando documentación exitosa: {str(e)}")
            return None

    def _generate_failure_analysis(self, execution_data, target_dir, log_file_path):
        """Genera análisis detallado para ejecuciones fallidas"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = execution_data.get("execution_info", {}).get(
                "test_name", "test"
            )
            safe_name = re.sub(r"[^\w\s-]", "", test_name).strip()
            safe_name = re.sub(r"[-\s]+", "_", safe_name)

            doc_filename = f"FAILURE_ANALYSIS_{safe_name}_{timestamp}.md"
            doc_path = target_dir / doc_filename

            # Crear contenido de análisis de fallo
            content = self._create_failure_analysis_content(
                execution_data, log_file_path
            )

            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(content)

            return str(doc_path)

        except Exception as e:
            self.logger.error(f"Error generando análisis de fallo: {str(e)}")
            return None

    def _create_success_content(self, execution_data):
        """Crea el contenido para documentación exitosa"""
        exec_info = execution_data.get("execution_info", {})
        summary = execution_data.get("summary", {})
        steps = execution_data.get("steps", [])

        content = f"""# Ejecución Exitosa - {exec_info.get('test_name', 'Test')}

## Información General

- **Fecha**: {exec_info.get('execution_date', 'N/A')}
- **Hora de Inicio**: {exec_info.get('start_time', 'N/A')}
- **Duración Total**: {exec_info.get('total_duration', 'N/A')}
- **Tipo de Ejecución**: {exec_info.get('execution_type', 'N/A')}
- **Directorio de Evidencias**: `{exec_info.get('evidence_directory', 'N/A')}`
- **Log de Ejecución**: `{exec_info.get('log_file', 'N/A')}`

## Resumen de Resultados

- **Total de Pasos**: {summary.get('total_steps', 0)}
- **Pasos Exitosos**: {summary.get('successful_steps', 0)}
- **Pasos Fallidos**: {summary.get('failed_steps', 0)}
- **Screenshots Tomados**: {summary.get('screenshots_taken', 0)}

## Pasos Ejecutados

"""

        for i, step in enumerate(steps, 1):
            status_text = (
                "SUCCESS"
                if step.get("status") == "SUCCESS"
                else "FAILED" if step.get("status") == "FAILED" else "WARNING"
            )
            content += f"""### {i}. {status_text} {step.get('name', 'Paso sin nombre')}

- **Descripción**: {step.get('description', 'Sin descripción')}
- **Duración**: {step.get('duration', 'No disponible')}
- **Timestamp**: {step.get('timestamp', 'No disponible')}

"""

            # Agregar evidencias si existen
            evidence = step.get("evidence", [])
            if evidence:
                content += "**Evidencias:**\n"
                for ev in evidence:
                    content += f"- [{ev.get('name', 'Evidencia')}]({ev.get('path', '#')}) ({ev.get('timestamp', 'Sin timestamp')})\n"
                content += "\n"

        content += f"""## Conclusión

Esta ejecución se completó **exitosamente** con {summary.get('successful_steps', 0)} de {summary.get('total_steps', 0)} pasos ejecutados correctamente.

### Archivos Generados

- **Reporte HTML**: `reports/execution_report_*.html`
- **Reporte JSON**: `reports/execution_report_*.json`
- **Screenshots**: `{exec_info.get('evidence_directory', 'N/A')}/screenshots/`

---
*Documento generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        return content

    def _create_failure_analysis_content(self, execution_data, log_file_path):
        """Crea el contenido para análisis de fallo"""
        exec_info = execution_data.get("execution_info", {})
        summary = execution_data.get("summary", {})
        steps = execution_data.get("steps", [])

        # Analizar el log si está disponible
        log_analysis = self._analyze_log_file(log_file_path) if log_file_path else {}

        content = f"""# Análisis de Fallo - {exec_info.get('test_name', 'Test')}

## Resumen del Fallo

- **Fecha**: {exec_info.get('execution_date', 'N/A')}
- **Hora de Inicio**: {exec_info.get('start_time', 'N/A')}
- **Duración Total**: {exec_info.get('total_duration', 'N/A')}
- **Tipo de Ejecución**: {exec_info.get('execution_type', 'N/A')}
- **Directorio de Evidencias**: `{exec_info.get('evidence_directory', 'N/A')}`
- **Log de Ejecución**: `{exec_info.get('log_file', 'N/A')}`

## Estadísticas del Fallo

- **Total de Pasos**: {summary.get('total_steps', 0)}
- **Pasos Exitosos**: {summary.get('successful_steps', 0)}
- **Pasos Fallidos**: {summary.get('failed_steps', 0)}
- **Screenshots Tomados**: {summary.get('screenshots_taken', 0)}

## Análisis del Log

"""

        if log_analysis:
            content += f"""### Información del Log

- **Archivo**: `{log_analysis.get('file_path', 'N/A')}`
- **Tamaño**: {log_analysis.get('file_size', 'N/A')} bytes
- **Última Modificación**: {log_analysis.get('last_modified', 'N/A')}

### Errores Encontrados

"""

            errors = log_analysis.get("errors", [])
            if errors:
                for i, error in enumerate(errors, 1):
                    content += f"""#### Error {i}: {error.get('type', 'Error Desconocido')}

- **Timestamp**: {error.get('timestamp', 'N/A')}
- **Ubicación**: {error.get('location', 'N/A')}
- **Mensaje**: {error.get('message', 'N/A')}
- **Contexto**: {error.get('context', 'N/A')}

"""
            else:
                content += "No se encontraron errores específicos en el log.\n\n"

            # Agregar análisis de patrones
            patterns = log_analysis.get("patterns", {})
            if patterns:
                content += "### Patrones Detectados\n\n"
                for pattern, count in patterns.items():
                    content += f"- **{pattern}**: {count} ocurrencias\n"
                content += "\n"
        else:
            content += "No se pudo analizar el archivo de log.\n\n"

        content += """## Análisis de Pasos

"""

        # Analizar pasos fallidos
        failed_steps = [step for step in steps if step.get("status") == "FAILED"]
        successful_steps = [step for step in steps if step.get("status") == "SUCCESS"]

        if failed_steps:
            content += f"### Pasos Fallidos ({len(failed_steps)})\n\n"
            for i, step in enumerate(failed_steps, 1):
                content += f"""#### {i}. {step.get('name', 'Paso sin nombre')}

- **Descripción**: {step.get('description', 'Sin descripción')}
- **Duración**: {step.get('duration', 'No disponible')}
- **Timestamp**: {step.get('timestamp', 'No disponible')}

"""
                # Agregar evidencias si existen
                evidence = step.get("evidence", [])
                if evidence:
                    content += "**Evidencias del Fallo:**\n"
                    for ev in evidence:
                        content += f"- [{ev.get('name', 'Evidencia')}]({ev.get('path', '#')}) ({ev.get('timestamp', 'Sin timestamp')})\n"
                    content += "\n"

        if successful_steps:
            content += f"### Pasos Exitosos ({len(successful_steps)})\n\n"
            for i, step in enumerate(successful_steps, 1):
                content += f"- **{i}.** {step.get('name', 'Paso sin nombre')} - {step.get('timestamp', 'N/A')}\n"
            content += "\n"

        # Agregar recomendaciones
        content += """## Recomendaciones para Solución

### Acciones Inmediatas

1. **Revisar Screenshots**: Examinar las capturas de pantalla del momento del fallo
2. **Analizar Log**: Revisar el archivo de log completo para más detalles
3. **Reproducir**: Intentar reproducir el fallo en un entorno controlado

### Posibles Causas

"""

        # Generar recomendaciones basadas en el análisis
        if log_analysis.get("errors"):
            content += "- **Errores de Selenium**: Verificar que los elementos estén disponibles\n"
            content += (
                "- **Timeouts**: Revisar tiempos de espera y condiciones de red\n"
            )
            content += "- **Elementos no encontrados**: Verificar selectores y estado de la página\n"

        content += """- **Problemas de red**: Verificar conectividad y velocidad
- **Cambios en la UI**: Revisar si la interfaz ha cambiado
- **Datos de prueba**: Verificar que los datos de entrada sean válidos

### Checklist de Verificación

- [ ] ¿Los elementos de la página están visibles?
- [ ] ¿Los selectores siguen siendo válidos?
- [ ] ¿La aplicación está funcionando correctamente?
- [ ] ¿Los datos de prueba son correctos?
- [ ] ¿Hay problemas de red o conectividad?

## Archivos de Referencia

- **Log Completo**: `{exec_info.get('log_file', 'N/A')}`
- **Screenshots**: `{exec_info.get('evidence_directory', 'N/A')}/screenshots/`
- **Reporte JSON**: `reports/execution_report_*.json`

---
*Análisis generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        return content

    def _analyze_log_file(self, log_file_path):
        """Analiza el archivo de log para extraer información de errores"""
        try:
            if not log_file_path or not os.path.exists(log_file_path):
                return {}

            log_analysis = {
                "file_path": log_file_path,
                "file_size": os.path.getsize(log_file_path),
                "last_modified": datetime.fromtimestamp(
                    os.path.getmtime(log_file_path)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "errors": [],
                "patterns": {},
            }

            with open(log_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Patrones de error comunes
            error_patterns = [
                (r"ERROR", "Error General"),
                (r"FAILED", "Paso Fallido"),
                (r"Exception", "Excepción"),
                (r"TimeoutException", "Timeout"),
                (r"NoSuchElementException", "Elemento No Encontrado"),
                (r"WebDriverException", "Error de WebDriver"),
                (r"AssertionError", "Error de Aserción"),
                (r"AttributeError", "Error de Atributo"),
                (r"KeyError", "Error de Clave"),
                (r"ValueError", "Error de Valor"),
            ]

            # Contar patrones
            for pattern, name in error_patterns:
                count = sum(
                    1 for line in lines if re.search(pattern, line, re.IGNORECASE)
                )
                if count > 0:
                    log_analysis["patterns"][name] = count

            # Extraer errores específicos
            for i, line in enumerate(lines):
                line = line.strip()
                if any(
                    re.search(pattern, line, re.IGNORECASE)
                    for pattern, _ in error_patterns
                ):
                    error_info = {
                        "line_number": i + 1,
                        "timestamp": self._extract_timestamp(line),
                        "type": self._classify_error(line),
                        "message": line,
                        "context": self._get_context(lines, i),
                    }
                    log_analysis["errors"].append(error_info)

            return log_analysis

        except Exception as e:
            self.logger.error(f"Error analizando log: {str(e)}")
            return {}

    def _extract_timestamp(self, line):
        """Extrae timestamp de una línea de log"""
        timestamp_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        match = re.search(timestamp_pattern, line)
        return match.group(1) if match else "N/A"

    def _classify_error(self, line):
        """Clasifica el tipo de error basado en el contenido"""
        if "NoSuchElementException" in line:
            return "Elemento No Encontrado"
        elif "TimeoutException" in line:
            return "Timeout"
        elif "WebDriverException" in line:
            return "Error de WebDriver"
        elif "AssertionError" in line:
            return "Error de Aserción"
        elif "Exception" in line:
            return "Excepción General"
        elif "ERROR" in line:
            return "Error de Log"
        else:
            return "Error Desconocido"

    def _get_context(self, lines, error_line_index, context_lines=2):
        """Obtiene contexto alrededor de una línea de error"""
        start = max(0, error_line_index - context_lines)
        end = min(len(lines), error_line_index + context_lines + 1)
        context = lines[start:end]
        return "\n".join(
            f"L{start + i + 1}: {line.strip()}" for i, line in enumerate(context)
        )

    def generate_daily_documentation_summary(self):
        """Genera un resumen diario de toda la documentación"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            summary_file = self.docs_dir / f"daily_summary_{today}.md"

            content = f"""# Resumen Diario de Documentación - {today}

## Estructura de Documentación

### Ejecuciones Exitosas
"""

            success_files = list(self.success_docs_dir.glob("*.md"))
            if success_files:
                content += f"- **Total**: {len(success_files)} documentos\n"
                for file in sorted(success_files):
                    content += f"- [{file.name}]({file.relative_to(self.docs_dir)})\n"
            else:
                content += "- No hay ejecuciones exitosas documentadas\n"

            content += "\n### Ejecuciones Fallidas\n"

            failed_files = list(self.failed_docs_dir.glob("*.md"))
            if failed_files:
                content += f"- **Total**: {len(failed_files)} documentos\n"
                for file in sorted(failed_files):
                    content += f"- [{file.name}]({file.relative_to(self.docs_dir)})\n"
            else:
                content += "- No hay ejecuciones fallidas documentadas\n"

            content += "\n### Ejecuciones Parciales\n"

            partial_files = list(self.partial_docs_dir.glob("*.md"))
            if partial_files:
                content += f"- **Total**: {len(partial_files)} documentos\n"
                for file in sorted(partial_files):
                    content += f"- [{file.name}]({file.relative_to(self.docs_dir)})\n"
            else:
                content += "- No hay ejecuciones parciales documentadas\n"

            content += f"""
## Estadísticas del Día

- **Exitosas**: {len(success_files)}
- **Fallidas**: {len(failed_files)}
- **Parciales**: {len(partial_files)}
- **Total**: {len(success_files) + len(failed_files) + len(partial_files)}

---
*Resumen generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(content)

            self.logger.info(f"Resumen diario generado: {summary_file}")
            return str(summary_file)

        except Exception as e:
            self.logger.error(f"Error generando resumen diario: {str(e)}")
            return None
