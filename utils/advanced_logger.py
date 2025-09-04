"""
Sistema de Logging Avanzado para Automatización de Pruebas
Organización por fecha, feature y resultado para facilitar análisis
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class AdvancedLogger:
    """Sistema avanzado de logging con organización automática"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logs_dir = self.project_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Cache de loggers para evitar duplicados
        self._loggers = {}

    def get_test_logger(
        self,
        feature_name: str,
        scenario_name: str,
        execution_date: Optional[str] = None,
    ) -> logging.Logger:
        """
        Obtiene un logger configurado para un test específico con organización por fecha

        Args:
            feature_name: Nombre del feature
            scenario_name: Nombre del scenario
            execution_date: Fecha de ejecución (opcional, usa fecha actual si no se especifica)

        Returns:
            Logger configurado
        """
        if execution_date is None:
            execution_date = datetime.now().strftime("%Y-%m-%d")

        # Crear estructura de directorios: logs/fecha/feature/
        date_dir = self.logs_dir / execution_date.replace("-", "_")
        feature_dir = date_dir / feature_name
        feature_dir.mkdir(parents=True, exist_ok=True)

        # Nombre del archivo de log con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{scenario_name}_{timestamp}.log"
        log_file = feature_dir / log_filename

        # Crear logger único para esta ejecución
        logger_name = f"{execution_date}_{feature_name}_{scenario_name}_{timestamp}"

        if logger_name not in self._loggers:
            self._loggers[logger_name] = self._create_logger(
                logger_name, log_file, feature_name, scenario_name
            )

        return self._loggers[logger_name]

    def _create_logger(
        self, name: str, log_file: Path, feature_name: str, scenario_name: str
    ) -> logging.Logger:
        """Crea un logger con configuración avanzada"""

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Evitar duplicar handlers
        if logger.handlers:
            return logger

        # Formato detallado para archivo
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-30s | %(funcName)-20s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Formato simplificado para consola
        console_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S"
        )

        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Agregar información inicial al log
        logger.info("=" * 80)
        logger.info(f"INICIO DE EJECUCIÓN - {feature_name} - {scenario_name}")
        logger.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Archivo de log: {log_file}")
        logger.info("=" * 80)

        return logger

    def log_step_execution(
        self,
        logger: logging.Logger,
        step_name: str,
        step_type: str,
        status: str,
        duration: float = None,
        details: Dict[str, Any] = None,
    ):
        """
        Registra la ejecución de un step con detalles estructurados

        Args:
            logger: Logger a usar
            step_name: Nombre del step
            step_type: Tipo de step (given/when/then)
            status: Estado del step (SUCCESS/FAILED/SKIPPED)
            duration: Duración en segundos
            details: Detalles adicionales
        """
        status_emoji = {
            "SUCCESS": "✅",
            "FAILED": "❌",
            "SKIPPED": "⏭️",
            "PENDING": "⏳",
        }.get(status, "❓")

        logger.info(f"{status_emoji} STEP {step_type.upper()}: {step_name}")
        logger.info(f"   Estado: {status}")

        if duration is not None:
            logger.info(f"   Duración: {duration:.2f} segundos")

        if details:
            for key, value in details.items():
                logger.info(f"   {key}: {value}")

        logger.info("-" * 60)

    def log_error_details(
        self, logger: logging.Logger, error: Exception, context: Dict[str, Any] = None
    ):
        """
        Registra detalles de un error con contexto

        Args:
            logger: Logger a usar
            error: Excepción ocurrida
            context: Contexto adicional del error
        """
        logger.error("🚨 ERROR DETECTADO")
        logger.error(f"   Tipo: {type(error).__name__}")
        logger.error(f"   Mensaje: {str(error)}")

        if context:
            logger.error("   Contexto:")
            for key, value in context.items():
                logger.error(f"     {key}: {value}")

        # Log del stack trace
        import traceback

        logger.error("   Stack Trace:")
        for line in traceback.format_exc().split("\n"):
            if line.strip():
                logger.error(f"     {line}")

        logger.error("-" * 60)

    def log_evidence_capture(
        self,
        logger: logging.Logger,
        evidence_type: str,
        file_path: str,
        description: str = None,
    ):
        """
        Registra la captura de evidencias

        Args:
            logger: Logger a usar
            evidence_type: Tipo de evidencia (screenshot, log, etc.)
            file_path: Ruta del archivo de evidencia
            description: Descripción de la evidencia
        """
        logger.info(f"📸 EVIDENCIA CAPTURADA: {evidence_type}")
        logger.info(f"   Archivo: {file_path}")
        if description:
            logger.info(f"   Descripción: {description}")
        logger.info(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("-" * 40)

    def log_test_summary(self, logger: logging.Logger, summary: Dict[str, Any]):
        """
        Registra un resumen de la ejecución del test

        Args:
            logger: Logger a usar
            summary: Diccionario con resumen de la ejecución
        """
        logger.info("=" * 80)
        logger.info("RESUMEN DE EJECUCIÓN")
        logger.info("=" * 80)

        for key, value in summary.items():
            logger.info(f"{key}: {value}")

        logger.info("=" * 80)
        logger.info(
            f"FIN DE EJECUCIÓN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info("=" * 80)

    def create_execution_metadata(
        self, feature_name: str, scenario_name: str, execution_date: str, log_file: Path
    ) -> Dict[str, Any]:
        """
        Crea metadatos de la ejecución para facilitar análisis

        Args:
            feature_name: Nombre del feature
            scenario_name: Nombre del scenario
            execution_date: Fecha de ejecución
            log_file: Archivo de log

        Returns:
            Diccionario con metadatos
        """
        metadata = {
            "execution_info": {
                "feature_name": feature_name,
                "scenario_name": scenario_name,
                "execution_date": execution_date,
                "start_time": datetime.now().isoformat(),
                "log_file": str(log_file),
            },
            "file_info": {
                "size_bytes": log_file.stat().st_size if log_file.exists() else 0,
                "created": datetime.now().isoformat(),
                "path": str(log_file),
            },
            "organization": {
                "date_directory": execution_date.replace("-", "_"),
                "feature_directory": feature_name,
                "log_filename": log_file.name,
            },
        }

        # Guardar metadatos como archivo JSON
        metadata_file = log_file.with_suffix(".json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return metadata

    def get_logs_by_date(self, date: str) -> List[Path]:
        """
        Obtiene todos los logs de una fecha específica

        Args:
            date: Fecha en formato YYYY-MM-DD

        Returns:
            Lista de archivos de log
        """
        date_dir = self.logs_dir / date.replace("-", "_")
        if not date_dir.exists():
            return []

        return list(date_dir.rglob("*.log"))

    def get_logs_by_feature(self, feature_name: str, date: str = None) -> List[Path]:
        """
        Obtiene todos los logs de un feature específico

        Args:
            feature_name: Nombre del feature
            date: Fecha específica (opcional)

        Returns:
            Lista de archivos de log
        """
        if date:
            feature_dir = self.logs_dir / date.replace("-", "_") / feature_name
            if not feature_dir.exists():
                return []
            return list(feature_dir.glob("*.log"))
        else:
            # Buscar en todas las fechas
            logs = []
            for date_dir in self.logs_dir.iterdir():
                if date_dir.is_dir():
                    feature_dir = date_dir / feature_name
                    if feature_dir.exists():
                        logs.extend(feature_dir.glob("*.log"))
            return logs

    def analyze_log_file(self, log_file: Path) -> Dict[str, Any]:
        """
        Analiza un archivo de log y extrae estadísticas

        Args:
            log_file: Archivo de log a analizar

        Returns:
            Diccionario con estadísticas del log
        """
        analysis = {
            "file_path": str(log_file),
            "file_size": 0,
            "total_lines": 0,
            "error_count": 0,
            "warning_count": 0,
            "info_count": 0,
            "debug_count": 0,
            "execution_time": None,
            "steps_executed": 0,
            "errors_found": [],
        }

        try:
            if not log_file.exists():
                return analysis

            analysis["file_size"] = log_file.stat().st_size

            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            analysis["total_lines"] = len(lines)

            for line in lines:
                line_lower = line.lower()
                if "error" in line_lower:
                    analysis["error_count"] += 1
                    if "error detected" in line_lower:
                        analysis["errors_found"].append(line.strip())
                elif "warning" in line_lower:
                    analysis["warning_count"] += 1
                elif "info" in line_lower:
                    analysis["info_count"] += 1
                elif "debug" in line_lower:
                    analysis["debug_count"] += 1

                if "step" in line_lower and (
                    "given" in line_lower
                    or "when" in line_lower
                    or "then" in line_lower
                ):
                    analysis["steps_executed"] += 1

            # Calcular tiempo de ejecución si está disponible
            start_time = None
            end_time = None

            for line in lines:
                if "inicio de ejecución" in line.lower():
                    # Extraer timestamp del inicio
                    start_time = self._extract_timestamp(line)
                elif "fin de ejecución" in line.lower():
                    # Extraer timestamp del fin
                    end_time = self._extract_timestamp(line)

            if start_time and end_time:
                try:
                    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                    analysis["execution_time"] = (end_dt - start_dt).total_seconds()
                except ValueError:
                    pass

        except Exception as e:
            analysis["analysis_error"] = str(e)

        return analysis

    def _extract_timestamp(self, line: str) -> Optional[str]:
        """Extrae timestamp de una línea de log"""
        import re

        timestamp_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        match = re.search(timestamp_pattern, line)
        return match.group(1) if match else None


# Instancia global para uso fácil
advanced_logger = AdvancedLogger()
