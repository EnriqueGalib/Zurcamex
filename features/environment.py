import json
import logging
import os
import tkinter as tk
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.cleanup_manager import CleanupManager
from utils.documentation_manager import DocumentationManager
from utils.evidence_manager import EvidenceManager
from utils.execution_report_generator import ExecutionReportGenerator


def get_screen_dimensions():
    """Obtiene las dimensiones de la pantalla actual"""
    try:
        # Método 1: Usar tkinter
        try:
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.destroy()

            logging.info(
                f"Dimensiones de pantalla detectadas (tkinter): {screen_width}x{screen_height}"
            )
            return screen_width, screen_height
        except Exception as e:
            logging.warning(f"Error con tkinter: {str(e)}")

        # Método 2: Usar ctypes (Windows)
        try:
            import ctypes

            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
            screen_height = user32.GetSystemMetrics(1)  # SM_CYSCREEN

            logging.info(
                f"Dimensiones de pantalla detectadas (ctypes): {screen_width}x{screen_height}"
            )
            return screen_width, screen_height
        except Exception as e:
            logging.warning(f"Error con ctypes: {str(e)}")

        # Método 3: Usar subprocess (cross-platform)
        try:
            import platform
            import subprocess

            if platform.system() == "Windows":
                result = subprocess.run(
                    [
                        "wmic",
                        "path",
                        "Win32_VideoController",
                        "get",
                        "CurrentHorizontalResolution,CurrentVerticalResolution",
                        "/format:value",
                    ],
                    capture_output=True,
                    text=True,
                )
                lines = result.stdout.strip().split("\n")
                width = height = None
                for line in lines:
                    if "CurrentHorizontalResolution=" in line:
                        width = int(line.split("=")[1])
                    elif "CurrentVerticalResolution=" in line:
                        height = int(line.split("=")[1])

                if width and height:
                    logging.info(
                        f"Dimensiones de pantalla detectadas (wmic): {width}x{height}"
                    )
                    return width, height
        except Exception as e:
            logging.warning(f"Error con subprocess: {str(e)}")

        # Valores por defecto si todos los métodos fallan
        logging.warning(
            "No se pudieron detectar dimensiones de pantalla, usando valores por defecto"
        )
        return 1920, 1080

    except Exception as e:
        logging.error(f"Error general obteniendo dimensiones de pantalla: {str(e)}")
        return 1920, 1080


def get_driver():
    """Configura y retorna el driver de Chrome adaptado a la pantalla"""
    try:
        # Obtener dimensiones de la pantalla
        screen_width, screen_height = get_screen_dimensions()

        # Configurar opciones de Chrome
        options = webdriver.ChromeOptions()

        # Opciones básicas
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        # Configurar tamaño de ventana adaptativo
        if screen_width >= 1920 and screen_height >= 1080:
            # Pantalla grande - maximizar
            options.add_argument("--start-maximized")
            logging.info("Configurando navegador para pantalla grande (maximizado)")
        else:
            # Pantalla pequeña - usar dimensiones específicas
            window_width = min(screen_width - 100, 1200)  # Dejar margen
            window_height = min(screen_height - 100, 800)  # Dejar margen
            options.add_argument(f"--window-size={window_width},{window_height}")
            logging.info(
                f"Configurando navegador para pantalla pequeña: {window_width}x{window_height}"
            )

        # Opciones adicionales para mejor rendimiento
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        # options.add_argument("--disable-images")  # Comentado: puede causar problemas con OKTA
        # options.add_argument("--disable-javascript")  # Comentado: OKTA necesita JavaScript

        # Configurar user agent
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Crear el driver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logging.warning(f"Error con ChromeDriverManager: {str(e)}")
            # Fallback: usar driver del sistema
            driver = webdriver.Chrome(options=options)

        # Configurar timeouts
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)

        # Maximizar la ventana del navegador
        try:
            driver.maximize_window()
            logging.info("✅ Navegador maximizado exitosamente")
        except Exception as e:
            logging.warning(f"Error maximizando navegador: {str(e)}")
            # Fallback: ajustar ventana si no se puede maximizar
            if not (screen_width >= 1920 and screen_height >= 1080):
                driver.set_window_size(
                    min(screen_width - 100, 1200), min(screen_height - 100, 800)
                )
                logging.info("Ventana ajustada a dimensiones de pantalla")

        logging.info(
            f"Driver configurado exitosamente para pantalla {screen_width}x{screen_height}"
        )
        return driver

    except Exception as e:
        logging.error(f"Error configurando el driver: {str(e)}")
        raise


def before_all(context):
    """Se ejecuta una sola vez antes de todos los escenarios"""
    try:
        with open(os.path.join(os.getcwd(), "config.json"), "r", encoding="utf-8") as f:
            context.config_data = json.load(f)
        logging.info("Configuración cargada correctamente")
    except Exception as e:
        logging.error(f"Error cargando config.json: {str(e)}")
        raise


def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    try:
        # Configurar logging específico para el escenario
        setup_scenario_logging(context, scenario)

        # Inicializar gestor de evidencias
        context.evidence_manager = EvidenceManager()

        # Inicializar generador de reportes
        context.report_generator = ExecutionReportGenerator()

        # Inicializar gestor de documentación
        context.documentation_manager = DocumentationManager()

        # Inicializar gestor de limpieza
        try:
            context.cleanup_manager = CleanupManager(
                context.config_data.get("cleanup_management", {})
            )
        except Exception as e:
            logging.warning(f"Error inicializando CleanupManager: {str(e)}")
            context.cleanup_manager = None

        # Inicializar tracking de ejecución
        context.start_time = datetime.now().strftime("%H:%M:%S")
        context.executed_steps = []
        context.screenshots_taken = 0

        # Limpiar archivos antiguos (solo una vez por sesión) - COMENTADO TEMPORALMENTE
        # if not hasattr(context, "_cleanup_done"):
        #     try:
        #         # Comentado temporalmente para evitar errores
        #         # context.evidence_manager.cleanup_old_evidence()
        #         if context.cleanup_manager:
        #             cleanup_summary = context.cleanup_manager.cleanup_old_files()
        #             if cleanup_summary:
        #                 logging.info(
        #                     f"🧹 Limpieza completada: {cleanup_summary['evidences_cleaned']} evidencias, {cleanup_summary['logs_cleaned']} logs, {cleanup_summary['reports_cleaned']} reportes, {cleanup_summary['docs_cleaned']} docs, {cleanup_summary['total_size_freed_mb']} MB liberados"
        #                 )
        #         context._cleanup_done = True
        #     except Exception as e:
        #         logging.warning(f"Error en limpieza inicial: {str(e)}")
        #         context._cleanup_done = True  # Marcar como hecho para evitar reintentos

        context.driver = get_driver()
        logging.info(f"Driver configurado para escenario: {scenario.name}")
    except Exception as e:
        logging.error(f"Error en before_scenario: {str(e)}")
        raise


def setup_scenario_logging(context, scenario):
    """Configura el logging específico para el escenario"""
    try:
        # Crear directorios para logs
        logs_dir = os.path.join("logs", scenario.feature.name, scenario.name)
        os.makedirs(logs_dir, exist_ok=True)

        # Nombre del archivo de log con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"test_{timestamp}.log")

        # Limpiar handlers existentes
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Configurar logging con archivo y consola
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, mode="w", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

        # Guardar la ruta del log en el contexto
        context.log_file = log_file

        logging.info(f"Logging configurado para escenario: {scenario.name}")
        logging.info(f"Archivo de log: {log_file}")

    except Exception as e:
        print(f"Error configurando logging: {str(e)}")
        # Configurar logging básico como fallback
        logging.basicConfig(level=logging.INFO)


def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    try:
        # Finalizar tracking de ejecución
        context.end_time = datetime.now().strftime("%H:%M:%S")
        context.overall_status = "SUCCESS" if scenario.status == "passed" else "FAILED"

        if hasattr(context, "driver"):
            if scenario.status == "failed":
                take_final_screenshot(context, scenario)
            context.driver.quit()
            logging.info("Driver cerrado")

        # Generar resumen diario si está habilitado
        if (
            hasattr(context, "evidence_manager")
            and context.evidence_manager.generate_daily_summaries
        ):
            context.evidence_manager.generate_daily_summary()

        # Generar resumen diario de documentación
        if hasattr(context, "documentation_manager"):
            try:
                doc_summary = (
                    context.documentation_manager.generate_daily_documentation_summary()
                )
                if doc_summary:
                    logging.info(
                        f"📚 Resumen diario de documentación generado: {doc_summary}"
                    )
            except Exception as e:
                logging.error(
                    f"Error generando resumen diario de documentación: {str(e)}"
                )

        # Generar reporte de ejecución
        if hasattr(context, "report_generator"):
            try:
                execution_data = context.report_generator.collect_execution_data(
                    context, scenario, scenario.feature
                )
                html_report, json_report = (
                    context.report_generator.generate_execution_report(execution_data)
                )

                if html_report:
                    logging.info(f"📊 Reporte de ejecución generado: {html_report}")
                    logging.info(f"📄 Reporte JSON generado: {json_report}")

                    # Mostrar mensaje al usuario
                    print("\n" + "=" * 80)
                    print("📊 REPORTE DE EJECUCIÓN GENERADO")
                    print("=" * 80)
                    print(f"✅ Reporte HTML: {html_report}")
                    print(f"📄 Reporte JSON: {json_report}")
                    print("=" * 80)
                else:
                    logging.warning("No se pudo generar el reporte de ejecución")
            except Exception as e:
                logging.error(f"Error generando reporte de ejecución: {str(e)}")

        # Generar documentación específica
        if hasattr(context, "documentation_manager"):
            try:
                log_file_path = getattr(context, "log_file", None)
                doc_path, pdf_path = (
                    context.documentation_manager.generate_execution_documentation(
                        execution_data, log_file_path
                    )
                )

                if doc_path:
                    logging.info(f"📚 Documentación generada: {doc_path}")

                    # Mostrar mensaje al usuario
                    print("\n" + "=" * 80)
                    print("📚 DOCUMENTACIÓN GENERADA")
                    print("=" * 80)
                    print(f"📄 Documento Markdown: {doc_path}")
                    if pdf_path:
                        print(f"📄 Documento PDF (para cliente): {pdf_path}")
                        print(
                            "💼 El documento PDF está listo para compartir con el cliente"
                        )
                    if context.overall_status == "FAILED":
                        print(
                            "🔍 Incluye análisis detallado del fallo y recomendaciones"
                        )
                    print("=" * 80)
                else:
                    logging.warning("No se pudo generar la documentación")
            except Exception as e:
                logging.error(f"Error generando documentación: {str(e)}")

    except Exception as e:
        logging.error(f"Error en after_scenario: {str(e)}")


def take_final_screenshot(context, scenario):
    """Toma una captura final si el escenario falla"""
    try:
        evidence_dir = os.path.join("evidences", scenario.feature.name, scenario.name)
        os.makedirs(evidence_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(evidence_dir, f"FAILED_{timestamp}.png")
        context.driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot de fallo guardado: {screenshot_path}")
    except Exception as e:
        logging.error(f"Error tomando screenshot final: {str(e)}")
