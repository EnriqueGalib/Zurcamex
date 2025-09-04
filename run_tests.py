#!/usr/bin/env python3
"""
Script principal para ejecutar las pruebas de automatización
Sistema de Automatización - Zucarmex QA
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TestRunner:
    """Clase principal para ejecutar las pruebas de automatización"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.features_dir = self.project_root / "features"
        self.reports_dir = self.project_root / "reports"
        self.logs_dir = self.project_root / "logs"

        # Crear directorios si no existen
        self.reports_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def check_dependencies(self):
        """Verifica que las dependencias estén instaladas"""
        try:
            import behave
            import selenium
            from webdriver_manager.chrome import ChromeDriverManager

            logger.info("✅ Dependencias verificadas correctamente")
            return True
        except ImportError as e:
            logger.error(f"❌ Dependencia faltante: {e}")
            logger.error("Ejecuta: pip install -r requirements.txt")
            return False

    def check_config(self):
        """Verifica que el archivo de configuración exista"""
        config_file = self.project_root / "config.json"
        if not config_file.exists():
            logger.error("❌ Archivo config.json no encontrado")
            return False

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.info("✅ Configuración cargada correctamente")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error en config.json: {e}")
            return False

    def list_features(self):
        """Lista todos los features disponibles"""
        logger.info("📋 Features disponibles:")
        feature_files = list(self.features_dir.glob("*.feature"))

        if not feature_files:
            logger.warning("⚠️  No se encontraron archivos .feature")
            return

        for i, feature_file in enumerate(feature_files, 1):
            logger.info(f"  {i}. {feature_file.name}")

            # Leer y mostrar descripción del feature
            try:
                with open(feature_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines[:10]:  # Primeras 10 líneas
                        if line.strip().startswith("Feature:"):
                            feature_name = line.strip().replace("Feature:", "").strip()
                            logger.info(f"     📝 {feature_name}")
                            break
            except Exception as e:
                logger.warning(f"     ⚠️  No se pudo leer la descripción: {e}")

    def run_behave(self, args):
        """Ejecuta behave con los argumentos especificados"""
        try:
            # Construir comando behave
            cmd = ["behave"] + args

            logger.info(f"🚀 Ejecutando: {' '.join(cmd)}")
            logger.info("=" * 60)

            # Ejecutar behave
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=False,  # Mostrar output en tiempo real
                text=True,
            )

            logger.info("=" * 60)
            if result.returncode == 0:
                logger.info("✅ Ejecución completada exitosamente")
            else:
                logger.warning(
                    f"⚠️  Ejecución completada con código: {result.returncode}"
                )

            return result.returncode

        except FileNotFoundError:
            logger.error("❌ Behave no encontrado. Instala con: pip install behave")
            return 1
        except Exception as e:
            logger.error(f"❌ Error ejecutando behave: {e}")
            return 1

    def generate_timestamp_report_dir(self):
        """Genera un directorio de reportes con timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.reports_dir / f"execution_{timestamp}"
        report_dir.mkdir(exist_ok=True)
        return report_dir

    def run_with_format(self, format_type, feature_file=None, tags=None):
        """Ejecuta las pruebas con un formato específico"""
        args = []

        # Agregar feature específico si se especifica
        if feature_file:
            if not feature_file.endswith(".feature"):
                feature_file += ".feature"
            feature_path = self.features_dir / feature_file
            if not feature_path.exists():
                logger.error(f"❌ Feature no encontrado: {feature_path}")
                return 1
            args.append(str(feature_path))

        # Agregar tags si se especifican
        if tags:
            args.extend(["--tags", tags])

        # Configurar formato de salida
        if format_type == "html":
            report_dir = self.generate_timestamp_report_dir()
            html_report = report_dir / "report.html"
            args.extend(["--format", "html", "--outfile", str(html_report)])
            logger.info(f"📄 Reporte HTML se generará en: {html_report}")

        elif format_type == "json":
            report_dir = self.generate_timestamp_report_dir()
            json_report = report_dir / "report.json"
            args.extend(["--format", "json", "--outfile", str(json_report)])
            logger.info(f"📄 Reporte JSON se generará en: {json_report}")

        elif format_type == "junit":
            report_dir = self.generate_timestamp_report_dir()
            args.extend(["--junit", "--junit-directory", str(report_dir)])
            logger.info(f"📄 Reportes JUnit se generarán en: {report_dir}")

        else:
            # Formato por defecto (pretty)
            args.extend(["--format", "pretty"])

        return self.run_behave(args)


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Script de ejecución para pruebas de automatización - Zucarmex QA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python run_tests.py                                    # Ejecutar todas las pruebas
  python run_tests.py --feature alta_catalogo           # Ejecutar feature específico
  python run_tests.py --format html                     # Generar reporte HTML
  python run_tests.py --format json                     # Generar reporte JSON
  python run_tests.py --tags @smoke                     # Ejecutar solo tests con tag @smoke
  python run_tests.py --list-features                   # Listar features disponibles
  python run_tests.py --feature alta_catalogo --format html  # Feature específico con HTML
        """,
    )

    parser.add_argument(
        "--feature", help="Ejecutar un feature específico (ej: alta_catalogo)"
    )

    parser.add_argument(
        "--format",
        choices=["pretty", "html", "json", "junit"],
        default="pretty",
        help="Formato del reporte de salida",
    )

    parser.add_argument(
        "--tags", help="Ejecutar solo tests con tags específicos (ej: @smoke)"
    )

    parser.add_argument(
        "--list-features",
        action="store_true",
        help="Listar todos los features disponibles",
    )

    parser.add_argument(
        "--check-deps", action="store_true", help="Verificar dependencias"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Salida detallada")

    args = parser.parse_args()

    # Configurar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Crear runner
    runner = TestRunner()

    # Mostrar banner
    print("=" * 80)
    print("🏢 ZUCARMEX - Sistema de Automatización de Pruebas")
    print("🤖 Credicam QA - Automated Testing Framework")
    print("=" * 80)

    # Verificar dependencias si se solicita
    if args.check_deps:
        if runner.check_dependencies() and runner.check_config():
            logger.info("✅ Todas las verificaciones pasaron")
            return 0
        else:
            logger.error("❌ Algunas verificaciones fallaron")
            return 1

    # Listar features si se solicita
    if args.list_features:
        runner.list_features()
        return 0

    # Verificaciones previas
    if not runner.check_dependencies():
        return 1

    if not runner.check_config():
        return 1

    # Ejecutar pruebas
    try:
        return runner.run_with_format(
            format_type=args.format, feature_file=args.feature, tags=args.tags
        )
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Ejecución interrumpida por el usuario")
        return 130
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
