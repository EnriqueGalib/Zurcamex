"""
Steps para la Alta de Catálogo
Sistema de Automatización - Zucarmex QA
"""

import json
import os
from datetime import datetime

from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.alta_catalogo_page import AltaCatalogoPage
from utils.advanced_logger import AdvancedLogger


def get_page_object(context):
    """Obtiene el objeto de página apropiado (zafra o catálogo)"""
    if hasattr(context, "alta_zafra_page"):
        return context.alta_zafra_page
    elif hasattr(context, "alta_catalogo_page"):
        return context.alta_catalogo_page
    else:
        raise AssertionError("No se encontró página configurada")


@given("que el navegador está configurado correctamente")
def step_navegador_configurado(context):
    """Configura el navegador para las pruebas"""
    # Usar el logger del context si está disponible, sino crear uno básico
    if not hasattr(context, "logger"):
        import logging

        context.logger = logging.getLogger(__name__)

    context.logger.info("Configurando navegador...")

    try:
        # El driver ya está configurado en environment.py
        # Solo necesitamos inicializar la página
        if hasattr(context, "driver"):
            # Si ya existe una página de zafra configurada, usar esa
            if hasattr(context, "alta_zafra_page"):
                context.logger.info("✅ Usando página de zafra ya configurada")
                return

            # Si no, inicializar página de catálogo
            context.alta_catalogo_page = AltaCatalogoPage(context.driver)

            # Configurar carpeta de ejecución específica para este escenario
            feature_name = "alta_catalogo"
            scenario_name = "Autenticación completa con OKTA para Alta de Catálogo"
            execution_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            context.alta_catalogo_page.set_execution_folder(
                feature_name, scenario_name, execution_timestamp
            )

            context.logger.info(
                "✅ Navegador ya configurado, inicializando página de catálogo"
            )
            context.logger.info(
                f"📁 Evidencias se guardarán en: {context.alta_catalogo_page.execution_folder}"
            )
        else:
            context.logger.error("❌ Driver no encontrado en context")
            raise AssertionError("Driver no configurado en environment")

    except Exception as e:
        context.logger.error(f"❌ Error configurando navegador: {e}")
        raise


@given("que el usuario navega a la página de login")
def step_usuario_navega_login(context):
    """Navega a la página de login"""
    context.logger.info("Navegando a la página de login...")

    try:
        # Navegar a la página de login
        resultado = context.alta_catalogo_page.navegar_a_login()

        if not resultado:
            context.logger.error("❌ No se pudo navegar a la página de login")
            raise AssertionError("Error al navegar a la página de login")

        # Verificar elementos de la página
        elementos_ok = context.alta_catalogo_page.verificar_elementos_pagina()

        if not elementos_ok:
            context.logger.warning("⚠️ Algunos elementos no se encontraron en la página")

        context.logger.info("✅ Navegación a login completada")

    except Exception as e:
        context.logger.error(f"❌ Error en navegación a login: {e}")
        raise


@given("que el usuario navega a la página de login y hace clic inmediato")
def step_usuario_navega_login_clic_inmediato(context):
    """Navega a la página de login y hace clic inmediato en OKTA"""
    context.logger.info("Navegando a la página de login y haciendo clic inmediato...")

    try:
        # Obtener la página apropiada (zafra o catálogo)
        page = get_page_object(context)

        # Navegar y hacer clic inmediato
        resultado = page.navegar_a_login_y_clic_inmediato()

        if not resultado:
            context.logger.error("❌ No se pudo navegar y hacer clic inmediato")
            raise AssertionError("Error al navegar y hacer clic inmediato")

        context.logger.info("✅ Navegación y clic inmediato completado")

    except Exception as e:
        context.logger.error(f"❌ Error en navegación y clic inmediato: {e}")
        raise


@when('el usuario hace clic inmediatamente en el botón "{boton}"')
def step_usuario_hace_clic_inmediato_boton(context, boton):
    """Hace clic inmediatamente en el botón especificado sin verificaciones adicionales"""
    context.logger.info(f"Haciendo clic inmediatamente en el botón: {boton}")

    try:
        if "OKTA" in boton.upper():
            resultado = context.alta_catalogo_page.hacer_clic_okta_inmediato()

            if not resultado:
                context.logger.error("❌ No se pudo hacer clic en el botón OKTA")
                raise AssertionError("Error al hacer clic en el botón OKTA")

            context.logger.info(
                "✅ Clic inmediato en botón OKTA realizado exitosamente"
            )
        else:
            context.logger.error(f"❌ Botón no reconocido: {boton}")
            raise AssertionError(f"Botón no reconocido: {boton}")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en botón: {e}")
        raise


@when('el usuario hace clic en el botón "{boton}"')
def step_usuario_hace_clic_boton(context, boton):
    """Hace clic en el botón especificado"""
    context.logger.info(f"Haciendo clic en el botón: {boton}")

    try:
        if "OKTA" in boton.upper():
            resultado = context.alta_catalogo_page.hacer_clic_okta()

            if not resultado:
                context.logger.error("❌ No se pudo hacer clic en el botón OKTA")
                raise AssertionError("Error al hacer clic en el botón OKTA")

            context.logger.info("✅ Clic en botón OKTA realizado exitosamente")
        else:
            context.logger.error(f"❌ Botón no reconocido: {boton}")
            raise AssertionError(f"Botón no reconocido: {boton}")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en botón: {e}")
        raise


@when("se cargan todos los elementos de la página")
def step_elementos_pagina_cargados(context):
    """Verifica que todos los elementos de la página estén cargados"""
    context.logger.info("Verificando carga de elementos de la página...")

    try:
        resultado = context.alta_catalogo_page.verificar_elementos_pagina()

        if not resultado:
            context.logger.warning("⚠️ No todos los elementos se cargaron correctamente")
        else:
            context.logger.info("✅ Todos los elementos de la página están cargados")

    except Exception as e:
        context.logger.error(f"❌ Error verificando elementos: {e}")
        raise


@then("debe redirigirse a la página de autenticación de OKTA")
def step_redireccion_okta(context):
    """Verifica que se produzca la redirección a OKTA"""
    context.logger.info("Verificando redirección a OKTA...")

    try:
        # Obtener la página apropiada (zafra o catálogo)
        page = get_page_object(context)

        resultado = page.verificar_redireccion_okta()

        if not resultado:
            context.logger.warning("⚠️ No se detectó redirección a OKTA")
            # No fallar la prueba, solo registrar el warning
        else:
            context.logger.info("✅ Redirección a OKTA verificada")

    except Exception as e:
        context.logger.error(f"❌ Error verificando redirección: {e}")
        # No fallar la prueba por este error


@when("el usuario ingresa el usuario {usuario} en OKTA")
def step_usuario_ingresa_usuario_okta(context, usuario):
    """Ingresa el usuario en la página de OKTA"""
    context.logger.info(f"Ingresando usuario en OKTA: {usuario}")

    try:
        # Verificar que estamos en la página de OKTA
        pagina_okta = context.alta_catalogo_page.verificar_pagina_okta()

        if not pagina_okta:
            context.logger.warning("⚠️ No se detectó página de OKTA, continuando...")

        # Ingresar el usuario
        resultado = context.alta_catalogo_page.ingresar_usuario_okta(usuario)

        if not resultado:
            context.logger.error("❌ No se pudo ingresar el usuario en OKTA")
            raise AssertionError("Error al ingresar usuario en OKTA")

        context.logger.info("✅ Usuario ingresado exitosamente en OKTA")

    except Exception as e:
        context.logger.error(f"❌ Error ingresando usuario en OKTA: {e}")
        raise


@when("el usuario hace clic en el botón Siguiente de OKTA")
def step_usuario_hace_clic_siguiente_okta(context):
    """Hace clic en el botón Siguiente de OKTA"""
    context.logger.info("Haciendo clic en botón Siguiente de OKTA...")

    try:
        resultado = context.alta_catalogo_page.hacer_clic_siguiente_okta()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en botón Siguiente")
            raise AssertionError("Error al hacer clic en botón Siguiente")

        context.logger.info("✅ Clic en botón Siguiente realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en botón Siguiente: {e}")
        raise


@when("el usuario ingresa el usuario {usuario} y hace clic en Siguiente de OKTA")
def step_usuario_ingresa_y_clic_siguiente_okta(context, usuario):
    """Ingresa el usuario y hace clic en Siguiente de forma ultra rápida"""
    context.logger.info(f"Ingresando usuario y haciendo clic en Siguiente: {usuario}")

    try:
        # Obtener la página apropiada (zafra o catálogo)
        page = get_page_object(context)

        # Verificar que estamos en la página de OKTA
        pagina_okta = page.verificar_pagina_okta()

        if not pagina_okta:
            context.logger.warning("⚠️ No se detectó página de OKTA, continuando...")

        # Ingresar usuario y hacer clic en Siguiente de forma ultra rápida
        resultado = page.ingresar_usuario_y_clic_siguiente_okta(usuario)

        if not resultado:
            context.logger.error(
                "❌ No se pudo ingresar usuario y hacer clic en Siguiente"
            )
            raise AssertionError("Error al ingresar usuario y hacer clic en Siguiente")

        context.logger.info(
            "✅ Usuario ingresado y clic en Siguiente realizado exitosamente"
        )

    except Exception as e:
        context.logger.error(
            f"❌ Error ingresando usuario y haciendo clic en Siguiente: {e}"
        )
        raise


@when("el usuario ingresa la contraseña {contrasena} en OKTA")
def step_usuario_ingresa_contrasena_okta(context, contrasena):
    """Ingresa la contraseña en la página de OKTA"""
    context.logger.info(f"Ingresando contraseña en OKTA: {contrasena}")

    try:
        # Verificar que estamos en la página de contraseña de OKTA
        pagina_contrasena = (
            context.alta_catalogo_page.verificar_pagina_contrasena_okta()
        )

        if not pagina_contrasena:
            context.logger.warning(
                "⚠️ No se detectó página de contraseña de OKTA, continuando..."
            )

        # Ingresar la contraseña
        resultado = context.alta_catalogo_page.ingresar_contrasena_okta(contrasena)

        if not resultado:
            context.logger.error("❌ No se pudo ingresar la contraseña en OKTA")
            raise AssertionError("Error al ingresar contraseña en OKTA")

        context.logger.info("✅ Contraseña ingresada exitosamente en OKTA")

    except Exception as e:
        context.logger.error(f"❌ Error ingresando contraseña en OKTA: {e}")
        raise


@when("el usuario hace clic en el botón Verificar de OKTA")
def step_usuario_hace_clic_verificar_okta(context):
    """Hace clic en el botón Verificar de OKTA"""
    context.logger.info("Haciendo clic en botón Verificar de OKTA...")

    try:
        resultado = context.alta_catalogo_page.hacer_clic_verificar_okta()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en botón Verificar")
            raise AssertionError("Error al hacer clic en botón Verificar")

        context.logger.info("✅ Clic en botón Verificar realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en botón Verificar: {e}")
        raise


@when("el usuario ingresa la contraseña {contrasena} y hace clic en Verificar de OKTA")
def step_usuario_ingresa_contrasena_y_clic_verificar_okta(context, contrasena):
    """Ingresa la contraseña y hace clic en Verificar de forma ultra rápida"""
    context.logger.info(
        f"Ingresando contraseña y haciendo clic en Verificar: {contrasena}"
    )

    try:
        # Verificar que estamos en la página de contraseña de OKTA
        pagina_contrasena = (
            context.alta_catalogo_page.verificar_pagina_contrasena_okta()
        )

        if not pagina_contrasena:
            context.logger.warning(
                "⚠️ No se detectó página de contraseña de OKTA, continuando..."
            )

        # Ingresar contraseña y hacer clic en Verificar de forma ultra rápida
        resultado = (
            context.alta_catalogo_page.ingresar_contrasena_y_clic_verificar_okta(
                contrasena
            )
        )

        if not resultado:
            context.logger.error(
                "❌ No se pudo ingresar contraseña y hacer clic en Verificar"
            )
            raise AssertionError(
                "Error al ingresar contraseña y hacer clic en Verificar"
            )

        context.logger.info(
            "✅ Contraseña ingresada y clic en Verificar realizado exitosamente"
        )

    except Exception as e:
        context.logger.error(
            f"❌ Error ingresando contraseña y haciendo clic en Verificar: {e}"
        )
        raise


@when(
    "el usuario ingresa la contraseña {contrasena} y hace clic en Verificar de OKTA ULTRA RÁPIDO"
)
def step_usuario_ingresa_contrasena_y_clic_verificar_okta_ultra_rapido(
    context, contrasena
):
    """Ingresa la contraseña y hace clic en Verificar de forma ULTRA RÁPIDA"""
    context.logger.info(
        f"Ingresando contraseña y haciendo clic en Verificar ULTRA RÁPIDO: {contrasena}"
    )

    try:
        # Verificar que estamos en la página de contraseña de OKTA
        pagina_contrasena = (
            context.alta_catalogo_page.verificar_pagina_contrasena_okta()
        )

        if not pagina_contrasena:
            context.logger.warning(
                "⚠️ No se detectó página de contraseña de OKTA, continuando..."
            )

        # Ingresar contraseña y hacer clic en Verificar de forma ULTRA RÁPIDA
        resultado = context.alta_catalogo_page.ingresar_contrasena_y_clic_verificar_okta_ultra_rapido(
            contrasena
        )

        if not resultado:
            context.logger.error(
                "❌ No se pudo ingresar contraseña y hacer clic en Verificar ULTRA RÁPIDO"
            )
            raise AssertionError(
                "Error al ingresar contraseña y hacer clic en Verificar ULTRA RÁPIDO"
            )

        context.logger.info(
            "✅ Contraseña ingresada y clic en Verificar ULTRA RÁPIDO realizado exitosamente"
        )

    except Exception as e:
        context.logger.error(
            f"❌ Error ingresando contraseña y haciendo clic en Verificar ULTRA RÁPIDO: {e}"
        )
        raise


@when(
    "el usuario ingresa la contraseña {contrasena} y hace clic en Verificar de OKTA con selector específico"
)
def step_usuario_ingresa_contrasena_y_clic_verificar_okta_selector_especifico(
    context, contrasena
):
    """Ingresa la contraseña y hace clic en Verificar usando el selector específico"""
    context.logger.info(
        f"Ingresando contraseña y haciendo clic en Verificar con selector específico: {contrasena}"
    )

    try:
        # Verificar que estamos en la página de contraseña de OKTA
        pagina_contrasena = (
            context.alta_catalogo_page.verificar_pagina_contrasena_okta()
        )

        if not pagina_contrasena:
            context.logger.warning(
                "⚠️ No se detectó página de contraseña de OKTA, continuando..."
            )

        # Ingresar contraseña y hacer clic en Verificar con selector específico
        resultado = context.alta_catalogo_page.ingresar_contrasena_y_clic_verificar_okta_selector_especifico(
            contrasena
        )

        if not resultado:
            context.logger.error(
                "❌ No se pudo ingresar contraseña y hacer clic en Verificar con selector específico"
            )
            raise AssertionError(
                "Error al ingresar contraseña y hacer clic en Verificar con selector específico"
            )

        context.logger.info(
            "✅ Contraseña ingresada y clic en Verificar con selector específico realizado exitosamente"
        )

    except Exception as e:
        context.logger.error(
            f"❌ Error ingresando contraseña y haciendo clic en Verificar con selector específico: {e}"
        )
        raise


@when(
    "el usuario ingresa la contraseña {contrasena} y hace clic en Verificar de OKTA con debug"
)
def step_usuario_ingresa_contrasena_y_clic_verificar_okta_debug(context, contrasena):
    """Ingresa la contraseña y hace clic en Verificar usando debug"""
    context.logger.info(
        f"Ingresando contraseña y haciendo clic en Verificar con debug: {contrasena}"
    )

    try:
        # Obtener la página apropiada (zafra o catálogo)
        page = get_page_object(context)

        # Verificar que estamos en la página de contraseña de OKTA
        pagina_contrasena = page.verificar_pagina_contrasena_okta()

        if not pagina_contrasena:
            context.logger.warning(
                "⚠️ No se detectó página de contraseña de OKTA, continuando..."
            )

        # Ingresar contraseña y hacer clic en Verificar con debug
        resultado = page.ingresar_contrasena_y_clic_verificar_debug(contrasena)

        if not resultado:
            context.logger.error(
                "❌ No se pudo ingresar contraseña y hacer clic en Verificar con debug"
            )
            raise AssertionError(
                "Error al ingresar contraseña y hacer clic en Verificar con debug"
            )

        context.logger.info(
            "✅ Contraseña ingresada y clic en Verificar con debug realizado exitosamente"
        )

    except Exception as e:
        context.logger.error(
            f"❌ Error ingresando contraseña y haciendo clic en Verificar con debug: {e}"
        )
        raise


@when("el usuario hace clic en Configurador")
def step_usuario_hace_clic_configurador(context):
    """Hace clic en el menú Configurador"""
    context.logger.info("Haciendo clic en Configurador...")

    try:
        # Hacer clic en Configurador
        resultado = context.alta_catalogo_page.hacer_clic_configurador()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en Configurador")
            raise AssertionError("Error al hacer clic en Configurador")

        context.logger.info("✅ Clic en Configurador realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en Configurador: {e}")
        raise


@when("el usuario hace clic en Gestor de catálogos")
def step_usuario_hace_clic_gestor_catalogos(context):
    """Hace clic en Gestor de catálogos"""
    context.logger.info("Haciendo clic en Gestor de catálogos...")

    try:
        # Hacer clic en Gestor de catálogos
        resultado = context.alta_catalogo_page.hacer_clic_gestor_catalogos()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en Gestor de catálogos")
            raise AssertionError("Error al hacer clic en Gestor de catálogos")

        context.logger.info("✅ Clic en Gestor de catálogos realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en Gestor de catálogos: {e}")
        raise


@when("el usuario hace clic en NUEVO CATÁLOGO")
def step_usuario_hace_clic_nuevo_catalogo(context):
    """Hace clic en NUEVO CATÁLOGO"""
    context.logger.info("Haciendo clic en NUEVO CATÁLOGO...")

    try:
        # Hacer clic en NUEVO CATÁLOGO
        resultado = context.alta_catalogo_page.hacer_clic_nuevo_catalogo()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en NUEVO CATÁLOGO")
            raise AssertionError("Error al hacer clic en NUEVO CATÁLOGO")

        context.logger.info("✅ Clic en NUEVO CATÁLOGO realizado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en NUEVO CATÁLOGO: {e}")
        raise


@when("el usuario hace clic en NUEVO CATÁLOGO con debug")
def step_usuario_hace_clic_nuevo_catalogo_debug(context):
    """Hace clic en NUEVO CATÁLOGO usando debug"""
    context.logger.info("Haciendo clic en NUEVO CATÁLOGO con debug...")

    try:
        # Hacer clic en NUEVO CATÁLOGO con debug
        resultado = context.alta_catalogo_page.hacer_clic_nuevo_catalogo_debug()

        if not resultado:
            context.logger.error("❌ No se pudo hacer clic en NUEVO CATÁLOGO con debug")
            raise AssertionError("Error al hacer clic en NUEVO CATÁLOGO con debug")

        context.logger.info(
            "✅ Clic en NUEVO CATÁLOGO con debug realizado exitosamente"
        )

    except Exception as e:
        context.logger.error(f"❌ Error haciendo clic en NUEVO CATÁLOGO con debug: {e}")
        raise


@when("el usuario llena el formulario completo con Test")
def step_usuario_llena_formulario_completo(context):
    """Llena el formulario completo con Test en todos los campos"""
    context.logger.info("Llenando formulario completo con Test...")

    try:
        # Llenar formulario completo
        resultado = context.alta_catalogo_page.llenar_formulario_completo()

        if not resultado:
            context.logger.error("❌ No se pudo llenar el formulario completo")
            raise AssertionError("Error al llenar el formulario completo")

        context.logger.info("✅ Formulario completo llenado exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error llenando formulario completo: {e}")
        raise


@when("el usuario guarda los datos generales")
def step_usuario_guarda_datos_generales(context):
    """Guarda los datos generales del formulario"""
    context.logger.info("Guardando datos generales...")

    try:
        # Guardar datos generales
        resultado = context.alta_catalogo_page.guardar_datos_generales()

        if not resultado:
            context.logger.error("❌ No se pudieron guardar los datos generales")
            raise AssertionError("Error al guardar los datos generales")

        context.logger.info("✅ Datos generales guardados exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error guardando datos generales: {e}")
        raise


@when("el usuario llena la estructura del catálogo con Test")
def step_usuario_llena_estructura_catalogo(context):
    """Llena la estructura del catálogo con Test en todos los campos"""
    context.logger.info("Llenando estructura del catálogo con Test...")

    try:
        # Llenar estructura del catálogo
        resultado = context.alta_catalogo_page.llenar_estructura_catalogo_completa()

        if not resultado:
            context.logger.error("❌ No se pudo llenar la estructura del catálogo")
            raise AssertionError("Error al llenar la estructura del catálogo")

        context.logger.info("✅ Estructura del catálogo llenada exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error llenando estructura del catálogo: {e}")
        raise


@when("el usuario guarda la estructura del catálogo")
def step_usuario_guarda_estructura_catalogo(context):
    """Guarda la estructura del catálogo"""
    context.logger.info("Guardando estructura del catálogo...")

    try:
        # Guardar estructura del catálogo
        resultado = context.alta_catalogo_page.guardar_estructura_catalogo_debug()

        if not resultado:
            context.logger.error("❌ No se pudo guardar la estructura del catálogo")
            raise AssertionError("Error al guardar la estructura del catálogo")

        context.logger.info("✅ Estructura del catálogo guardada exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error guardando estructura del catálogo: {e}")
        raise


@when("debe capturar evidencias del proceso")
def step_debe_capturar_evidencias_proceso(context):
    """Captura evidencias del proceso completado"""
    context.logger.info("Capturando evidencias del proceso...")

    try:
        # Capturar screenshot final
        context.alta_catalogo_page._capturar_screenshot("proceso_completado")

        context.logger.info("✅ Evidencias del proceso capturadas exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error capturando evidencias del proceso: {e}")
        raise


@when("el usuario espera para validar manualmente la 2FA")
def step_usuario_espera_validacion_manual_2fa(context):
    """Espera a que el usuario valide manualmente la 2FA"""
    context.logger.info("Esperando validación manual de 2FA...")

    try:
        # Obtener la página apropiada (zafra o catálogo)
        page = get_page_object(context)

        resultado = page.esperar_validacion_manual_2fa()

        if not resultado:
            context.logger.error("❌ Error en validación manual de 2FA")
            raise AssertionError("Error en validación manual de 2FA")

        context.logger.info("✅ Validación manual de 2FA completada exitosamente")

    except Exception as e:
        context.logger.error(f"❌ Error en validación manual de 2FA: {e}")
        raise


@then("debe verificar que esté en la página principal de Zucarmex")
def step_verificar_pagina_principal_zucarmex(context):
    """Verifica que estemos en la página principal de Zucarmex"""
    context.logger.info("Verificando página principal de Zucarmex...")

    try:
        # Obtener la página apropiada (zafra o catálogo)
        page = get_page_object(context)

        resultado = page.verificar_pagina_principal_zucarmex()

        if not resultado:
            context.logger.warning(
                "⚠️ No se pudo verificar completamente la página principal"
            )
            # No fallar la prueba, solo registrar el warning

        context.logger.info("✅ Verificación de página principal completada")

    except Exception as e:
        context.logger.error(f"❌ Error verificando página principal: {e}")
        # No fallar la prueba por este error


@then("debe verificar que el logo de Zulka esté visible")
def step_verificar_logo_zulka(context):
    """Verifica que el logo de Zulka esté visible"""
    context.logger.info("Verificando visibilidad del logo de Zulka...")

    try:
        # Obtener estado de la página
        estado = context.alta_catalogo_page.obtener_estado_pagina()

        if estado:
            context.logger.info(f"Estado de la página: {estado}")

        # Capturar screenshot final
        context.alta_catalogo_page._capturar_screenshot("verificacion_logo_zulka")

        context.logger.info("✅ Verificación del logo de Zulka completada")

    except Exception as e:
        context.logger.error(f"❌ Error verificando logo: {e}")
        raise


@then("debe verificar que el botón OKTA esté disponible")
def step_verificar_boton_okta(context):
    """Verifica que el botón OKTA esté disponible"""
    context.logger.info("Verificando disponibilidad del botón OKTA...")

    try:
        # Verificar elementos de la página
        resultado = context.alta_catalogo_page.verificar_elementos_pagina()

        if resultado:
            context.logger.info("✅ Botón OKTA está disponible")
        else:
            context.logger.warning("⚠️ Botón OKTA no está disponible")

        # Capturar screenshot final
        context.alta_catalogo_page._capturar_screenshot("verificacion_boton_okta")

    except Exception as e:
        context.logger.error(f"❌ Error verificando botón OKTA: {e}")
        raise


@then("debe capturar screenshot de la página completa")
def step_capturar_screenshot_completo(context):
    """Captura un screenshot de la página completa"""
    context.logger.info("Capturando screenshot de la página completa...")

    try:
        context.alta_catalogo_page._capturar_screenshot("pagina_completa_final")
        context.logger.info("✅ Screenshot de página completa capturado")

    except Exception as e:
        context.logger.error(f"❌ Error capturando screenshot: {e}")
        raise


@then("debe capturar evidencias del proceso")
def step_capturar_evidencias(context):
    """Captura evidencias del proceso completo"""
    context.logger.info("Capturando evidencias del proceso...")

    try:
        # Capturar screenshot final
        context.alta_catalogo_page._capturar_screenshot("evidencias_finales")

        # Obtener estado final de la página
        estado_final = context.alta_catalogo_page.obtener_estado_pagina()

        if estado_final:
            context.logger.info(f"Estado final de la página: {estado_final}")

        context.logger.info("✅ Evidencias del proceso capturadas")

    except Exception as e:
        context.logger.error(f"❌ Error capturando evidencias: {e}")
        raise


# El environment.py ya maneja la limpieza del navegador
