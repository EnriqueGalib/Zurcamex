"""
Steps específicos para la Alta de Zafra
Sistema de Automatización - Zucarmex QA

Nota: Los steps de autenticación se reutilizan de alta_catalogo_steps.py
"""

from datetime import datetime

from behave import given, then, when

from pages.alta_zafra_page import AltaZafraPage


@given("que el navegador está configurado correctamente para zafra")
def step_navegador_configurado_zafra(context):
    """Configura el navegador específicamente para pruebas de zafra"""
    # Usar el logger del context si está disponible, sino crear uno básico
    if not hasattr(context, "logger"):
        import logging

        context.logger = logging.getLogger(__name__)

    context.logger.info("Configurando navegador para zafra...")

    try:
        # El driver ya está configurado en environment.py
        # Solo necesitamos inicializar la página específica para zafra
        if hasattr(context, "driver"):
            context.alta_zafra_page = AltaZafraPage(context.driver)

            # Configurar carpeta de ejecución específica para este escenario
            feature_name = "alta_zafra"
            scenario_name = "Autenticación completa con OKTA para Alta de Zafra"
            execution_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            context.alta_zafra_page.set_execution_folder(
                feature_name, scenario_name, execution_timestamp
            )

            context.logger.info(
                "✅ Navegador configurado para zafra, inicializando página"
            )
            context.logger.info(
                f"📁 Evidencias se guardarán en: {context.alta_zafra_page.execution_folder}"
            )
        else:
            context.logger.error("❌ Driver no encontrado en context")
            raise AssertionError("Driver no configurado en environment")

    except Exception as e:
        context.logger.error(f"❌ Error configurando navegador para zafra: {e}")
        raise


@when("el usuario hace clic en Configuración")
def step_usuario_hace_clic_configuracion(context):
    """Hace clic en el menú Configuración"""
    context.logger.info("Haciendo clic en Configuración...")

    try:
        # Hacer clic en Configuración
        resultado = context.alta_zafra_page.hacer_clic_configuracion()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en Configuración")
            raise AssertionError("Error al hacer clic en Configuración")

        context.logger.info("✅ Clic en Configuración realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en Configuración: {e}")
        raise


@when("el usuario hace clic en Zafras")
def step_usuario_hace_clic_zafras(context):
    """Hace clic en el submenú Zafras"""
    context.logger.info("Haciendo clic en Zafras...")

    try:
        # Hacer clic en Zafras
        resultado = context.alta_zafra_page.hacer_clic_zafras()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en Zafras")
            raise AssertionError("Error al hacer clic en Zafras")

        context.logger.info("✅ Clic en Zafras realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en Zafras: {e}")
        raise


@when("el usuario hace clic en Nueva zafra")
def step_usuario_hace_clic_nueva_zafra(context):
    """Hace clic en el botón Nueva zafra"""
    context.logger.info("Haciendo clic en Nueva zafra...")

    try:
        # Hacer clic en Nueva zafra
        resultado = context.alta_zafra_page.hacer_clic_nueva_zafra()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en Nueva zafra")
            raise AssertionError("Error al hacer clic en Nueva zafra")

        context.logger.info("✅ Clic en Nueva zafra realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en Nueva zafra: {e}")
        raise


# El environment.py ya maneja la limpieza del navegador
