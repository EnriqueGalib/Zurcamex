"""
Locators para la página de Alta de Catálogo
Sistema de Automatización - Zucarmex QA
"""

from selenium.webdriver.common.by import By


class AltaCatalogoLocators:
    """Locators para elementos de la página de Alta de Catálogo"""

    def __init__(self):
        # Elementos principales de la página de login
        self.LOGO_ZULKA = (By.CSS_SELECTOR, "img[alt*='Zulka'], .logo, [class*='logo']")
        self.TITULO_ZULKA = (By.XPATH, "//*[contains(text(), 'Zulka')]")

        # Botón de autenticación con OKTA
        self.BOTON_OKTA = (
            By.XPATH,
            "//button[contains(text(), 'AUTENTICARSE CON OKTA') or contains(text(), 'Autenticarse con OKTA')]",
        )
        self.BOTON_OKTA_ALT = (
            By.CSS_SELECTOR,
            "button[class*='okta'], .okta-button, [data-testid*='okta']",
        )

        # Elementos de la tarjeta de login
        self.TARJETA_LOGIN = (
            By.CSS_SELECTOR,
            ".login-card, .auth-card, [class*='login']",
        )

        # Elementos de validación
        self.PAGINA_LOGIN = (By.CSS_SELECTOR, "body, html")
        self.URL_LOGIN = "https://credicam-qa.zucarmex.com/login"

        # Elementos de carga/espera
        self.INDICADOR_CARGA = (
            By.CSS_SELECTOR,
            ".loading, .spinner, [class*='loading']",
        )

        # Elementos de error (por si aparecen)
        self.MENSAJE_ERROR = (By.CSS_SELECTOR, ".error, .alert-error, [class*='error']")
        self.MENSAJE_EXITO = (
            By.CSS_SELECTOR,
            ".success, .alert-success, [class*='success']",
        )

        # Elementos de la página de OKTA
        self.OKTA_TITULO = (
            By.XPATH,
            "//*[contains(text(), 'Conectando con') or contains(text(), 'Inicie sesión')]",
        )
        self.OKTA_LOGO_ZUCARMEX = (
            By.CSS_SELECTOR,
            "img[alt*='ZUCARMEX'], .okta-logo, [class*='logo']",
        )
        self.OKTA_CAMPO_USUARIO = (
            By.CSS_SELECTOR,
            "input[type='email'], input[name*='username'], input[id*='username'], input[placeholder*='usuario']",
        )
        self.OKTA_CAMPO_USUARIO_ALT = (
            By.XPATH,
            "//input[@type='text' or @type='email']",
        )
        self.OKTA_CHECKBOX_CONECTADO = (
            By.CSS_SELECTOR,
            "input[type='checkbox'], input[name*='remember']",
        )
        self.OKTA_BOTON_SIGUIENTE = (
            By.XPATH,
            "//button[contains(text(), 'Siguiente') or contains(text(), 'Next')]",
        )
        self.OKTA_BOTON_SIGUIENTE_ALT = (
            By.CSS_SELECTOR,
            "button[type='submit'], .okta-button, [class*='button']",
        )
        self.OKTA_ENLACE_DESBLOQUEAR = (
            By.XPATH,
            "//a[contains(text(), 'Desbloquear') or contains(text(), 'Unlock')]",
        )
        self.OKTA_ENLACE_AYUDA = (
            By.XPATH,
            "//a[contains(text(), 'Ayuda') or contains(text(), 'Help')]",
        )

        # Elementos de la página de contraseña de OKTA
        self.OKTA_ICONO_CANDADO = (
            By.CSS_SELECTOR,
            ".okta-icon, .lock-icon, [class*='lock'], [class*='candado']",
        )
        self.OKTA_TEXTO_VERIFICAR = (
            By.XPATH,
            "//*[contains(text(), 'Verifique con su contraseña') or contains(text(), 'Verify with your password')]",
        )
        self.OKTA_USUARIO_MOSTRADO = (
            By.XPATH,
            "//*[contains(text(), 'consultores-mobiik-okta@zucarmex.com')]",
        )
        self.OKTA_CAMPO_CONTRASENA = (
            By.CSS_SELECTOR,
            "input[type='password'], input[name*='password'], input[id*='password']",
        )
        self.OKTA_CAMPO_CONTRASENA_ALT = (By.XPATH, "//input[@type='password']")
        self.OKTA_ICONO_OJO = (
            By.CSS_SELECTOR,
            ".eye-icon, .show-password, [class*='eye'], [class*='show']",
        )
        self.OKTA_BOTON_VERIFICAR = (
            By.XPATH,
            "//*[@id='form53']/div[2]/input",
        )
        self.OKTA_BOTON_VERIFICAR_ALT = (
            By.XPATH,
            "//button[contains(text(), 'Verificar') or contains(text(), 'Verify')]",
        )
        self.OKTA_BOTON_VERIFICAR_ALT2 = (
            By.CSS_SELECTOR,
            "button[type='submit'], .okta-button, [class*='verify']",
        )
        self.OKTA_ENLACE_OLVIDO_CONTRASENA = (
            By.XPATH,
            "//a[contains(text(), 'Olvidó') or contains(text(), 'Forgot')]",
        )
        self.OKTA_ENLACE_VOLVER_LOGIN = (
            By.XPATH,
            "//a[contains(text(), 'Volver') or contains(text(), 'Go back')]",
        )

        # Elementos de la página principal de Zucarmex
        self.ZULKA_LOGO = (By.CSS_SELECTOR, ".logo, [class*='logo'], img[alt*='Zulka']")
        self.ZULKA_TITULO = (By.XPATH, "//*[contains(text(), 'Zulka')]")
        self.BIENVENIDO_TEXTO = (
            By.XPATH,
            "//*[contains(text(), 'Bienvenido a Zucarmex')]",
        )
        self.MENU_HAMBURGUESA = (
            By.CSS_SELECTOR,
            ".hamburger, .menu-toggle, [class*='menu']",
        )
        self.NAVEGACION_CREDITO = (By.XPATH, "//*[contains(text(), 'Crédito')]")
        self.NAVEGACION_CAMPO = (By.XPATH, "//*[contains(text(), 'Campo')]")
        self.NAVEGACION_LABORATORIO = (By.XPATH, "//*[contains(text(), 'Laboratorio')]")
        self.NAVEGACION_CONFIGURACION = (
            By.XPATH,
            "//*[contains(text(), 'Configuración')]",
        )
        self.NAVEGACION_CONFIGURADOR = (
            By.XPATH,
            "//*[contains(text(), 'Configurador')]",
        )
        self.CONFIGURADOR_MENU = (
            By.XPATH,
            "//*[contains(text(), 'Configurador')]",
        )
        self.CONFIGURADOR_MENU_ALT = (
            By.CSS_SELECTOR,
            "[class*='configurador'], [class*='menu-item']:contains('Configurador')",
        )

        # Gestor de Catálogos
        self.GESTOR_CATALOGOS = (
            By.XPATH,
            "//*[contains(text(), 'Gestor de catálogos')]",
        )
        self.GESTOR_CATALOGOS_ALT = (
            By.CSS_SELECTOR,
            "[class*='gestor'], [class*='catalogos'], [class*='menu-item']:contains('Gestor')",
        )

        # Botón NUEVO CATÁLOGO
        self.BOTON_NUEVO_CATALOGO = (
            By.XPATH,
            "//button[contains(text(), 'NUEVO CATÁLOGO')]",
        )
        self.BOTON_NUEVO_CATALOGO_ALT = (
            By.CSS_SELECTOR,
            "button:contains('NUEVO CATÁLOGO'), [class*='nuevo'], [class*='catalogo']",
        )

        # Formulario Nuevo Catálogo - Campos (IDs actualizados según debug)
        self.CAMPO_NOMBRE = (By.XPATH, "//input[@name='nombre']")
        self.CAMPO_DESCRIPCION = (By.XPATH, "//input[@name='descripcion']")
        self.DROPDOWN_CLASIFICACION_AREA = (By.XPATH, "//input[@name='tipo_area']")
        self.DROPDOWN_TIPO_CLASIFICACION = (
            By.XPATH,
            "//input[@name='clasificacion_id']",
        )

        # Opciones de Dropdowns (IDs dinámicos actualizados)
        self.OPCION_CLASIFICACION_AREA = (By.XPATH, "//*[@id='«rn»']/li[2]")
        self.OPCION_TIPO_CLASIFICACION = (By.XPATH, "//*[@id='«ro»']/li[2]")

        # Opciones alternativas por clase Material-UI
        self.OPCION_CLASIFICACION_AREA_ALT = (
            By.XPATH,
            "//li[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Crédito')]",
        )
        self.OPCION_TIPO_CLASIFICACION_ALT = (
            By.XPATH,
            "//li[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Global')]",
        )

        # Botón Guardar Datos Generales
        self.BOTON_GUARDAR_DATOS_GENERALES = (
            By.XPATH,
            "//*[@id='custom-tabpanel-0']/div/div/div/form/div[2]/button",
        )

        # Estructura del Catálogo - Campos (IDs actualizados según debug)
        self.CAMPO_NOMBRE_TECNICO = (By.XPATH, "//*[@id='«r2n»']")
        self.CAMPO_ETIQUETA = (By.XPATH, "//*[@id='«r2o»']")
        self.DROPDOWN_TIPO_DATO = (By.XPATH, "//*[@id='tipoDato-0']")

        # Opción de Tipo de Dato (IDs dinámicos actualizados)
        self.OPCION_TIPO_DATO = (By.XPATH, "//*[@id='«r18»']/li[2]")
        self.OPCION_TIPO_DATO_ALT = (
            By.XPATH,
            "//li[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Texto')]",
        )

        # Botón Guardar Estructura
        self.BOTON_GUARDAR_ESTRUCTURA = (
            By.XPATH,
            "//*[@id='custom-tabpanel-1']/div/div/form/div[3]/button",
        )
        self.BOTON_CERRAR_SESION = (By.XPATH, "//*[contains(text(), 'Cerrar Sesión')]")
        self.USUARIO_INFO = (
            By.XPATH,
            "//*[contains(text(), 'Consultores Mobilk Okta')]",
        )

        # URLs
        self.URL_OKTA = "zucarmex.okta.com"
        self.URL_HOME = "credicam-qa.zucarmex.com/home"
