import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.login_locators import LoginLocators


class LoginPage:
    """Page Object para la página de login"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(__name__)

    def navigate_to_login(self, url):
        """Navega a la página de login"""
        try:
            self.driver.get(url)
            self.logger.info(f"Navegando a: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Error navegando a {url}: {str(e)}")
            return False

    def click_okta_auth_button(self):
        """Hace clic en el botón 'AUTENTICARSE CON OKTA'"""
        try:
            # Intentar con XPath primero
            okta_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, LoginLocators.OKTA_AUTH_BUTTON_ALT)
                )
            )
            okta_button.click()
            self.logger.info("Botón 'AUTENTICARSE CON OKTA' clickeado exitosamente")

            # Esperar a que la página se cargue completamente
            import time

            time.sleep(3)
            self.logger.info("Esperando 3 segundos para que la página se cargue...")

            return True
        except Exception as e:
            self.logger.error(f"Error clickeando botón OKTA: {str(e)}")
            return False

    def debug_page_elements(self):
        """Método de debug para verificar elementos en la página"""
        try:
            self.logger.info("=== DEBUG: Elementos en la página ===")
            self.logger.info(f"URL actual: {self.driver.current_url}")
            self.logger.info(f"Título de la página: {self.driver.title}")

            # Buscar todos los inputs
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            self.logger.info(f"Encontrados {len(inputs)} elementos input:")
            for i, input_elem in enumerate(inputs):
                self.logger.info(
                    f"  Input {i+1}: type='{input_elem.get_attribute('type')}', name='{input_elem.get_attribute('name')}', id='{input_elem.get_attribute('id')}', value='{input_elem.get_attribute('value')}'"
                )

            # Buscar todos los botones
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            self.logger.info(f"Encontrados {len(buttons)} elementos button:")
            for i, button in enumerate(buttons):
                self.logger.info(
                    f"  Button {i+1}: text='{button.text}', type='{button.get_attribute('type')}', class='{button.get_attribute('class')}'"
                )

            # Buscar elementos con texto "Siguiente", "Next", "Iniciar sesión", "Sign In", "Verificar"
            try:
                next_elements = self.driver.find_elements(
                    By.XPATH,
                    "//*[contains(text(), 'Siguiente') or contains(text(), 'Next') or contains(text(), 'Iniciar sesión') or contains(text(), 'Sign In') or contains(text(), 'Verificar')]",
                )
                self.logger.info(
                    f"Encontrados {len(next_elements)} elementos con texto de botones:"
                )
                for i, elem in enumerate(next_elements):
                    self.logger.info(
                        f"  Elemento {i+1}: tag='{elem.tag_name}', text='{elem.text}', class='{elem.get_attribute('class')}', value='{elem.get_attribute('value')}'"
                    )
            except Exception as e:
                self.logger.warning(f"Error buscando elementos de botones: {str(e)}")

            # Buscar todos los inputs de tipo submit
            try:
                submit_inputs = self.driver.find_elements(
                    By.XPATH, "//input[@type='submit']"
                )
                self.logger.info(
                    f"Encontrados {len(submit_inputs)} inputs de tipo submit:"
                )
                for i, elem in enumerate(submit_inputs):
                    self.logger.info(
                        f"  Submit {i+1}: value='{elem.get_attribute('value')}', name='{elem.get_attribute('name')}', id='{elem.get_attribute('id')}'"
                    )
            except Exception as e:
                self.logger.warning(f"Error buscando inputs submit: {str(e)}")

            self.logger.info("=== FIN DEBUG ===")
        except Exception as e:
            self.logger.error(f"Error en debug: {str(e)}")

    def enter_username(self, username):
        """Ingresa el nombre de usuario en OKTA con múltiples selectores"""
        selectors = [
            (By.CSS_SELECTOR, LoginLocators.OKTA_USERNAME_FIELD),
            (By.CSS_SELECTOR, LoginLocators.OKTA_USERNAME_FIELD_ALT1),
            (By.CSS_SELECTOR, LoginLocators.OKTA_USERNAME_FIELD_ALT2),
            (By.CSS_SELECTOR, LoginLocators.OKTA_USERNAME_FIELD_ALT3),
            (By.XPATH, LoginLocators.OKTA_USERNAME_FIELD_ALT4),
            (By.XPATH, LoginLocators.OKTA_USERNAME_FIELD_ALT5),
        ]

        for by_type, selector in selectors:
            try:
                self.logger.info(f"Intentando selector: {selector}")
                username_field = self.wait.until(
                    EC.element_to_be_clickable((by_type, selector))
                )
                username_field.clear()
                username_field.send_keys(username)
                self.logger.info(f"Usuario ingresado exitosamente en OKTA: {username}")
                return True
            except Exception as e:
                self.logger.warning(f"Selector {selector} falló: {str(e)}")
                continue

        self.logger.error("Todos los selectores de usuario fallaron")
        return False

    def click_next_button(self):
        """Hace clic en el botón 'Siguiente' de OKTA con múltiples selectores"""
        selectors = [
            (By.XPATH, LoginLocators.OKTA_NEXT_BUTTON),
            (By.XPATH, LoginLocators.OKTA_NEXT_BUTTON_ALT1),
            (By.XPATH, LoginLocators.OKTA_NEXT_BUTTON_ALT2),
            (By.XPATH, LoginLocators.OKTA_NEXT_BUTTON_ALT3),
            (By.CSS_SELECTOR, LoginLocators.OKTA_NEXT_BUTTON_ALT4),
            (By.CSS_SELECTOR, LoginLocators.OKTA_NEXT_BUTTON_ALT5),
        ]

        for by_type, selector in selectors:
            try:
                self.logger.info(f"Intentando selector de botón Siguiente: {selector}")
                next_button = self.wait.until(
                    EC.element_to_be_clickable((by_type, selector))
                )
                next_button.click()
                self.logger.info("Botón 'Siguiente' clickeado exitosamente en OKTA")
                return True
            except Exception as e:
                self.logger.warning(
                    f"Selector de botón Siguiente {selector} falló: {str(e)}"
                )
                continue

        self.logger.error("Todos los selectores de botón 'Siguiente' fallaron")
        return False

    def enter_password(self, password):
        """Ingresa la contraseña en OKTA con múltiples selectores"""
        selectors = [
            (By.CSS_SELECTOR, LoginLocators.OKTA_PASSWORD_FIELD),
            (By.CSS_SELECTOR, LoginLocators.OKTA_PASSWORD_FIELD_ALT1),
            (By.XPATH, LoginLocators.OKTA_PASSWORD_FIELD_ALT2),
        ]

        for by_type, selector in selectors:
            try:
                self.logger.info(f"Intentando selector de contraseña: {selector}")
                password_field = self.wait.until(
                    EC.element_to_be_clickable((by_type, selector))
                )
                password_field.clear()
                password_field.send_keys(password)
                self.logger.info("Contraseña ingresada exitosamente en OKTA")
                return True
            except Exception as e:
                self.logger.warning(
                    f"Selector de contraseña {selector} falló: {str(e)}"
                )
                continue

        self.logger.error("Todos los selectores de contraseña fallaron")
        return False

    def click_login_button(self):
        """Hace clic en el botón de login de OKTA con múltiples selectores"""
        selectors = [
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT1),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT2),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT3),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT4),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT5),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT6),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT7),
            (By.XPATH, LoginLocators.OKTA_SIGNIN_BUTTON_ALT8),
        ]

        for by_type, selector in selectors:
            try:
                self.logger.info(f"Intentando selector de botón login: {selector}")
                login_button = self.wait.until(
                    EC.element_to_be_clickable((by_type, selector))
                )
                login_button.click()
                self.logger.info("✅ Botón 'Verificar' clickeado exitosamente en OKTA")

                # Esperar un momento después del clic para que se procese
                import time

                time.sleep(2)
                self.logger.info(
                    "⏱️ Esperando 2 segundos después del clic en 'Verificar'..."
                )

                return True
            except Exception as e:
                self.logger.warning(
                    f"Selector de botón login {selector} falló: {str(e)}"
                )
                continue

        self.logger.error("Todos los selectores de botón de login fallaron")
        return False

    def login(self, username, password):
        """Realiza el proceso completo de login con OKTA (dos pasos)"""
        try:
            # Paso 1: Hacer clic en el botón OKTA inicial
            self.click_okta_auth_button()

            # Debug: Verificar elementos después del clic en OKTA
            self.debug_page_elements()

            # Paso 2: Ingresar usuario y hacer clic en "Siguiente"
            if not self.enter_username(username):
                self.logger.error("No se pudo ingresar el usuario")
                return False

            if not self.click_next_button():
                self.logger.error("No se pudo hacer clic en 'Siguiente'")
                return False

            # Debug: Verificar elementos después del clic en "Siguiente"
            self.debug_page_elements()

            # Paso 3: Ingresar contraseña y hacer clic en "Iniciar sesión"
            if not self.enter_password(password):
                self.logger.error("No se pudo ingresar la contraseña")
                return False

            # Esperar un poco después de ingresar la contraseña
            import time

            time.sleep(2)
            self.logger.info("Esperando 2 segundos después de ingresar contraseña...")

            if not self.click_login_button():
                self.logger.error("No se pudo hacer clic en 'Iniciar sesión'")
                return False

            self.logger.info("Proceso de login con OKTA completado")
            return True
        except Exception as e:
            self.logger.error(f"Error en el proceso de login con OKTA: {str(e)}")
            return False

    def is_login_successful(self):
        """Verifica si el login fue exitoso (después del 2FA manual)"""
        try:
            # Esperar a que la URL cambie o aparezca algún elemento del dashboard
            # Esto se ejecutará después del 2FA manual
            self.wait.until(
                lambda driver: "login" not in driver.current_url.lower()
                and "okta" not in driver.current_url.lower()
            )
            self.logger.info("Login exitoso - redirigido del login y OKTA")
            return True
        except Exception as e:
            self.logger.error(f"Error verificando login exitoso: {str(e)}")
            return False

    def wait_for_manual_2fa(self):
        """Pausa la automatización para permitir validación manual del 2FA con detección automática del HOME"""
        try:
            self.logger.info(
                "⏸️ PAUSA AUTOMATIZACIÓN: Validación manual del 2FA requerida"
            )

            # Mostrar mensaje claro al usuario
            print("\n" + "=" * 80)
            print("🔐 VALIDACIÓN MANUAL DEL 2FA REQUERIDA")
            print("=" * 80)
            print("✅ El botón 'Verificar' ha sido clickeado exitosamente")
            print(
                "⏸️  La automatización se ha pausado para permitir la validación manual del 2FA."
            )
            print("")
            print("📱 INSTRUCCIONES:")
            print("1. Revise su dispositivo móvil o aplicación de autenticación")
            print("2. Complete la validación del 2FA (código, notificación, etc.)")
            print("3. Espere a que aparezca la página HOME del sistema")
            print(
                "4. La automatización detectará automáticamente cuando esté en el HOME"
            )
            print("")
            print(
                "⏱️  DETECCIÓN AUTOMÁTICA: La automatización verificará cada 5 segundos"
            )
            print("🏠 VERIFICACIÓN: Esperando a que aparezca el HOME del sistema")
            print("🔄 CONTINUACIÓN: La automatización continuará automáticamente")
            print("=" * 80)

            # Intentar detección automática del HOME con timeout
            max_attempts = 60  # 5 minutos máximo (60 * 5 segundos)
            attempt = 0

            while attempt < max_attempts:
                attempt += 1
                self.logger.info(
                    f"🔍 Intento {attempt}/{max_attempts}: Verificando si estamos en el HOME..."
                )

                # Verificar si ya estamos en el HOME
                if self.is_on_home_page():
                    self.logger.info(
                        "🏠 ¡HOME detectado automáticamente! Continuando..."
                    )
                    print(
                        "🏠 ¡HOME detectado automáticamente! Continuando automatización..."
                    )
                    return True

                # Esperar 5 segundos antes del siguiente intento
                import time

                time.sleep(5)

                # Mostrar progreso cada 30 segundos (6 intentos)
                if attempt % 6 == 0:
                    remaining_time = (max_attempts - attempt) * 5
                    print(
                        f"⏳ Esperando HOME... Tiempo restante: {remaining_time} segundos"
                    )

            # Si llegamos aquí, no se detectó el HOME automáticamente
            self.logger.warning(
                "⚠️ No se detectó el HOME automáticamente. Solicitando confirmación manual..."
            )
            print("\n⚠️ No se detectó el HOME automáticamente.")
            print("Por favor, confirme manualmente que está en el HOME del sistema.")

            try:
                input("Presione ENTER cuando esté en el HOME para continuar...")
                self.logger.info("✅ Usuario confirmó manualmente que está en el HOME")
                print("✅ Continuando automatización...")
                return True
            except KeyboardInterrupt:
                self.logger.warning("Usuario interrumpió la ejecución")
                print("\n❌ Ejecución interrumpida por el usuario")
                raise KeyboardInterrupt

        except Exception as e:
            self.logger.error(f"Error en espera manual del 2FA: {str(e)}")
            return False

    def is_on_home_page(self):
        """Verifica si estamos en la página HOME del sistema"""
        try:
            current_url = self.driver.current_url.lower()

            # Verificar que no estamos en páginas de login/OKTA
            if "login" in current_url or "okta" in current_url:
                return False

            # Verificar elementos típicos del HOME del sistema
            home_indicators = [
                # Buscar elementos comunes del dashboard/home
                "//div[contains(@class, 'dashboard')]",
                "//div[contains(@class, 'home')]",
                "//div[contains(@class, 'main-content')]",
                "//div[contains(@class, 'content-area')]",
                "//nav[contains(@class, 'navbar')]",
                "//header[contains(@class, 'header')]",
                "//aside[contains(@class, 'sidebar')]",
                "//div[contains(@class, 'menu')]",
                # Buscar elementos específicos de Zucarmex/Credicam
                "//*[contains(text(), 'Configurador')]",
                "//*[contains(text(), 'Catálogos')]",
                "//*[contains(text(), 'Gestor')]",
                "//*[contains(text(), 'Sistema')]",
                "//*[contains(text(), 'Dashboard')]",
                "//*[contains(text(), 'Inicio')]",
                # Buscar elementos de navegación
                "//a[contains(@href, 'dashboard')]",
                "//a[contains(@href, 'home')]",
                "//a[contains(@href, 'main')]",
            ]

            # Verificar al menos uno de los indicadores
            for indicator in home_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    if elements:
                        self.logger.info(f"🏠 Indicador HOME encontrado: {indicator}")
                        return True
                except Exception:
                    continue

            # Verificar que la URL parece ser del sistema (no login/OKTA)
            if any(
                keyword in current_url
                for keyword in ["credicam", "zucarmex", "dashboard", "home", "main"]
            ):
                self.logger.info(f"🏠 URL del sistema detectada: {current_url}")
                return True

            # Si no encontramos indicadores específicos, verificar que al menos no estamos en login/OKTA
            if not any(
                keyword in current_url
                for keyword in ["login", "okta", "auth", "signin"]
            ):
                self.logger.info(
                    f"🏠 Página del sistema detectada (no login/OKTA): {current_url}"
                )
                return True

            return False

        except Exception as e:
            self.logger.error(f"Error verificando página HOME: {str(e)}")
            return False

    def wait_for_home_page(self):
        """Espera a que aparezca la página HOME después del 2FA"""
        try:
            # Esperar a que la URL cambie y no contenga login ni okta
            self.wait.until(
                lambda driver: "login" not in driver.current_url.lower()
                and "okta" not in driver.current_url.lower()
            )
            self.logger.info("🏠 Página HOME detectada - autenticación completa")
            return True
        except Exception as e:
            self.logger.error(f"Error esperando página HOME: {str(e)}")
            return False
