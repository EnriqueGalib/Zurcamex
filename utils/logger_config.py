"""
Sistema de Logging para Automatización de Pruebas
Compatibilidad con sistema avanzado de logging organizado por fecha y feature
"""

import logging
import os

from .advanced_logger import advanced_logger


def setup_logger(name, log_file=None, level=logging.INFO):
    """Configura un logger con handlers de archivo y consola (compatibilidad)"""

    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers
    if logger.handlers:
        return logger

    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo si se especifica
    if log_file:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_test_logger(feature_name, scenario_name, execution_date=None):
    """
    Obtiene un logger configurado para un test específico con organización por fecha

    Args:
        feature_name: Nombre del feature
        scenario_name: Nombre del scenario
        execution_date: Fecha de ejecución (opcional)

    Returns:
        Logger configurado con organización avanzada
    """
    return advanced_logger.get_test_logger(feature_name, scenario_name, execution_date)


def log_step_execution(
    logger, step_name, step_type, status, duration=None, details=None
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
    advanced_logger.log_step_execution(
        logger, step_name, step_type, status, duration, details
    )


def log_error_details(logger, error, context=None):
    """
    Registra detalles de un error con contexto

    Args:
        logger: Logger a usar
        error: Excepción ocurrida
        context: Contexto adicional del error
    """
    advanced_logger.log_error_details(logger, error, context)


def log_evidence_capture(logger, evidence_type, file_path, description=None):
    """
    Registra la captura de evidencias

    Args:
        logger: Logger a usar
        evidence_type: Tipo de evidencia (screenshot, log, etc.)
        file_path: Ruta del archivo de evidencia
        description: Descripción de la evidencia
    """
    advanced_logger.log_evidence_capture(logger, evidence_type, file_path, description)


def log_test_summary(logger, summary):
    """
    Registra un resumen de la ejecución del test

    Args:
        logger: Logger a usar
        summary: Diccionario con resumen de la ejecución
    """
    advanced_logger.log_test_summary(logger, summary)


def get_logs_by_date(date):
    """
    Obtiene todos los logs de una fecha específica

    Args:
        date: Fecha en formato YYYY-MM-DD

    Returns:
        Lista de archivos de log
    """
    return advanced_logger.get_logs_by_date(date)


def get_logs_by_feature(feature_name, date=None):
    """
    Obtiene todos los logs de un feature específico

    Args:
        feature_name: Nombre del feature
        date: Fecha específica (opcional)

    Returns:
        Lista de archivos de log
    """
    return advanced_logger.get_logs_by_feature(feature_name, date)


def analyze_log_file(log_file):
    """
    Analiza un archivo de log y extrae estadísticas

    Args:
        log_file: Archivo de log a analizar

    Returns:
        Diccionario con estadísticas del log
    """
    return advanced_logger.analyze_log_file(log_file)
