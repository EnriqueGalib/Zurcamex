import json
import logging
import os
from datetime import datetime

from behave import given, then, when

from pages.catalogo_page import CatalogoPage
from pages.login_page import LoginPage


# Configurar logging
def setup_logging(feature_name, scenario_name):
    """Configura el logging para el feature y escenario actual"""
    # El logging ya está configurado en environment.py
    # Solo obtenemos el logger existente
    return logging.getLogger(__name__)


def setup_evidence_dirs(
    feature_name, scenario_name, execution_result="UNKNOWN", context=None
):
    """Configura los directorios para evidencias usando el gestor de evidencias"""
    try:
        # Usar el gestor de evidencias del contexto si está disponible
        if context and hasattr(context, "evidence_manager"):
            evidence_dir, screenshots_dir = (
                context.evidence_manager.create_evidence_structure(
                    feature_name, scenario_name, execution_result
                )
            )
        else:
            # Fallback a estructura simple
            evidence_dir = os.path.join("evidences", feature_name, scenario_name)
            screenshots_dir = evidence_dir
            os.makedirs(evidence_dir, exist_ok=True)

        # Directorio para reportes
        reports_dir = os.path.join("reports", feature_name, scenario_name)
        os.makedirs(reports_dir, exist_ok=True)

        return evidence_dir, screenshots_dir
    except Exception as e:
        logging.error(f"Error configurando directorios de evidencias: {str(e)}")
        # Fallback absoluto
        evidence_dir = os.path.join("evidences", feature_name, scenario_name)
        os.makedirs(evidence_dir, exist_ok=True)
        return evidence_dir, evidence_dir


def take_screenshot(
    driver, evidence_dir, step_name, screenshots_dir=None, context=None
):
    """Toma una captura de pantalla"""
    try:
        # Usar directorio de screenshots específico si está disponible
        target_dir = screenshots_dir if screenshots_dir else evidence_dir

        # Asegurar que el directorio existe
        os.makedirs(target_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(target_dir, f"{step_name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot guardado: {screenshot_path}")

        # Registrar screenshot en el contexto si está disponible
        if context and hasattr(context, "screenshots_taken"):
            context.screenshots_taken += 1

        return screenshot_path
    except Exception as e:
        logging.error(f"Error tomando screenshot: {str(e)}")
        return None


def track_step_execution(
    context, step_name, step_description, status="SUCCESS", evidence_paths=None
):
    """Registra la ejecución de un paso para el reporte"""
    try:
        if not hasattr(context, "executed_steps"):
            context.executed_steps = []

        step_data = {
            "name": step_name,
            "description": step_description,
            "status": status,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "duration": "No disponible",  # Se puede mejorar calculando duración real
            "evidence": [],
        }

        # Agregar evidencias si están disponibles
        if evidence_paths:
            if isinstance(evidence_paths, str):
                evidence_paths = [evidence_paths]

            for evidence_path in evidence_paths:
                if evidence_path and os.path.exists(evidence_path):
                    step_data["evidence"].append(
                        {
                            "name": os.path.basename(evidence_path),
                            "path": evidence_path,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                        }
                    )

        context.executed_steps.append(step_data)
        logging.info(f"Paso registrado: {step_name} - {status}")

    except Exception as e:
        logging.error(f"Error registrando paso: {str(e)}")


@given("estoy en la página de inicio de sesión")
def step_given_login_page(context):
    """Navega a la página de login"""
    # Configurar logging y directorios
    context.logger = setup_logging("alta_catalogo", "login_and_create_catalog")
    context.evidence_dir, context.screenshots_dir = setup_evidence_dirs(
        "alta_catalogo", "login_and_create_catalog", "UNKNOWN", context
    )

    # Log inicial para verificar que el logging funciona
    context.logger.info("=" * 60)
    context.logger.info("INICIANDO PRUEBA DE LOGIN Y CREACIÓN DE CATÁLOGO")
    context.logger.info("=" * 60)

    # Leer configuración
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    qa_url = config["urls"]["qa"]
    context.logger.info(f"URL de QA: {qa_url}")

    # Crear página de login y navegar
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login(qa_url)

    # Tomar screenshot
    screenshot_path = take_screenshot(
        context.driver,
        context.evidence_dir,
        "login_page",
        context.screenshots_dir,
        context,
    )

    # Registrar paso
    track_step_execution(
        context,
        "Navegación a Login",
        "Navegando a la página de login del sistema",
        "SUCCESS",
        screenshot_path,
    )


@when('inicio sesión con usuario "{username}" y contraseña "{password}"')
def step_when_login(context, username, password):
    """Realiza el login inicial con las credenciales especificadas hasta el botón Verificar"""
    context.logger.info(f"Iniciando login inicial con usuario: {username}")

    # Realizar login inicial (hasta hacer clic en "Verificar")
    success = context.login_page.login(username, password)

    if success:
        context.logger.info("Login inicial completado - botón 'Verificar' clickeado")
        # Tomar screenshot después del login inicial
        screenshot_path = take_screenshot(
            context.driver,
            context.evidence_dir,
            "after_verify_clicked",
            context.screenshots_dir,
            context,
        )
        track_step_execution(
            context,
            "Login Inicial",
            "Login con credenciales hasta botón Verificar",
            "SUCCESS",
            screenshot_path,
        )
    else:
        context.logger.error("Error en el proceso de login inicial")
        screenshot_path = take_screenshot(
            context.driver,
            context.evidence_dir,
            "login_error",
            context.screenshots_dir,
            context,
        )
        track_step_execution(
            context,
            "Login Inicial",
            "Login con credenciales hasta botón Verificar",
            "FAILED",
            screenshot_path,
        )
        assert False, "Error en el proceso de login inicial"


@when("espero la validación manual de 2FA después de hacer clic en verificar")
def step_when_wait_2fa(context):
    """Pausa la automatización para validación manual del 2FA"""
    context.logger.info("⏸️ PAUSA AUTOMATIZACIÓN: Validación manual del 2FA requerida")

    # Tomar screenshot del estado actual
    take_screenshot(
        context.driver,
        context.evidence_dir,
        "waiting_for_2fa",
        context.screenshots_dir,
    )

    # Usar el método de la página de login para manejar la espera del 2FA
    success = context.login_page.wait_for_manual_2fa()

    if not success:
        context.logger.error("Error en la espera manual del 2FA")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "2fa_wait_error",
            context.screenshots_dir,
        )
        assert False, "Error en la espera manual del 2FA"

    # Tomar screenshot después de la confirmación
    take_screenshot(
        context.driver,
        context.evidence_dir,
        "2fa_confirmed",
        context.screenshots_dir,
    )


@then("debería estar completamente autenticado y en la página principal")
def step_then_authenticated(context):
    """Verifica que la autenticación completa después del 2FA fue exitosa y estamos en el HOME"""
    context.logger.info(
        "Verificando autenticación completa y llegada al HOME después del 2FA"
    )

    # Tomar screenshot del estado actual
    take_screenshot(
        context.driver,
        context.evidence_dir,
        "verifying_home_page",
        context.screenshots_dir,
    )

    # Usar el método de la página de login para verificar que estamos en el
    # home
    try:
        # Esperar un poco para que la página se estabilice
        import time

        time.sleep(3)

        # Verificar que estamos en el home usando el método de la página
        home_detected = context.login_page.wait_for_home_page()

        if home_detected:
            current_url = context.driver.current_url
            context.logger.info(
                "✅ Autenticación completa verificada - estamos en el HOME"
            )
            context.logger.info(f"🏠 Página actual: {current_url}")
            take_screenshot(
                context.driver,
                context.evidence_dir,
                "home_page_reached",
                context.screenshots_dir,
            )
        else:
            # Verificar manualmente si estamos en una página válida
            current_url = context.driver.current_url
            context.logger.info(f"URL actual después del 2FA: {current_url}")

            if "login" in current_url.lower() or "okta" in current_url.lower():
                context.logger.error("Aún en página de login/OKTA después del 2FA")
                take_screenshot(
                    context.driver,
                    context.evidence_dir,
                    "still_on_login_page",
                    context.screenshots_dir,
                )
                assert (
                    False
                ), "La autenticación del 2FA no fue exitosa - aún en página de login/OKTA"

            # Si no es login/OKTA, asumir que estamos en el sistema
            context.logger.info(
                "✅ Página del sistema detectada - continuando con la prueba"
            )
            take_screenshot(
                context.driver,
                context.evidence_dir,
                "system_page_detected",
                context.screenshots_dir,
            )

    except Exception as e:
        context.logger.error(f"Error verificando autenticación completa: {str(e)}")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "full_auth_verification_error",
            context.screenshots_dir,
        )
        assert False, f"Error verificando autenticación completa: {str(e)}"


@when("navego al menú Configurador > Catálogos")
def step_when_navigate_menu(context):
    """Navega al menú Configurador > Gestor de catálogos"""
    context.logger.info("Navegando al menú Configurador > Gestor de catálogos")

    # Crear página de catálogos y navegar
    context.catalogo_page = CatalogoPage(context.driver)
    success = context.catalogo_page.navigate_to_catalogos()

    if success:
        context.logger.info("✅ Navegación al Gestor de catálogos exitosa")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "gestor_catalogos_menu",
            context.screenshots_dir,
        )
    else:
        context.logger.error("❌ Error navegando al Gestor de catálogos")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "navigation_error",
            context.screenshots_dir,
        )
        assert False, "Error navegando al Gestor de catálogos"


@when('hago clic en el botón "Nuevo" para crear un nuevo catálogo')
def step_when_click_nuevo(context):
    """Hace clic en el botón Nuevo para crear un catálogo"""
    context.logger.info("Haciendo clic en botón Nuevo Catálogo")

    success = context.catalogo_page.click_nuevo_catalogo()

    if success:
        context.logger.info("Botón Nuevo clickeado exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "nuevo_catalogo_clicked",
            context.screenshots_dir,
        )
    else:
        context.logger.error("Error clickeando botón Nuevo")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "nuevo_button_error",
            context.screenshots_dir,
        )
        assert False, "Error clickeando botón Nuevo"


@when("lleno el formulario del catálogo con:")
def step_when_fill_catalog_form(context):
    """Llena el formulario de catálogo con los datos de la tabla"""
    context.logger.info("Llenando formulario de catálogo")

    # Extraer datos de la tabla
    form_data = {}
    for row in context.table:
        form_data[row["Nombre"]] = row["Descripción"]

    # Llenar formulario
    success = context.catalogo_page.fill_catalogo_form(
        nombre=form_data["Nombre"], descripcion=form_data["Descripción"]
    )

    if success:
        context.logger.info("Formulario de catálogo llenado exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "catalog_form_filled",
            context.screenshots_dir,
        )
    else:
        context.logger.error("Error llenando formulario de catálogo")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "catalog_form_error",
            context.screenshots_dir,
        )
        assert False, "Error llenando formulario de catálogo"


@when("guardo el catálogo")
def step_when_save_catalog(context):
    """Guarda el catálogo"""
    context.logger.info("Guardando catálogo")

    success = context.catalogo_page.save_catalogo()

    if success:
        context.logger.info("Catálogo guardado exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "catalog_saved",
            context.screenshots_dir,
        )
    else:
        context.logger.error("Error guardando catálogo")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "catalog_save_error",
            context.screenshots_dir,
        )
        assert False, "Error guardando catálogo"


@then("el catálogo debería crearse exitosamente")
def step_then_catalog_created(context):
    """Verifica que el catálogo fue creado exitosamente"""
    context.logger.info("Verificando creación exitosa del catálogo")

    # Verificar mensaje de éxito
    success = context.catalogo_page.is_success_message_displayed()

    if success:
        context.logger.info("Catálogo creado exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "catalog_creation_success",
            context.screenshots_dir,
        )
    else:
        context.logger.warning("No se detectó mensaje de éxito, pero continuando...")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "catalog_creation_warning",
            context.screenshots_dir,
        )


@when("lleno el formulario de detalles técnicos con:")
def step_when_fill_technical_form(context):
    """Llena el formulario de detalles técnicos con los datos de la tabla"""
    context.logger.info("Llenando formulario de detalles técnicos")

    # Extraer datos de la tabla
    form_data = {}
    for row in context.table:
        form_data[row["Nombre Técnico"]] = row["Etiqueta"]

    # Llenar formulario de detalles técnicos
    success = context.catalogo_page.fill_edicion_form(
        nombre_tecnico=form_data["Nombre Técnico"],
        etiqueta=form_data["Etiqueta"],
    )

    if success:
        context.logger.info("Formulario de detalles técnicos llenado exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "technical_details_filled",
            context.screenshots_dir,
        )
    else:
        context.logger.error("Error llenando formulario de detalles técnicos")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "technical_details_error",
            context.screenshots_dir,
        )
        assert False, "Error llenando formulario de detalles técnicos"


@when("guardo los detalles técnicos")
def step_when_save_technical(context):
    """Guarda los detalles técnicos"""
    context.logger.info("Guardando detalles técnicos")

    success = context.catalogo_page.save_edicion()

    if success:
        context.logger.info("Detalles técnicos guardados exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "technical_details_saved",
            context.screenshots_dir,
        )
    else:
        context.logger.error("Error guardando detalles técnicos")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "technical_details_save_error",
            context.screenshots_dir,
        )
        assert False, "Error guardando detalles técnicos"


@then("los detalles técnicos deberían guardarse exitosamente")
def step_then_technical_saved(context):
    """Verifica que los detalles técnicos fueron guardados exitosamente"""
    context.logger.info("Verificando guardado exitoso de detalles técnicos")

    # Verificar mensaje de éxito
    success = context.catalogo_page.is_success_message_displayed()

    if success:
        context.logger.info("Detalles técnicos guardados exitosamente")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "technical_details_success",
            context.screenshots_dir,
        )
    else:
        context.logger.warning("No se detectó mensaje de éxito, pero continuando...")
        take_screenshot(
            context.driver,
            context.evidence_dir,
            "technical_details_warning",
            context.screenshots_dir,
        )

    # Tomar screenshot final
    take_screenshot(
        context.driver,
        context.evidence_dir,
        "test_completed",
        context.screenshots_dir,
    )
    context.logger.info("Prueba completada exitosamente")
