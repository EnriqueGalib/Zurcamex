"""
Locators para la página de login con OKTA
Sistema de Automatización - Zucarmex QA
"""

from selenium.webdriver.common.by import By


class LoginOktaLocators:
    """Locators para elementos de la página de login con OKTA"""

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
