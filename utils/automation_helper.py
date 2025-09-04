"""
Helper Principal para Automatización de Pruebas
Integra todas las funcionalidades del sistema de automatización
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .advanced_logger import advanced_logger
from .code_reuse_helper import CodeReuseHelper
from .element_validator import ElementValidator
from .pdf_generator import PDFGenerator


class AutomationHelper:
    """Helper principal que integra todas las funcionalidades del sistema"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)

        # Inicializar componentes
        self.code_helper = CodeReuseHelper(project_root)
        self.pdf_generator = PDFGenerator()

    def prepare_test_execution(
        self, feature_name: str, scenario_name: str, driver=None
    ) -> Dict[str, Any]:
        """
        Prepara la ejecución de una prueba con todas las validaciones

        Args:
            feature_name: Nombre del feature
            scenario_name: Nombre del scenario
            driver: Instancia del WebDriver (opcional)

        Returns:
            Diccionario con información de preparación
        """
        self.logger.info(f"🚀 Preparando ejecución: {feature_name} - {scenario_name}")

        preparation_result = {
            "feature_name": feature_name,
            "scenario_name": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "preparation_steps": [],
            "validation_results": {},
            "reuse_suggestions": {},
            "ready_to_execute": False,
        }

        try:
            # 1. Verificar código reutilizable
            self.logger.info("🔍 Buscando código reutilizable...")
            reuse_suggestions = self.code_helper.suggest_code_reuse(
                f"Automatización de {feature_name} - {scenario_name}"
            )
            preparation_result["reuse_suggestions"] = reuse_suggestions
            preparation_result["preparation_steps"].append(
                {
                    "step": "code_reuse_analysis",
                    "status": "completed",
                    "details": (
                        f"Encontrados {len(reuse_suggestions.get('reusable_steps', []))} "
                        f"steps reutilizables"
                    ),
                }
            )

            # 2. Validar elementos si hay driver disponible
            if driver:
                self.logger.info("🔍 Validando elementos de la página...")
                try:
                    element_validator = ElementValidator(driver)
                    validation_result = element_validator.validate_feature_elements(
                        feature_name
                    )
                    preparation_result["validation_results"] = validation_result

                    if validation_result["overall_status"] == "SUCCESS":
                        preparation_result["preparation_steps"].append(
                            {
                                "step": "element_validation",
                                "status": "success",
                                "details": (
                                    f"Todos los elementos válidos "
                                    f"({validation_result['valid_elements']} elementos)"
                                ),
                            }
                        )
                        preparation_result["ready_to_execute"] = True
                    else:
                        preparation_result["preparation_steps"].append(
                            {
                                "step": "element_validation",
                                "status": "failed",
                                "details": (
                                    f"Elementos faltantes: "
                                    f"{validation_result['invalid_elements']}"
                                ),
                            }
                        )
                        preparation_result["ready_to_execute"] = False

                except Exception as e:
                    self.logger.warning(f"Error en validación de elementos: {e}")
                    preparation_result["preparation_steps"].append(
                        {
                            "step": "element_validation",
                            "status": "error",
                            "details": str(e),
                        }
                    )
            else:
                self.logger.info(
                    "⚠️ No hay driver disponible, saltando validación de elementos"
                )
                preparation_result["preparation_steps"].append(
                    {
                        "step": "element_validation",
                        "status": "skipped",
                        "details": "No hay driver disponible",
                    }
                )
                preparation_result["ready_to_execute"] = True

            # 3. Configurar logging
            self.logger.info("📝 Configurando sistema de logging...")
            test_logger = advanced_logger.get_test_logger(feature_name, scenario_name)
            preparation_result["logger"] = test_logger
            preparation_result["preparation_steps"].append(
                {
                    "step": "logging_setup",
                    "status": "completed",
                    "details": "Sistema de logging configurado",
                }
            )

            self.logger.info(
                f"✅ Preparación completada. Listo para ejecutar: "
                f"{preparation_result['ready_to_execute']}"
            )

        except Exception as e:
            self.logger.error(f"❌ Error en preparación: {e}")
            preparation_result["preparation_steps"].append(
                {"step": "preparation_error", "status": "error", "details": str(e)}
            )
            preparation_result["ready_to_execute"] = False

        return preparation_result

    def execute_test_with_monitoring(
        self, feature_name: str, scenario_name: str, test_function, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Ejecuta una prueba con monitoreo completo

        Args:
            feature_name: Nombre del feature
            scenario_name: Nombre del scenario
            test_function: Función de prueba a ejecutar
            *args, **kwargs: Argumentos para la función de prueba

        Returns:
            Diccionario con resultados de la ejecución
        """
        self.logger.info(f"🎯 Ejecutando prueba: {feature_name} - {scenario_name}")

        execution_result = {
            "feature_name": feature_name,
            "scenario_name": scenario_name,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration": None,
            "status": "PENDING",
            "steps_executed": [],
            "errors": [],
            "evidences": [],
            "summary": {},
        }

        # Obtener logger para esta ejecución
        test_logger = advanced_logger.get_test_logger(feature_name, scenario_name)

        try:
            # Ejecutar la función de prueba
            start_time = datetime.now()
            result = test_function(*args, **kwargs)
            end_time = datetime.now()

            execution_result["end_time"] = end_time.isoformat()
            execution_result["duration"] = (end_time - start_time).total_seconds()
            execution_result["status"] = "SUCCESS"

            # Log del resumen
            summary = {
                "execution_time": f"{execution_result['duration']:.2f} segundos",
                "status": "SUCCESS",
                "result": str(result) if result else "No result returned",
            }

            advanced_logger.log_test_summary(test_logger, summary)
            execution_result["summary"] = summary

            self.logger.info(
                f"✅ Prueba ejecutada exitosamente: "
                f"{execution_result['duration']:.2f}s"
            )

        except Exception as e:
            execution_result["end_time"] = datetime.now().isoformat()
            execution_result["status"] = "FAILED"
            execution_result["errors"].append(
                {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Log del error
            advanced_logger.log_error_details(
                test_logger,
                e,
                {
                    "feature": feature_name,
                    "scenario": scenario_name,
                    "execution_time": execution_result.get("duration", "N/A"),
                },
            )

            self.logger.error(f"❌ Prueba falló: {str(e)}")

        return execution_result

    def generate_complete_report(
        self, execution_result: Dict[str, Any], log_file_path: str = None
    ) -> Dict[str, str]:
        """
        Genera reportes completos de la ejecución

        Args:
            execution_result: Resultados de la ejecución
            log_file_path: Ruta del archivo de log

        Returns:
            Diccionario con rutas de archivos generados
        """
        self.logger.info("📊 Generando reportes completos...")

        generated_files = {}

        try:
            # Preparar datos para el PDF
            execution_data = {
                "execution_info": {
                    "test_name": (
                        f"{execution_result['feature_name']} - "
                        f"{execution_result['scenario_name']}"
                    ),
                    "feature_name": execution_result["feature_name"],
                    "execution_date": execution_result["start_time"][:10],
                    "start_time": execution_result["start_time"],
                    "total_duration": (
                        f"{execution_result.get('duration', 0):.2f} segundos"
                    ),
                    "overall_status": execution_result["status"],
                    "execution_type": "Automated Test",
                },
                "summary": {
                    "total_steps": len(execution_result.get("steps_executed", [])),
                    "successful_steps": len(
                        [
                            s
                            for s in execution_result.get("steps_executed", [])
                            if s.get("status") == "SUCCESS"
                        ]
                    ),
                    "failed_steps": len(
                        [
                            s
                            for s in execution_result.get("steps_executed", [])
                            if s.get("status") == "FAILED"
                        ]
                    ),
                    "screenshots_taken": len(execution_result.get("evidences", [])),
                },
                "steps": execution_result.get("steps_executed", []),
            }

            # Generar PDF
            pdf_path, metadata_path = self.pdf_generator.generate_execution_pdf(
                execution_data, log_file_path
            )

            if pdf_path:
                generated_files["pdf"] = pdf_path
                generated_files["pdf_metadata"] = metadata_path
                self.logger.info(f"📄 PDF generado: {pdf_path}")

            # Generar reporte de análisis si hay errores
            if execution_result["status"] == "FAILED" and execution_result.get(
                "errors"
            ):
                analysis_report = self._generate_failure_analysis(execution_result)
                generated_files["failure_analysis"] = analysis_report
                self.logger.info(f"🔍 Análisis de fallo generado: {analysis_report}")

        except Exception as e:
            self.logger.error(f"❌ Error generando reportes: {e}")
            generated_files["error"] = str(e)

        return generated_files

    def _generate_failure_analysis(self, execution_result: Dict[str, Any]) -> str:
        """
        Genera análisis detallado de fallos

        Args:
            execution_result: Resultados de la ejecución

        Returns:
            Ruta del archivo de análisis generado
        """
        try:
            # Crear directorio para análisis
            analysis_dir = Path("docs/FALLIDOS")
            analysis_dir.mkdir(parents=True, exist_ok=True)

            # Generar nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            feature_name = execution_result["feature_name"]
            scenario_name = execution_result["scenario_name"]

            analysis_file = (
                analysis_dir
                / f"FAILURE_ANALYSIS_{feature_name}_{scenario_name}_{timestamp}.md"
            )

            # Generar contenido del análisis
            analysis_content = f"""# ❌ Análisis de Fallo - {feature_name} - {scenario_name}

## 🚨 Resumen del Fallo

- **Fecha**: {execution_result['start_time'][:10]}
- **Hora**: {execution_result['start_time'][11:19]}
- **Duración**: {execution_result.get('duration', 0):.2f} segundos
- **Feature**: {feature_name}
- **Scenario**: {scenario_name}

## 🔍 Errores Encontrados

"""

            for i, error in enumerate(execution_result.get("errors", []), 1):
                analysis_content += f"""### Error {i}

- **Tipo**: {error['error_type']}
- **Mensaje**: {error['error_message']}
- **Timestamp**: {error['timestamp']}

"""

            analysis_content += f"""## 💡 Recomendaciones

### 🔧 Acciones Inmediatas

1. **Revisar Logs**: Examinar el archivo de log completo para más detalles
2. **Verificar Elementos**: Confirmar que los elementos de la página estén disponibles
3. **Validar Datos**: Verificar que los datos de prueba sean correctos
4. **Reproducir Manualmente**: Intentar reproducir el fallo manualmente

### 🛠️ Posibles Causas

- Cambios en la interfaz de usuario
- Problemas de conectividad o rendimiento
- Datos de prueba incorrectos o faltantes
- Elementos no disponibles o con selectores incorrectos
- Timeouts o problemas de sincronización

### 📋 Checklist de Verificación

- [ ] ¿La aplicación está funcionando correctamente?
- [ ] ¿Los elementos de la página están visibles?
- [ ] ¿Los selectores siguen siendo válidos?
- [ ] ¿Los datos de prueba son correctos?
- [ ] ¿Hay problemas de red o conectividad?

## 📁 Archivos de Referencia

- **Log de Ejecución**: Ver directorio de logs correspondiente
- **Screenshots**: Ver directorio de evidencias
- **Reporte PDF**: Ver directorio de PDFs

---
*Análisis generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Sistema de Automatización de Pruebas - Zucarmex*
"""

            # Guardar archivo
            with open(analysis_file, "w", encoding="utf-8") as f:
                f.write(analysis_content)

            return str(analysis_file)

        except Exception as e:
            self.logger.error(f"Error generando análisis de fallo: {e}")
            return None

    def cleanup_old_files(self, days_to_keep: int = 30) -> Dict[str, int]:
        """
        Limpia archivos antiguos del sistema

        Args:
            days_to_keep: Días de archivos a mantener

        Returns:
            Diccionario con estadísticas de limpieza
        """
        self.logger.info(
            f"🧹 Limpiando archivos antiguos (más de {days_to_keep} días)..."
        )

        cleanup_stats = {
            "logs_cleaned": 0,
            "evidences_cleaned": 0,
            "reports_cleaned": 0,
            "pdfs_cleaned": 0,
            "total_size_freed": 0,
        }

        try:
            from datetime import timedelta

            cutoff_date = datetime.now() - timedelta(days=days_to_keep)

            # Limpiar logs
            logs_dir = self.project_root / "logs"
            if logs_dir.exists():
                for log_file in logs_dir.rglob("*.log"):
                    if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                        cleanup_stats["total_size_freed"] += log_file.stat().st_size
                        log_file.unlink()
                        cleanup_stats["logs_cleaned"] += 1

            # Limpiar evidencias
            evidences_dir = self.project_root / "evidences"
            if evidences_dir.exists():
                for evidence_file in evidences_dir.rglob("*.png"):
                    if (
                        datetime.fromtimestamp(evidence_file.stat().st_mtime)
                        < cutoff_date
                    ):
                        cleanup_stats[
                            "total_size_freed"
                        ] += evidence_file.stat().st_size
                        evidence_file.unlink()
                        cleanup_stats["evidences_cleaned"] += 1

            # Limpiar reportes
            reports_dir = self.project_root / "reports"
            if reports_dir.exists():
                for report_file in reports_dir.rglob("*.html"):
                    if (
                        datetime.fromtimestamp(report_file.stat().st_mtime)
                        < cutoff_date
                    ):
                        cleanup_stats["total_size_freed"] += report_file.stat().st_size
                        report_file.unlink()
                        cleanup_stats["reports_cleaned"] += 1

            # Limpiar PDFs
            pdfs_dir = self.project_root / "pdfs"
            if pdfs_dir.exists():
                for pdf_file in pdfs_dir.rglob("*.html"):
                    if datetime.fromtimestamp(pdf_file.stat().st_mtime) < cutoff_date:
                        cleanup_stats["total_size_freed"] += pdf_file.stat().st_size
                        pdf_file.unlink()
                        cleanup_stats["pdfs_cleaned"] += 1

            self.logger.info(f"✅ Limpieza completada: {cleanup_stats}")

        except Exception as e:
            self.logger.error(f"❌ Error en limpieza: {e}")

        return cleanup_stats


# Instancia global para uso fácil
automation_helper = AutomationHelper()
