"""
Locators para la página de Alta de Zafra
Sistema de Automatización - Zucarmex QA
"""

from selenium.webdriver.common.by import By


class AltaZafraLocators:
    """Locators para elementos de la página de Alta de Zafra"""

    def __init__(self):
        # Reutilizar locators de autenticación y navegación básica
        from locators.alta_catalogo_locators import AltaCatalogoLocators

        # Crear instancia de los locators base
        base_locators = AltaCatalogoLocators()

        # Reutilizar todos los locators de autenticación y navegación
        self.LOGO_ZULKA = base_locators.LOGO_ZULKA
        self.TITULO_ZULKA = base_locators.TITULO_ZULKA
        self.BOTON_OKTA = base_locators.BOTON_OKTA
        self.BOTON_OKTA_ALT = base_locators.BOTON_OKTA_ALT
        self.TARJETA_LOGIN = base_locators.TARJETA_LOGIN
        self.PAGINA_LOGIN = base_locators.PAGINA_LOGIN
        self.URL_LOGIN = base_locators.URL_LOGIN
        self.INDICADOR_CARGA = base_locators.INDICADOR_CARGA
        self.MENSAJE_ERROR = base_locators.MENSAJE_ERROR
        self.MENSAJE_EXITO = base_locators.MENSAJE_EXITO

        # Locators de OKTA
        self.OKTA_TITULO = base_locators.OKTA_TITULO
        self.OKTA_LOGO_ZUCARMEX = base_locators.OKTA_LOGO_ZUCARMEX
        self.OKTA_CAMPO_USUARIO = base_locators.OKTA_CAMPO_USUARIO
        self.OKTA_CAMPO_USUARIO_ALT = base_locators.OKTA_CAMPO_USUARIO_ALT
        self.OKTA_CHECKBOX_CONECTADO = base_locators.OKTA_CHECKBOX_CONECTADO
        self.OKTA_BOTON_SIGUIENTE = base_locators.OKTA_BOTON_SIGUIENTE
        self.OKTA_BOTON_SIGUIENTE_ALT = base_locators.OKTA_BOTON_SIGUIENTE_ALT
        self.OKTA_ENLACE_DESBLOQUEAR = base_locators.OKTA_ENLACE_DESBLOQUEAR
        self.OKTA_ENLACE_AYUDA = base_locators.OKTA_ENLACE_AYUDA
        self.OKTA_ICONO_CANDADO = base_locators.OKTA_ICONO_CANDADO
        self.OKTA_TEXTO_VERIFICAR = base_locators.OKTA_TEXTO_VERIFICAR
        self.OKTA_USUARIO_MOSTRADO = base_locators.OKTA_USUARIO_MOSTRADO
        self.OKTA_CAMPO_CONTRASENA = base_locators.OKTA_CAMPO_CONTRASENA
        self.OKTA_CAMPO_CONTRASENA_ALT = base_locators.OKTA_CAMPO_CONTRASENA_ALT
        self.OKTA_ICONO_OJO = base_locators.OKTA_ICONO_OJO
        self.OKTA_BOTON_VERIFICAR = base_locators.OKTA_BOTON_VERIFICAR
        self.OKTA_BOTON_VERIFICAR_ALT = base_locators.OKTA_BOTON_VERIFICAR_ALT
        self.OKTA_BOTON_VERIFICAR_ALT2 = base_locators.OKTA_BOTON_VERIFICAR_ALT2
        self.OKTA_ENLACE_OLVIDO_CONTRASENA = base_locators.OKTA_ENLACE_OLVIDO_CONTRASENA
        self.OKTA_ENLACE_VOLVER_LOGIN = base_locators.OKTA_ENLACE_VOLVER_LOGIN

        # Locators de página principal
        self.ZULKA_LOGO = base_locators.ZULKA_LOGO
        self.ZULKA_TITULO = base_locators.ZULKA_TITULO
        self.BIENVENIDO_TEXTO = base_locators.BIENVENIDO_TEXTO
        self.MENU_HAMBURGUESA = base_locators.MENU_HAMBURGUESA
        self.NAVEGACION_CREDITO = base_locators.NAVEGACION_CREDITO
        self.NAVEGACION_CAMPO = base_locators.NAVEGACION_CAMPO
        self.NAVEGACION_LABORATORIO = base_locators.NAVEGACION_LABORATORIO
        self.NAVEGACION_CONFIGURACION = base_locators.NAVEGACION_CONFIGURACION
        self.NAVEGACION_CONFIGURADOR = base_locators.NAVEGACION_CONFIGURADOR
        self.CONFIGURADOR_MENU = base_locators.CONFIGURADOR_MENU
        self.CONFIGURADOR_MENU_ALT = base_locators.CONFIGURADOR_MENU_ALT

        # Locators específicos para Zafra
        self.CONFIGURACION_MENU = (
            By.XPATH,
            "//*[contains(text(), 'Configuración')]",
        )
        self.CONFIGURACION_MENU_ALT = (
            By.XPATH,
            "//*[contains(@class, 'configuracion') or contains(@class, 'menu-item')]",
        )

        # Locator para Zafras (submenú de Configuración)
        self.ZAFRAS_MENU = (
            By.XPATH,
            "//*[contains(text(), 'Zafras')]",
        )
        self.ZAFRAS_MENU_ALT = (
            By.XPATH,
            "//*[contains(@class, 'zafras') or contains(@class, 'menu-item')]",
        )

        # Locator para el botón Nueva zafra
        self.BOTON_NUEVA_ZAFRA = (
            By.XPATH,
            "//button[contains(text(), 'Nueva zafra')]",
        )
        self.BOTON_NUEVA_ZAFRA_ALT = (
            By.XPATH,
            "//*[contains(text(), 'Nueva zafra')]",
        )

        # URLs
        self.URL_OKTA = base_locators.URL_OKTA
        self.URL_HOME = base_locators.URL_HOME
