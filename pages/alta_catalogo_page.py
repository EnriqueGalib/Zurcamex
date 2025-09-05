"""
Page Object para la página de Alta de Catálogo
Sistema de Automatización - Zucarmex QA
"""

import logging
import os
import time
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.alta_catalogo_locators import AltaCatalogoLocators


class AltaCatalogoPage:
    """Page Object para la página de Alta de Catálogo"""

    def __init__(self, driver):
        self.driver = driver
        self.locators = AltaCatalogoLocators()
        self.wait = WebDriverWait(driver, 15)
        self.logger = logging.getLogger(__name__)
        self.execution_folder = None  # Carpeta específica para esta ejecución

    def set_execution_folder(
        self, feature_name, scenario_name, execution_timestamp=None
    ):
        """Configura la carpeta de ejecución para esta instancia"""
        try:
            from utils.evidence_manager import EvidenceManager

            evidence_manager = EvidenceManager()
            self.execution_folder = evidence_manager.get_execution_folder(
                feature_name, scenario_name, execution_timestamp
            )
            self.logger.info(
                f"📁 Carpeta de ejecución configurada: {self.execution_folder}"
            )
        except Exception as e:
            self.logger.error(f"❌ Error configurando carpeta de ejecución: {e}")
            # Fallback a estructura simple
            self.execution_folder = (
                f"evidences/{datetime.now().strftime('%Y-%m-%d')}/alta_catalogo"
            )

    def navegar_a_login(self):
        """Navega a la página de login"""
        try:
            self.logger.info("Navegando a la página de login...")
            self.driver.get(self.locators.URL_LOGIN)

            # Esperar a que la página cargue completamente
            self.wait.until(EC.presence_of_element_located(self.locators.PAGINA_LOGIN))

            # Capturar screenshot de la página cargada
            self._capturar_screenshot("pagina_login_cargada")

            self.logger.info(f"✅ Navegación exitosa a: {self.locators.URL_LOGIN}")
            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al cargar la página de login")
            self._capturar_screenshot("error_timeout_login")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error al navegar a login: {e}")
            self._capturar_screenshot("error_navegacion_login")
            return False

    def navegar_a_login_y_clic_inmediato(self):
        """Navega a la página de login y hace clic inmediato en OKTA"""
        try:
            self.logger.info(
                "Navegando a la página de login y haciendo clic inmediato..."
            )
            self.driver.get(self.locators.URL_LOGIN)

            # Esperar solo a que el body esté presente (mínimo necesario) - ULTRA RÁPIDO
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located(self.locators.PAGINA_LOGIN)
            )

            # Capturar screenshot de la página cargada
            self._capturar_screenshot("pagina_login_cargada")

            # Hacer clic inmediato en OKTA sin esperas adicionales
            self.logger.info("Haciendo clic inmediato en OKTA...")

            # Intentar con timeout muy corto (2 segundos)
            try:
                boton_okta = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.BOTON_OKTA)
                )
                self.logger.info("✅ Botón OKTA encontrado inmediatamente")
            except TimeoutException:
                # Si no encuentra con el primer selector, intentar con el alternativo
                self.logger.info("Intentando con selector alternativo...")
                boton_okta = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.BOTON_OKTA_ALT)
                )
                self.logger.info("✅ Botón OKTA encontrado con selector alternativo")

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_okta_inmediato")

            # Hacer clic inmediatamente
            boton_okta.click()
            self.logger.info("✅ Clic inmediato realizado en el botón OKTA")

            # Esperar solo 0.5 segundos para que se procese el clic
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_okta_inmediato")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            self.logger.info(
                f"✅ Navegación y clic inmediato exitoso en: {self.locators.URL_LOGIN}"
            )
            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic inmediato en OKTA")
            self._capturar_screenshot("error_timeout_clic_inmediato")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error en navegación y clic inmediato: {e}")
            self._capturar_screenshot("error_navegacion_clic_inmediato")
            return False

    def verificar_elementos_pagina(self):
        """Verifica que los elementos principales de la página estén presentes"""
        try:
            self.logger.info("Verificando elementos de la página de login...")

            elementos_verificados = []

            # Verificar logo/título Zulka
            try:
                self.wait.until(
                    EC.presence_of_element_located(self.locators.TITULO_ZULKA)
                )
                elementos_verificados.append("Título Zulka")
                self.logger.info("✅ Título Zulka encontrado")
            except TimeoutException:
                self.logger.warning("⚠️ Título Zulka no encontrado")

            # Verificar botón OKTA
            try:
                self.wait.until(
                    EC.presence_of_element_located(self.locators.BOTON_OKTA)
                )
                elementos_verificados.append("Botón OKTA")
                self.logger.info("✅ Botón OKTA encontrado")
            except TimeoutException:
                self.logger.warning("⚠️ Botón OKTA no encontrado con selector principal")

                # Intentar con selector alternativo
                try:
                    self.wait.until(
                        EC.presence_of_element_located(self.locators.BOTON_OKTA_ALT)
                    )
                    elementos_verificados.append("Botón OKTA (alternativo)")
                    self.logger.info(
                        "✅ Botón OKTA encontrado con selector alternativo"
                    )
                except TimeoutException:
                    self.logger.error("❌ Botón OKTA no encontrado con ningún selector")

            # Verificar tarjeta de login
            try:
                self.wait.until(
                    EC.presence_of_element_located(self.locators.TARJETA_LOGIN)
                )
                elementos_verificados.append("Tarjeta de login")
                self.logger.info("✅ Tarjeta de login encontrada")
            except TimeoutException:
                self.logger.warning("⚠️ Tarjeta de login no encontrada")

            self.logger.info(
                f"Elementos verificados: {', '.join(elementos_verificados)}"
            )
            return len(elementos_verificados) > 0

        except Exception as e:
            self.logger.error(f"❌ Error verificando elementos: {e}")
            self._capturar_screenshot("error_verificacion_elementos")
            return False

    def hacer_clic_okta_inmediato(self):
        """Hace clic inmediatamente en el botón de autenticación con OKTA sin verificaciones adicionales"""
        try:
            self.logger.info("Haciendo clic inmediato en el botón OKTA...")

            # Intentar con el selector principal (timeout ultra corto)
            try:
                boton_okta = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.BOTON_OKTA)
                )
                self.logger.info("✅ Botón OKTA encontrado con selector principal")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                boton_okta = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.BOTON_OKTA_ALT)
                )
                self.logger.info("✅ Botón OKTA encontrado con selector alternativo")

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_okta_inmediato")

            # Hacer clic inmediatamente
            boton_okta.click()
            self.logger.info("✅ Clic inmediato realizado en el botón OKTA")

            # Esperar solo 0.2 segundos para que se procese el clic - ULTRA RÁPIDO
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_okta_inmediato")

            # Verificar si hay redirección o cambio en la página
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic inmediato en el botón OKTA")
            self._capturar_screenshot("error_timeout_clic_okta_inmediato")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error al hacer clic inmediato en OKTA: {e}")
            self._capturar_screenshot("error_clic_okta_inmediato")
            return False

    def hacer_clic_okta(self):
        """Hace clic en el botón de autenticación con OKTA"""
        try:
            self.logger.info("Intentando hacer clic en el botón OKTA...")

            # Intentar con el selector principal
            try:
                boton_okta = self.wait.until(
                    EC.element_to_be_clickable(self.locators.BOTON_OKTA)
                )
                self.logger.info("✅ Botón OKTA encontrado con selector principal")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                boton_okta = self.wait.until(
                    EC.element_to_be_clickable(self.locators.BOTON_OKTA_ALT)
                )
                self.logger.info("✅ Botón OKTA encontrado con selector alternativo")

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_okta")

            # Hacer clic en el botón
            boton_okta.click()
            self.logger.info("✅ Clic realizado en el botón OKTA")

            # Esperar un momento para que se procese el clic
            time.sleep(2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_okta")

            # Verificar si hay redirección o cambio en la página
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic en el botón OKTA")
            self._capturar_screenshot("error_timeout_clic_okta")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error al hacer clic en OKTA: {e}")
            self._capturar_screenshot("error_clic_okta")
            return False

    def verificar_redireccion_okta(self):
        """Verifica si se produjo la redirección a OKTA"""
        try:
            self.logger.info("Verificando redirección a OKTA...")

            # Esperar un momento para que se complete la redirección - ULTRA RÁPIDO
            time.sleep(1)

            url_actual = self.driver.current_url
            self.logger.info(f"URL actual: {url_actual}")

            # Verificar si la URL contiene indicadores de OKTA
            if "okta" in url_actual.lower() or "sso" in url_actual.lower():
                self.logger.info("✅ Redirección a OKTA detectada")
                self._capturar_screenshot("redireccion_okta_exitosa")
                return True
            else:
                self.logger.warning(
                    f"⚠️ No se detectó redirección a OKTA. URL actual: {url_actual}"
                )
                self._capturar_screenshot("sin_redireccion_okta")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando redirección: {e}")
            self._capturar_screenshot("error_verificacion_redireccion")
            return False

    def verificar_pagina_okta(self):
        """Verifica que estemos en la página de OKTA"""
        try:
            self.logger.info("Verificando página de OKTA...")

            # Esperar a que la página de OKTA cargue
            time.sleep(2)

            url_actual = self.driver.current_url
            self.logger.info(f"URL actual: {url_actual}")

            # Verificar si estamos en OKTA
            if self.locators.URL_OKTA in url_actual:
                self.logger.info("✅ Página de OKTA detectada")
                self._capturar_screenshot("pagina_okta_cargada")
                return True
            else:
                self.logger.warning(
                    f"⚠️ No se detectó página de OKTA. URL: {url_actual}"
                )
                self._capturar_screenshot("pagina_no_okta")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando página de OKTA: {e}")
            self._capturar_screenshot("error_verificacion_okta")
            return False

    def ingresar_usuario_okta(self, usuario):
        """Ingresa el usuario en el campo de OKTA"""
        try:
            self.logger.info(f"Ingresando usuario en OKTA: {usuario}")

            # Buscar el campo de usuario con timeout ultra corto
            try:
                campo_usuario = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_USUARIO)
                )
                self.logger.info("✅ Campo de usuario encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_usuario = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_USUARIO_ALT)
                )
                self.logger.info(
                    "✅ Campo de usuario encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar el usuario
            campo_usuario.clear()
            campo_usuario.send_keys(usuario)
            self.logger.info(f"✅ Usuario ingresado: {usuario}")

            # Capturar screenshot después de ingresar usuario
            self._capturar_screenshot("usuario_ingresado_okta")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al encontrar campo de usuario en OKTA")
            self._capturar_screenshot("error_timeout_campo_usuario")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error ingresando usuario en OKTA: {e}")
            self._capturar_screenshot("error_ingresar_usuario")
            return False

    def hacer_clic_siguiente_okta(self):
        """Hace clic en el botón Siguiente de OKTA"""
        try:
            self.logger.info("Haciendo clic en botón Siguiente de OKTA...")

            # Buscar el botón Siguiente con timeout ultra corto
            try:
                boton_siguiente = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_SIGUIENTE)
                )
                self.logger.info("✅ Botón Siguiente encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                boton_siguiente = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_SIGUIENTE_ALT)
                )
                self.logger.info(
                    "✅ Botón Siguiente encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_siguiente_okta")

            # Hacer clic en el botón
            boton_siguiente.click()
            self.logger.info("✅ Clic realizado en botón Siguiente")

            # Esperar solo 0.5 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_siguiente_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic en botón Siguiente")
            self._capturar_screenshot("error_timeout_boton_siguiente")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en botón Siguiente: {e}")
            self._capturar_screenshot("error_clic_siguiente")
            return False

    def ingresar_usuario_y_clic_siguiente_okta(self, usuario):
        """Ingresa el usuario y hace clic en Siguiente de forma ultra rápida"""
        try:
            self.logger.info(
                f"Ingresando usuario y haciendo clic en Siguiente: {usuario}"
            )

            # Buscar el campo de usuario con timeout ultra corto
            try:
                campo_usuario = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_USUARIO)
                )
                self.logger.info("✅ Campo de usuario encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_usuario = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_USUARIO_ALT)
                )
                self.logger.info(
                    "✅ Campo de usuario encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar el usuario de forma rápida
            campo_usuario.clear()
            campo_usuario.send_keys(usuario)
            self.logger.info(f"✅ Usuario ingresado: {usuario}")

            # Capturar screenshot después de ingresar usuario
            self._capturar_screenshot("usuario_ingresado_okta")

            # Buscar el botón Siguiente con timeout ultra corto
            try:
                boton_siguiente = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_SIGUIENTE)
                )
                self.logger.info("✅ Botón Siguiente encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                boton_siguiente = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_SIGUIENTE_ALT)
                )
                self.logger.info(
                    "✅ Botón Siguiente encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_siguiente_okta")

            # Hacer clic en el botón inmediatamente
            boton_siguiente.click()
            self.logger.info("✅ Clic realizado en botón Siguiente")

            # Esperar solo 0.5 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_siguiente_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            self.logger.info("✅ Usuario ingresado y clic en Siguiente completado")
            return True

        except TimeoutException:
            self.logger.error("❌ Timeout en ingreso de usuario y clic en Siguiente")
            self._capturar_screenshot("error_timeout_usuario_siguiente")
            return False
        except Exception as e:
            self.logger.error(
                f"❌ Error en ingreso de usuario y clic en Siguiente: {e}"
            )
            self._capturar_screenshot("error_usuario_siguiente")
            return False

    def verificar_pagina_contrasena_okta(self):
        """Verifica que estemos en la página de contraseña de OKTA"""
        try:
            self.logger.info("Verificando página de contraseña de OKTA...")

            # Esperar a que la página de contraseña cargue
            time.sleep(2)

            url_actual = self.driver.current_url
            self.logger.info(f"URL actual: {url_actual}")

            # Verificar si estamos en OKTA y hay elementos de contraseña
            if self.locators.URL_OKTA in url_actual:
                # Buscar el campo de contraseña para confirmar que estamos en la página correcta
                try:
                    WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located(
                            self.locators.OKTA_CAMPO_CONTRASENA
                        )
                    )
                    self.logger.info("✅ Página de contraseña de OKTA detectada")
                    self._capturar_screenshot("pagina_contrasena_okta_cargada")
                    return True
                except TimeoutException:
                    self.logger.warning("⚠️ No se detectó campo de contraseña en OKTA")
                    self._capturar_screenshot("sin_campo_contrasena")
                    return False
            else:
                self.logger.warning(
                    f"⚠️ No se detectó página de OKTA. URL: {url_actual}"
                )
                self._capturar_screenshot("pagina_no_okta_contrasena")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando página de contraseña de OKTA: {e}")
            self._capturar_screenshot("error_verificacion_contrasena_okta")
            return False

    def ingresar_contrasena_okta(self, contrasena):
        """Ingresa la contraseña en el campo de OKTA"""
        try:
            self.logger.info("Ingresando contraseña en OKTA...")

            # Buscar el campo de contraseña con timeout ultra corto
            try:
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_CONTRASENA)
                )
                self.logger.info("✅ Campo de contraseña encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        self.locators.OKTA_CAMPO_CONTRASENA_ALT
                    )
                )
                self.logger.info(
                    "✅ Campo de contraseña encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar la contraseña de forma rápida
            campo_contrasena.clear()
            campo_contrasena.send_keys(contrasena)
            self.logger.info("✅ Contraseña ingresada")

            # Capturar screenshot después de ingresar contraseña
            self._capturar_screenshot("contrasena_ingresada_okta")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al encontrar campo de contraseña en OKTA")
            self._capturar_screenshot("error_timeout_campo_contrasena")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error ingresando contraseña en OKTA: {e}")
            self._capturar_screenshot("error_ingresar_contrasena")
            return False

    def hacer_clic_verificar_okta(self):
        """Hace clic en el botón Verificar de OKTA"""
        try:
            self.logger.info("Haciendo clic en botón Verificar de OKTA...")

            # Buscar el botón Verificar con timeout ultra corto
            try:
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR)
                )
                self.logger.info("✅ Botón Verificar encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR_ALT)
                )
                self.logger.info(
                    "✅ Botón Verificar encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_verificar_okta")

            # Hacer clic en el botón inmediatamente
            boton_verificar.click()
            self.logger.info("✅ Clic realizado en botón Verificar")

            # Esperar solo 0.5 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_verificar_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic en botón Verificar")
            self._capturar_screenshot("error_timeout_boton_verificar")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en botón Verificar: {e}")
            self._capturar_screenshot("error_clic_verificar")
            return False

    def ingresar_contrasena_y_clic_verificar_okta(self, contrasena):
        """Ingresa la contraseña y hace clic en Verificar de forma ultra rápida"""
        try:
            self.logger.info(f"Ingresando contraseña y haciendo clic en Verificar...")

            # Buscar el campo de contraseña con timeout ultra corto
            try:
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_CONTRASENA)
                )
                self.logger.info("✅ Campo de contraseña encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        self.locators.OKTA_CAMPO_CONTRASENA_ALT
                    )
                )
                self.logger.info(
                    "✅ Campo de contraseña encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar la contraseña de forma rápida
            campo_contrasena.clear()
            campo_contrasena.send_keys(contrasena)
            self.logger.info("✅ Contraseña ingresada")

            # Capturar screenshot después de ingresar contraseña
            self._capturar_screenshot("contrasena_ingresada_okta")

            # Buscar el botón Verificar con timeout ultra corto
            try:
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR)
                )
                self.logger.info("✅ Botón Verificar encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR_ALT)
                )
                self.logger.info(
                    "✅ Botón Verificar encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_verificar_okta")

            # Hacer clic en el botón inmediatamente
            boton_verificar.click()
            self.logger.info("✅ Clic realizado en botón Verificar")

            # Esperar solo 0.5 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_verificar_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            self.logger.info("✅ Contraseña ingresada y clic en Verificar completado")
            return True

        except TimeoutException:
            self.logger.error("❌ Timeout en ingreso de contraseña y clic en Verificar")
            self._capturar_screenshot("error_timeout_contrasena_verificar")
            return False
        except Exception as e:
            self.logger.error(
                f"❌ Error en ingreso de contraseña y clic en Verificar: {e}"
            )
            self._capturar_screenshot("error_contrasena_verificar")
            return False

    def ingresar_contrasena_y_clic_verificar_okta_ultra_rapido(self, contrasena):
        """Ingresa la contraseña y hace clic en Verificar de forma ULTRA RÁPIDA"""
        try:
            self.logger.info(
                f"Ingresando contraseña y haciendo clic en Verificar ULTRA RÁPIDO: {contrasena}"
            )

            # Buscar el campo de contraseña con timeout ultra corto
            try:
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_CONTRASENA)
                )
                self.logger.info("✅ Campo de contraseña encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        self.locators.OKTA_CAMPO_CONTRASENA_ALT
                    )
                )
                self.logger.info(
                    "✅ Campo de contraseña encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar la contraseña de forma ultra rápida
            campo_contrasena.clear()
            campo_contrasena.send_keys(contrasena)
            self.logger.info("✅ Contraseña ingresada")

            # Capturar screenshot después de ingresar contraseña
            self._capturar_screenshot("contrasena_ingresada_okta")

            # Buscar el botón Verificar con timeout ultra corto
            try:
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR)
                )
                self.logger.info("✅ Botón Verificar encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                try:
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector alternativo"
                    )
                except TimeoutException:
                    # Intentar con selectores más específicos
                    self.logger.info("Intentando con selectores más específicos...")
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(text(), 'Verificar')]")
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector específico"
                    )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_verificar_okta")

            # Hacer clic en el botón inmediatamente usando JavaScript si es necesario
            try:
                boton_verificar.click()
                self.logger.info("✅ Clic realizado en botón Verificar")
            except Exception as e:
                self.logger.info("Intentando clic con JavaScript...")
                self.driver.execute_script("arguments[0].click();", boton_verificar)
                self.logger.info("✅ Clic realizado con JavaScript en botón Verificar")

            # Esperar solo 0.2 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_verificar_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            self.logger.info(
                "✅ Contraseña ingresada y clic en Verificar ULTRA RÁPIDO completado"
            )
            return True

        except TimeoutException:
            self.logger.error(
                "❌ Timeout en ingreso de contraseña y clic en Verificar ULTRA RÁPIDO"
            )
            self._capturar_screenshot("error_timeout_contrasena_verificar_ultra_rapido")
            return False
        except Exception as e:
            self.logger.error(
                f"❌ Error en ingreso de contraseña y clic en Verificar ULTRA RÁPIDO: {e}"
            )
            self._capturar_screenshot("error_contrasena_verificar_ultra_rapido")
            return False

    def hacer_clic_verificar_okta_ultra_rapido(self):
        """Hace clic en el botón Verificar de OKTA de forma ultra rápida"""
        try:
            self.logger.info("Haciendo clic ULTRA RÁPIDO en botón Verificar de OKTA...")

            # Buscar el botón Verificar con timeout ultra corto
            try:
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR)
                )
                self.logger.info("✅ Botón Verificar encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                try:
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector alternativo"
                    )
                except TimeoutException:
                    # Intentar con selectores más específicos
                    self.logger.info("Intentando con selectores más específicos...")
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(text(), 'Verificar')]")
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector específico"
                    )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_verificar_okta")

            # Hacer clic en el botón inmediatamente usando JavaScript si es necesario
            try:
                boton_verificar.click()
                self.logger.info("✅ Clic realizado en botón Verificar")
            except Exception as e:
                self.logger.info("Intentando clic con JavaScript...")
                self.driver.execute_script("arguments[0].click();", boton_verificar)
                self.logger.info("✅ Clic realizado con JavaScript en botón Verificar")

            # Esperar solo 0.2 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_verificar_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic en botón Verificar")
            self._capturar_screenshot("error_timeout_boton_verificar")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en botón Verificar: {e}")
            self._capturar_screenshot("error_clic_verificar")
            return False

    def ingresar_contrasena_y_clic_verificar_okta_selector_especifico(self, contrasena):
        """Ingresa la contraseña y hace clic en Verificar usando el selector específico"""
        try:
            self.logger.info(
                f"Ingresando contraseña y haciendo clic en Verificar con selector específico: {contrasena}"
            )

            # Buscar el campo de contraseña con timeout ultra corto
            try:
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_CONTRASENA)
                )
                self.logger.info("✅ Campo de contraseña encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        self.locators.OKTA_CAMPO_CONTRASENA_ALT
                    )
                )
                self.logger.info(
                    "✅ Campo de contraseña encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar la contraseña de forma ultra rápida
            campo_contrasena.clear()
            campo_contrasena.send_keys(contrasena)
            self.logger.info("✅ Contraseña ingresada")

            # Capturar screenshot después de ingresar contraseña
            self._capturar_screenshot("contrasena_ingresada_okta")

            # Usar el selector específico proporcionado por el usuario
            selector_especifico = (By.XPATH, "//*[@id='form53']/div[2]/input")

            # Buscar el botón Verificar con timeout ultra corto
            try:
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(selector_especifico)
                )
                self.logger.info(
                    "✅ Botón Verificar encontrado con selector específico"
                )
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                try:
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector alternativo"
                    )
                except TimeoutException:
                    # Intentar con el tercer selector
                    self.logger.info("Intentando con tercer selector...")
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT2
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con tercer selector"
                    )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_verificar_okta")

            # Hacer clic en el botón inmediatamente usando JavaScript si es necesario
            try:
                boton_verificar.click()
                self.logger.info("✅ Clic realizado en botón Verificar")
            except Exception as e:
                self.logger.info("Intentando clic con JavaScript...")
                self.driver.execute_script("arguments[0].click();", boton_verificar)
                self.logger.info("✅ Clic realizado con JavaScript en botón Verificar")

            # Esperar solo 0.2 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_verificar_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            self.logger.info(
                "✅ Contraseña ingresada y clic en Verificar con selector específico completado"
            )
            return True

        except TimeoutException:
            self.logger.error(
                "❌ Timeout en ingreso de contraseña y clic en Verificar con selector específico"
            )
            self._capturar_screenshot("error_timeout_contrasena_verificar_especifico")
            return False
        except Exception as e:
            self.logger.error(
                f"❌ Error en ingreso de contraseña y clic en Verificar con selector específico: {e}"
            )
            self._capturar_screenshot("error_contrasena_verificar_especifico")
            return False

    def hacer_clic_verificar_okta_selector_especifico(self):
        """Hace clic en el botón Verificar usando el selector específico proporcionado"""
        try:
            self.logger.info(
                "Haciendo clic en botón Verificar con selector específico..."
            )

            # Usar el selector específico proporcionado por el usuario
            selector_especifico = (By.XPATH, "//*[@id='form53']/div[2]/input")

            # Buscar el botón Verificar con timeout ultra corto
            try:
                boton_verificar = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(selector_especifico)
                )
                self.logger.info(
                    "✅ Botón Verificar encontrado con selector específico"
                )
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                try:
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector alternativo"
                    )
                except TimeoutException:
                    # Intentar con el tercer selector
                    self.logger.info("Intentando con tercer selector...")
                    boton_verificar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT2
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con tercer selector"
                    )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_verificar_okta")

            # Hacer clic en el botón inmediatamente usando JavaScript si es necesario
            try:
                boton_verificar.click()
                self.logger.info("✅ Clic realizado en botón Verificar")
            except Exception as e:
                self.logger.info("Intentando clic con JavaScript...")
                self.driver.execute_script("arguments[0].click();", boton_verificar)
                self.logger.info("✅ Clic realizado con JavaScript en botón Verificar")

            # Esperar solo 0.2 segundos para que se procese
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_verificar_okta")

            # Verificar URL actual
            url_actual = self.driver.current_url
            self.logger.info(f"URL actual después del clic: {url_actual}")

            return True

        except TimeoutException:
            self.logger.error(
                "❌ Timeout al hacer clic en botón Verificar con selector específico"
            )
            self._capturar_screenshot("error_timeout_boton_verificar_especifico")
            return False
        except Exception as e:
            self.logger.error(
                f"❌ Error haciendo clic en botón Verificar con selector específico: {e}"
            )
            self._capturar_screenshot("error_clic_verificar_especifico")
            return False

    def esperar_validacion_manual_2fa(self):
        """Espera a que el usuario valide manualmente la 2FA"""
        try:
            self.logger.info("⏳ Esperando validación manual de 2FA...")

            # Capturar screenshot del estado actual
            self._capturar_screenshot("esperando_validacion_2fa")

            # Mensaje claro en consola para validación manual
            print("\n" + "=" * 60)
            print("🔐 AUTENTICACIÓN MANUAL DE 2FA REQUERIDA")
            print("=" * 60)
            print("📱 Por favor, completa la autenticación de dos factores")
            print("   en el navegador que se abrió automáticamente.")
            print("")
            print("⏳ Esperando a que termines la autenticación manual...")
            print("")
            input("✅ Presiona ENTER cuando hayas terminado la autenticación manual: ")
            print("🚀 Continuando con la automatización...")
            print("=" * 60)

            self.logger.info("✅ Validación manual de 2FA completada, continuando...")

            # Capturar screenshot después de la validación
            self._capturar_screenshot("despues_validacion_2fa")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error en validación manual de 2FA: {e}")
            self._capturar_screenshot("error_validacion_2fa")
            return False

    def verificar_pagina_principal_zucarmex(self):
        """Verifica que estemos en la página principal de Zucarmex"""
        try:
            self.logger.info("Verificando página principal de Zucarmex...")

            # Esperar a que la página cargue - ULTRA RÁPIDO
            time.sleep(1)

            url_actual = self.driver.current_url
            self.logger.info(f"URL actual: {url_actual}")

            # Verificar si estamos en la página principal
            if self.locators.URL_HOME in url_actual:
                self.logger.info("✅ URL de página principal detectada")

                # Verificar elementos de la página principal
                try:
                    WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located(self.locators.BIENVENIDO_TEXTO)
                    )
                    self.logger.info("✅ Texto de bienvenida encontrado")
                except TimeoutException:
                    self.logger.warning("⚠️ No se encontró el texto de bienvenida")

                # Verificar logo de Zulka
                try:
                    WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located(self.locators.ZULKA_LOGO)
                    )
                    self.logger.info("✅ Logo de Zulka encontrado")
                except TimeoutException:
                    self.logger.warning("⚠️ No se encontró el logo de Zulka")

                self._capturar_screenshot("pagina_principal_zucarmex")
                return True

            else:
                self.logger.warning(
                    f"⚠️ No se detectó página principal. URL: {url_actual}"
                )
                self._capturar_screenshot("no_pagina_principal")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando página principal: {e}")
            self._capturar_screenshot("error_verificacion_pagina_principal")
            return False

    def hacer_clic_configurador(self):
        """Hace clic en el menú Configurador"""
        try:
            self.logger.info("🔧 Haciendo clic en Configurador...")

            # Buscar el elemento Configurador con timeout optimizado
            try:
                configurador = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.CONFIGURADOR_MENU)
                )
                self.logger.info("✅ Elemento Configurador encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                configurador = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.CONFIGURADOR_MENU_ALT)
                )
                self.logger.info(
                    "✅ Elemento Configurador encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_configurador")

            # Hacer clic en Configurador
            configurador.click()
            self.logger.info("✅ Clic en Configurador realizado")

            # Espera optimizada para que se expanda el menú
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_configurador")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en Configurador: {e}")
            self._capturar_screenshot("error_clic_configurador")
            return False

    def hacer_clic_gestor_catalogos(self):
        """Hace clic en Gestor de catálogos con tiempos optimizados"""
        try:
            self.logger.info("📋 Haciendo clic en Gestor de catálogos...")

            # Buscar el elemento Gestor de catálogos con timeout reducido
            try:
                gestor = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.GESTOR_CATALOGOS)
                )
                self.logger.info("✅ Elemento Gestor de catálogos encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                gestor = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.GESTOR_CATALOGOS_ALT)
                )
                self.logger.info(
                    "✅ Elemento Gestor de catálogos encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_gestor_catalogos")

            # Hacer clic en Gestor de catálogos
            gestor.click()
            self.logger.info("✅ Clic en Gestor de catálogos realizado")

            # Espera reducida para que se cargue la página
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_gestor_catalogos")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en Gestor de catálogos: {e}")
            self._capturar_screenshot("error_clic_gestor_catalogos")
            return False

    def hacer_clic_nuevo_catalogo(self):
        """Hace clic en NUEVO CATÁLOGO con tiempos optimizados"""
        try:
            self.logger.info("➕ Haciendo clic en NUEVO CATÁLOGO...")

            # Buscar el botón NUEVO CATÁLOGO con timeout reducido
            try:
                nuevo_catalogo = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.BOTON_NUEVO_CATALOGO)
                )
                self.logger.info("✅ Botón NUEVO CATÁLOGO encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                nuevo_catalogo = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(self.locators.BOTON_NUEVO_CATALOGO_ALT)
                )
                self.logger.info(
                    "✅ Botón NUEVO CATÁLOGO encontrado con selector alternativo"
                )

            # Capturar screenshot antes del clic
            self._capturar_screenshot("antes_clic_nuevo_catalogo")

            # Hacer clic en NUEVO CATÁLOGO
            nuevo_catalogo.click()
            self.logger.info("✅ Clic en NUEVO CATÁLOGO realizado")

            # Espera reducida para que se abra el formulario
            time.sleep(0.2)

            # Capturar screenshot después del clic
            self._capturar_screenshot("despues_clic_nuevo_catalogo")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en NUEVO CATÁLOGO: {e}")
            self._capturar_screenshot("error_clic_nuevo_catalogo")
            return False

    def debug_elementos_nuevo_catalogo(self):
        """Debug: Busca todos los elementos posibles para el botón NUEVO CATÁLOGO"""
        try:
            self.logger.info(
                "🔍 DEBUG: Buscando elementos para el botón NUEVO CATÁLOGO..."
            )

            # Lista de selectores a probar
            selectores = [
                (
                    "Botón NUEVO CATÁLOGO",
                    "//button[contains(text(), 'NUEVO CATÁLOGO')]",
                ),
                (
                    "Botón Nuevo Catálogo",
                    "//button[contains(text(), 'Nuevo Catálogo')]",
                ),
                ("Botón Nuevo", "//button[contains(text(), 'Nuevo')]"),
                ("Botón Crear", "//button[contains(text(), 'Crear')]"),
                ("Botón Agregar", "//button[contains(text(), 'Agregar')]"),
                ("CSS nuevo", "button:contains('NUEVO'), button:contains('Nuevo')"),
                ("CSS crear", "button:contains('Crear'), button:contains('Agregar')"),
                ("Input submit", "//input[@type='submit']"),
                ("Botón submit", "//button[@type='submit']"),
            ]

            elementos_encontrados = []

            for nombre, selector in selectores:
                try:
                    if selector.startswith("//"):
                        # XPath
                        elementos = self.driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS
                        elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    if elementos:
                        for i, elemento in enumerate(elementos):
                            try:
                                texto = (
                                    elemento.text
                                    or elemento.get_attribute("value")
                                    or elemento.get_attribute("placeholder")
                                    or "Sin texto"
                                )
                                tag = elemento.tag_name
                                tipo = elemento.get_attribute("type") or "Sin tipo"
                                clase = elemento.get_attribute("class") or "Sin clase"
                                id_elem = elemento.get_attribute("id") or "Sin ID"

                                info = f"{nombre} #{i+1}: tag={tag}, type={tipo}, text='{texto}', class='{clase}', id='{id_elem}'"
                                elementos_encontrados.append(info)
                                self.logger.info(f"✅ {info}")
                            except Exception as e:
                                self.logger.info(
                                    f"⚠️ {nombre} #{i+1}: Error obteniendo info - {e}"
                                )
                    else:
                        self.logger.info(f"❌ {nombre}: No encontrado")

                except Exception as e:
                    self.logger.info(f"❌ {nombre}: Error - {e}")

            # Capturar screenshot para análisis
            self._capturar_screenshot("debug_elementos_nuevo_catalogo")

            return elementos_encontrados

        except Exception as e:
            self.logger.error(f"❌ Error en debug de elementos NUEVO CATÁLOGO: {e}")
            return []

    def hacer_clic_nuevo_catalogo_debug(self):
        """Intenta hacer clic en NUEVO CATÁLOGO con múltiples métodos"""
        try:
            self.logger.info(
                "🔍 Intentando hacer clic en NUEVO CATÁLOGO con múltiples métodos..."
            )

            # Primero hacer debug de elementos
            elementos = self.debug_elementos_nuevo_catalogo()

            # Lista de métodos a probar
            metodos = [
                (
                    "Botón NUEVO CATÁLOGO",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'NUEVO CATÁLOGO')]"
                    ),
                ),
                (
                    "Botón Nuevo Catálogo",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Nuevo Catálogo')]"
                    ),
                ),
                (
                    "Botón Nuevo",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Nuevo')]"
                    ),
                ),
                (
                    "Botón Crear",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Crear')]"
                    ),
                ),
                (
                    "Botón Agregar",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Agregar')]"
                    ),
                ),
                (
                    "CSS nuevo",
                    lambda: self.driver.find_element(
                        By.CSS_SELECTOR,
                        "button:contains('NUEVO'), button:contains('Nuevo')",
                    ),
                ),
            ]

            for nombre, metodo in metodos:
                try:
                    self.logger.info(f"🔄 Probando método: {nombre}")
                    elemento = metodo()

                    if elemento:
                        self.logger.info(f"✅ Elemento encontrado con {nombre}")

                        # Capturar screenshot antes del clic
                        self._capturar_screenshot(
                            f"antes_clic_{nombre.replace(' ', '_')}"
                        )

                        # Intentar clic normal
                        try:
                            elemento.click()
                            self.logger.info(f"✅ Clic exitoso con {nombre}")
                            time.sleep(0.2)
                            self._capturar_screenshot(
                                f"despues_clic_{nombre.replace(' ', '_')}"
                            )
                            return True
                        except Exception as e:
                            self.logger.info(f"⚠️ Clic normal falló con {nombre}: {e}")

                            # Intentar clic con JavaScript
                            try:
                                self.driver.execute_script(
                                    "arguments[0].click();", elemento
                                )
                                self.logger.info(
                                    f"✅ Clic con JavaScript exitoso con {nombre}"
                                )
                                time.sleep(0.2)
                                self._capturar_screenshot(
                                    f"despues_clic_js_{nombre.replace(' ', '_')}"
                                )
                                return True
                            except Exception as e2:
                                self.logger.info(
                                    f"❌ Clic con JavaScript también falló con {nombre}: {e2}"
                                )

                except Exception as e:
                    self.logger.info(f"❌ Método {nombre} falló: {e}")

            self.logger.error(
                "❌ Ningún método funcionó para hacer clic en NUEVO CATÁLOGO"
            )
            return False

        except Exception as e:
            self.logger.error(f"❌ Error en clic debug NUEVO CATÁLOGO: {e}")
            return False

    def debug_elementos_formulario(self):
        """Debug: Busca todos los elementos del formulario"""
        try:
            self.logger.info("🔍 DEBUG: Buscando elementos del formulario...")

            # Buscar todos los inputs
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            self.logger.info(f"📋 Encontrados {len(inputs)} inputs en la página")

            for i, input_elem in enumerate(inputs):
                try:
                    input_type = input_elem.get_attribute("type") or "Sin tipo"
                    input_id = input_elem.get_attribute("id") or "Sin ID"
                    input_class = input_elem.get_attribute("class") or "Sin clase"
                    input_placeholder = (
                        input_elem.get_attribute("placeholder") or "Sin placeholder"
                    )
                    input_name = input_elem.get_attribute("name") or "Sin name"

                    self.logger.info(
                        f"Input #{i+1}: type={input_type}, id={input_id}, class={input_class}, placeholder={input_placeholder}, name={input_name}"
                    )
                except Exception as e:
                    self.logger.info(f"Input #{i+1}: Error obteniendo atributos - {e}")

            # Buscar todos los textareas
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            self.logger.info(f"📋 Encontrados {len(textareas)} textareas en la página")

            for i, textarea in enumerate(textareas):
                try:
                    textarea_id = textarea.get_attribute("id") or "Sin ID"
                    textarea_class = textarea.get_attribute("class") or "Sin clase"
                    textarea_placeholder = (
                        textarea.get_attribute("placeholder") or "Sin placeholder"
                    )
                    textarea_name = textarea.get_attribute("name") or "Sin name"

                    self.logger.info(
                        f"Textarea #{i+1}: id={textarea_id}, class={textarea_class}, placeholder={textarea_placeholder}, name={textarea_name}"
                    )
                except Exception as e:
                    self.logger.info(
                        f"Textarea #{i+1}: Error obteniendo atributos - {e}"
                    )

            # Buscar todos los selects
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            self.logger.info(f"📋 Encontrados {len(selects)} selects en la página")

            for i, select in enumerate(selects):
                try:
                    select_id = select.get_attribute("id") or "Sin ID"
                    select_class = select.get_attribute("class") or "Sin clase"
                    select_name = select.get_attribute("name") or "Sin name"

                    self.logger.info(
                        f"Select #{i+1}: id={select_id}, class={select_class}, name={select_name}"
                    )
                except Exception as e:
                    self.logger.info(f"Select #{i+1}: Error obteniendo atributos - {e}")

            # Buscar todos los elementos li (opciones de dropdown)
            lis = self.driver.find_elements(By.TAG_NAME, "li")
            self.logger.info(f"📋 Encontrados {len(lis)} elementos li en la página")

            for i, li in enumerate(lis[:10]):  # Solo mostrar los primeros 10
                try:
                    li_id = li.get_attribute("id") or "Sin ID"
                    li_class = li.get_attribute("class") or "Sin clase"
                    li_text = li.text or "Sin texto"
                    li_data_value = li.get_attribute("data-value") or "Sin data-value"
                    li_role = li.get_attribute("role") or "Sin role"

                    self.logger.info(
                        f"Li #{i+1}: id={li_id}, class={li_class}, text='{li_text}', data-value={li_data_value}, role={li_role}"
                    )
                except Exception as e:
                    self.logger.info(f"Li #{i+1}: Error obteniendo atributos - {e}")

            # Capturar screenshot del debug
            self._capturar_screenshot("debug_elementos_formulario")

        except Exception as e:
            self.logger.error(f"❌ Error en debug de elementos del formulario: {e}")

    def llenar_campo_nombre_debug(self, texto="Test"):
        """Llena el campo Nombre con debug para encontrar el elemento correcto"""
        try:
            self.logger.info(f"📝 Llenando campo Nombre con debug: {texto}")

            # Primero hacer debug de elementos
            self.debug_elementos_formulario()

            # Intentar múltiples selectores para el campo Nombre
            selectores_nombre = [
                (By.XPATH, "//*[@id='«rb»']"),
                (By.XPATH, "//input[@placeholder='Nombre']"),
                (By.XPATH, "//input[@name='nombre']"),
                (By.XPATH, "//input[contains(@class, 'nombre')]"),
                (By.XPATH, "//input[contains(@id, 'nombre')]"),
                (By.XPATH, "//input[@type='text'][1]"),
                (By.XPATH, "//input[not(@type='hidden')][1]"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.CSS_SELECTOR, "input:not([type='hidden'])"),
            ]

            campo_nombre = None
            selector_usado = None

            for selector in selectores_nombre:
                try:
                    self.logger.info(f"🔍 Probando selector: {selector}")
                    campo_nombre = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    selector_usado = selector
                    self.logger.info(
                        f"✅ Campo Nombre encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not campo_nombre:
                self.logger.error(
                    "❌ No se pudo encontrar el campo Nombre con ningún selector"
                )
                return False

            # Capturar screenshot antes de llenar
            self._capturar_screenshot("antes_llenar_nombre_debug")

            # Hacer clic en el campo antes de escribir
            campo_nombre.click()
            self.logger.info("✅ Clic en campo Nombre realizado")

            # Limpiar el campo y escribir el texto
            campo_nombre.clear()
            campo_nombre.send_keys(texto)
            self.logger.info(f"✅ Campo Nombre llenado con: {texto}")

            # Capturar screenshot después de llenar
            self._capturar_screenshot("despues_llenar_nombre_debug")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error llenando campo Nombre con debug: {e}")
            self._capturar_screenshot("error_llenar_nombre_debug")
            return False

    def llenar_campo_nombre(self, texto="Test"):
        """Llena el campo Nombre con el texto especificado (primera letra en mayúscula)"""
        return self.llenar_campo_nombre_debug(texto)

    def llenar_campo_descripcion_debug(self, texto="Test"):
        """Llena el campo Descripción con debug para encontrar el elemento correcto"""
        try:
            self.logger.info(f"📝 Llenando campo Descripción con debug: {texto}")

            # Intentar múltiples selectores para el campo Descripción
            selectores_descripcion = [
                (By.XPATH, "//*[@id='«rc»']"),
                (By.XPATH, "//input[@placeholder='Descripción']"),
                (By.XPATH, "//textarea[@placeholder='Descripción']"),
                (By.XPATH, "//input[@name='descripcion']"),
                (By.XPATH, "//textarea[@name='descripcion']"),
                (By.XPATH, "//input[contains(@class, 'descripcion')]"),
                (By.XPATH, "//textarea[contains(@class, 'descripcion')]"),
                (By.XPATH, "//input[contains(@id, 'descripcion')]"),
                (By.XPATH, "//textarea[contains(@id, 'descripcion')]"),
                (By.XPATH, "//input[@type='text'][2]"),
                (By.XPATH, "//textarea[1]"),
                (By.CSS_SELECTOR, "textarea"),
                (By.CSS_SELECTOR, "input[type='text']:nth-of-type(2)"),
            ]

            campo_descripcion = None
            selector_usado = None

            for selector in selectores_descripcion:
                try:
                    self.logger.info(f"🔍 Probando selector descripción: {selector}")
                    campo_descripcion = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    selector_usado = selector
                    self.logger.info(
                        f"✅ Campo Descripción encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not campo_descripcion:
                self.logger.error(
                    "❌ No se pudo encontrar el campo Descripción con ningún selector"
                )
                return False

            # Capturar screenshot antes de llenar
            self._capturar_screenshot("antes_llenar_descripcion_debug")

            # Hacer clic en el campo antes de escribir
            campo_descripcion.click()
            self.logger.info("✅ Clic en campo Descripción realizado")

            # Limpiar el campo y escribir el texto
            campo_descripcion.clear()
            campo_descripcion.send_keys(texto)
            self.logger.info(f"✅ Campo Descripción llenado con: {texto}")

            # Capturar screenshot después de llenar
            self._capturar_screenshot("despues_llenar_descripcion_debug")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error llenando campo Descripción con debug: {e}")
            self._capturar_screenshot("error_llenar_descripcion_debug")
            return False

    def llenar_campo_descripcion(self, texto="Test"):
        """Llena el campo Descripción con el texto especificado (primera letra en mayúscula)"""
        return self.llenar_campo_descripcion_debug(texto)

    def seleccionar_clasificacion_area_debug(self):
        """Selecciona la primera opción de Clasificación de área con debug"""
        try:
            self.logger.info("🔽 Seleccionando Clasificación de área con debug...")

            # Intentar múltiples selectores para el dropdown
            selectores_dropdown = [
                (By.XPATH, "//*[@id='tipo_area']"),
                (By.XPATH, "//select[@name='tipo_area']"),
                (By.XPATH, "//select[contains(@class, 'tipo_area')]"),
                (By.XPATH, "//select[contains(@id, 'tipo')]"),
                (By.XPATH, "//select[contains(@id, 'area')]"),
                (By.XPATH, "//select[1]"),
                (By.CSS_SELECTOR, "select"),
                (By.CSS_SELECTOR, "select:first-of-type"),
            ]

            dropdown_area = None
            for selector in selectores_dropdown:
                try:
                    self.logger.info(f"🔍 Probando selector dropdown: {selector}")
                    dropdown_area = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(f"✅ Dropdown encontrado con selector: {selector}")
                    break
                except:
                    continue

            if not dropdown_area:
                self.logger.error(
                    "❌ No se pudo encontrar el dropdown de Clasificación de área"
                )
                return False

            # Capturar screenshot antes de abrir dropdown
            self._capturar_screenshot("antes_abrir_dropdown_area_debug")

            # Hacer clic en el dropdown para abrirlo
            dropdown_area.click()
            self.logger.info("✅ Dropdown Clasificación de área abierto")

            # Esperar un momento para que se abra
            time.sleep(0.2)

            # Intentar múltiples selectores para la opción
            selectores_opcion = [
                (By.XPATH, "//*[@id='«rn»']/li[2]"),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Crédito')]",
                ),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiMenuItem-root') and @data-value='1']",
                ),
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root')][2]"),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiButtonBase-root') and contains(text(), 'Crédito')]",
                ),
                (By.XPATH, "//li[2]"),
                (By.XPATH, "//option[2]"),
                (By.CSS_SELECTOR, "li.MuiMenuItem-root:nth-child(2)"),
                (By.CSS_SELECTOR, "li:nth-child(2)"),
            ]

            opcion_area = None
            for selector in selectores_opcion:
                try:
                    self.logger.info(f"🔍 Probando selector opción: {selector}")
                    opcion_area = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(f"✅ Opción encontrada con selector: {selector}")
                    break
                except:
                    continue

            if not opcion_area:
                self.logger.error(
                    "❌ No se pudo encontrar la opción de Clasificación de área"
                )
                return False

            # Hacer clic en la opción usando JavaScript para evitar interceptación
            try:
                opcion_area.click()
                self.logger.info("✅ Opción de Clasificación de área seleccionada")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Clic normal falló, intentando con JavaScript: {e}"
                )
                self.driver.execute_script("arguments[0].click();", opcion_area)
                self.logger.info(
                    "✅ Opción de Clasificación de área seleccionada con JavaScript"
                )

            # Hacer clic en otro lado de la página para cerrar el dropdown
            self.driver.find_element(By.TAG_NAME, "body").click()
            self.logger.info("✅ Clic en otro lado para cerrar dropdown")

            # Capturar screenshot después de seleccionar
            self._capturar_screenshot("despues_seleccionar_area_debug")

            return True

        except Exception as e:
            self.logger.error(
                f"❌ Error seleccionando Clasificación de área con debug: {e}"
            )
            self._capturar_screenshot("error_seleccionar_area_debug")
            return False

    def seleccionar_clasificacion_area(self):
        """Selecciona la primera opción de Clasificación de área"""
        return self.seleccionar_clasificacion_area_debug()

    def seleccionar_tipo_clasificacion_debug(self):
        """Selecciona la primera opción de Tipo de Clasificación con debug"""
        try:
            self.logger.info("🔽 Seleccionando Tipo de Clasificación con debug...")

            # Intentar múltiples selectores para el dropdown
            selectores_dropdown = [
                (By.XPATH, "//*[@id='clasificacion_id']"),
                (By.XPATH, "//select[@name='clasificacion_id']"),
                (By.XPATH, "//select[contains(@class, 'clasificacion')]"),
                (By.XPATH, "//select[contains(@id, 'clasificacion')]"),
                (By.XPATH, "//select[contains(@id, 'tipo')]"),
                (By.XPATH, "//select[2]"),
                (By.CSS_SELECTOR, "select:nth-of-type(2)"),
                (By.CSS_SELECTOR, "select:last-of-type"),
            ]

            dropdown_tipo = None
            for selector in selectores_dropdown:
                try:
                    self.logger.info(f"🔍 Probando selector dropdown tipo: {selector}")
                    dropdown_tipo = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Dropdown tipo encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not dropdown_tipo:
                self.logger.error(
                    "❌ No se pudo encontrar el dropdown de Tipo de Clasificación"
                )
                return False

            # Capturar screenshot antes de abrir dropdown
            self._capturar_screenshot("antes_abrir_dropdown_tipo_debug")

            # Hacer clic en el dropdown para abrirlo
            dropdown_tipo.click()
            self.logger.info("✅ Dropdown Tipo de Clasificación abierto")

            # Esperar un momento para que se abra
            time.sleep(0.2)

            # Intentar múltiples selectores para la opción
            selectores_opcion = [
                (By.XPATH, "//*[@id='«ro»']/li[2]"),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Global')]",
                ),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiMenuItem-root') and @data-value='1']",
                ),
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root')][2]"),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiButtonBase-root') and contains(text(), 'Global')]",
                ),
                (By.XPATH, "//li[2]"),
                (By.XPATH, "//option[2]"),
                (By.CSS_SELECTOR, "li.MuiMenuItem-root:nth-child(2)"),
                (By.CSS_SELECTOR, "li:nth-child(2)"),
            ]

            opcion_tipo = None
            for selector in selectores_opcion:
                try:
                    self.logger.info(f"🔍 Probando selector opción tipo: {selector}")
                    opcion_tipo = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Opción tipo encontrada con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not opcion_tipo:
                self.logger.error(
                    "❌ No se pudo encontrar la opción de Tipo de Clasificación"
                )
                return False

            # Hacer clic en la opción usando JavaScript para evitar interceptación
            try:
                opcion_tipo.click()
                self.logger.info("✅ Opción de Tipo de Clasificación seleccionada")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Clic normal falló, intentando con JavaScript: {e}"
                )
                self.driver.execute_script("arguments[0].click();", opcion_tipo)
                self.logger.info(
                    "✅ Opción de Tipo de Clasificación seleccionada con JavaScript"
                )

            # Hacer clic en otro lado de la página para cerrar el dropdown
            self.driver.find_element(By.TAG_NAME, "body").click()
            self.logger.info("✅ Clic en otro lado para cerrar dropdown")

            # Capturar screenshot después de seleccionar
            self._capturar_screenshot("despues_seleccionar_tipo_debug")

            return True

        except Exception as e:
            self.logger.error(
                f"❌ Error seleccionando Tipo de Clasificación con debug: {e}"
            )
            self._capturar_screenshot("error_seleccionar_tipo_debug")
            return False

    def seleccionar_tipo_clasificacion(self):
        """Selecciona la primera opción de Tipo de Clasificación"""
        return self.seleccionar_tipo_clasificacion_debug()

    def llenar_formulario_completo(self):
        """Llena el formulario completo con todos los campos"""
        try:
            self.logger.info("📋 Llenando formulario completo de Nuevo Catálogo...")

            # Llenar campo Nombre
            if not self.llenar_campo_nombre("Test"):
                return False

            # Llenar campo Descripción
            if not self.llenar_campo_descripcion("Test"):
                return False

            # Seleccionar Clasificación de área
            if not self.seleccionar_clasificacion_area():
                return False

            # Seleccionar Tipo de Clasificación
            if not self.seleccionar_tipo_clasificacion():
                return False

            self.logger.info("✅ Formulario completo llenado exitosamente")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error llenando formulario completo: {e}")
            self._capturar_screenshot("error_formulario_completo")
            return False

    def guardar_datos_generales_debug(self):
        """Guarda los datos generales del formulario con debug"""
        try:
            self.logger.info("💾 Guardando datos generales con debug...")

            # Esperar 5 segundos antes de guardar
            self.logger.info("⏳ Esperando 5 segundos antes de guardar...")
            time.sleep(5)

            # Intentar múltiples selectores para el botón
            selectores_boton = [
                (
                    By.XPATH,
                    "//*[@id='custom-tabpanel-0']/div/div/div/form/div[2]/button",
                ),
                (By.XPATH, "//button[contains(text(), 'Guardar')]"),
                (By.XPATH, "//button[contains(text(), 'guardar')]"),
                (By.XPATH, "//button[contains(text(), 'GUARDAR')]"),
                (By.XPATH, "//button[contains(text(), 'Datos Generales')]"),
                (By.XPATH, "//button[contains(@class, 'guardar')]"),
                (By.XPATH, "//button[contains(@class, 'save')]"),
                (By.XPATH, "//button[@type='submit']"),
                (
                    By.XPATH,
                    "//button[contains(@class, 'MuiButton') and contains(@class, 'MuiButton-contained')]",
                ),
                (
                    By.XPATH,
                    "//button[contains(@class, 'MuiButton') and not(contains(@class, 'MuiIconButton'))]",
                ),
                (By.XPATH, "//button[not(contains(@class, 'MuiIconButton'))]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "button.MuiButton-contained"),
                (By.CSS_SELECTOR, "button:not(.MuiIconButton)"),
            ]

            boton_guardar = None
            for selector in selectores_boton:
                try:
                    self.logger.info(f"🔍 Probando selector botón: {selector}")
                    boton_guardar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(f"✅ Botón encontrado con selector: {selector}")
                    break
                except:
                    continue

            if not boton_guardar:
                self.logger.error(
                    "❌ No se pudo encontrar el botón Guardar Datos Generales"
                )
                return False

            # Capturar screenshot antes de guardar
            self._capturar_screenshot("antes_guardar_datos_debug")

            # Hacer clic en el botón usando JavaScript para evitar interceptación
            try:
                boton_guardar.click()
                self.logger.info("✅ Clic en Guardar Datos Generales realizado")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Clic normal falló, intentando con JavaScript: {e}"
                )
                self.driver.execute_script("arguments[0].click();", boton_guardar)
                self.logger.info(
                    "✅ Clic en Guardar Datos Generales realizado con JavaScript"
                )

            # Esperar un momento para que se procese
            time.sleep(0.2)

            # Capturar screenshot después de guardar
            self._capturar_screenshot("despues_guardar_datos_debug")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error guardando datos generales con debug: {e}")
            self._capturar_screenshot("error_guardar_datos_debug")
            return False

    def guardar_datos_generales(self):
        """Guarda los datos generales del formulario"""
        return self.guardar_datos_generales_debug()

    def llenar_campo_nombre_tecnico_debug(self, texto="Test"):
        """Llena el campo Nombre Técnico con debug para encontrar el elemento correcto"""
        try:
            self.logger.info(f"📝 Llenando campo Nombre Técnico con debug: {texto}")

            # Intentar múltiples selectores para el campo Nombre Técnico
            selectores_nombre_tecnico = [
                (By.XPATH, "//*[@id='«r2n»']"),
                (By.XPATH, "//input[@name='atributos_catalogo[0].nombre_atributo']"),
                (By.XPATH, "//input[contains(@name, 'nombre_atributo')]"),
                (
                    By.XPATH,
                    "//input[contains(@class, 'MuiInputBase-input') and contains(@name, 'atributos_catalogo')]",
                ),
                (By.XPATH, "//input[@type='text'][1]"),
                (By.CSS_SELECTOR, "input[name*='nombre_atributo']"),
            ]

            campo_nombre_tecnico = None
            for selector in selectores_nombre_tecnico:
                try:
                    self.logger.info(f"🔍 Probando selector nombre técnico: {selector}")
                    campo_nombre_tecnico = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Campo Nombre Técnico encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not campo_nombre_tecnico:
                self.logger.error("❌ No se pudo encontrar el campo Nombre Técnico")
                return False

            # Capturar screenshot antes de llenar
            self._capturar_screenshot("antes_llenar_nombre_tecnico_debug")

            # Hacer clic en el campo antes de escribir
            campo_nombre_tecnico.click()
            self.logger.info("✅ Clic en campo Nombre Técnico realizado")

            # Limpiar el campo y escribir el texto
            campo_nombre_tecnico.clear()
            campo_nombre_tecnico.send_keys(texto)
            self.logger.info(f"✅ Campo Nombre Técnico llenado con: {texto}")

            # Capturar screenshot después de llenar
            self._capturar_screenshot("despues_llenar_nombre_tecnico_debug")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error llenando campo Nombre Técnico con debug: {e}")
            self._capturar_screenshot("error_llenar_nombre_tecnico_debug")
            return False

    def llenar_campo_etiqueta_debug(self, texto="Test"):
        """Llena el campo Etiqueta con debug para encontrar el elemento correcto"""
        try:
            self.logger.info(f"📝 Llenando campo Etiqueta con debug: {texto}")

            # Intentar múltiples selectores para el campo Etiqueta
            selectores_etiqueta = [
                (By.XPATH, "//*[@id='«r2o»']"),
                (By.XPATH, "//input[@name='atributos_catalogo[0].etiqueta']"),
                (By.XPATH, "//input[contains(@name, 'etiqueta')]"),
                (
                    By.XPATH,
                    "//input[contains(@class, 'MuiInputBase-input') and contains(@name, 'atributos_catalogo')][2]",
                ),
                (By.XPATH, "//input[@type='text'][2]"),
                (By.CSS_SELECTOR, "input[name*='etiqueta']"),
            ]

            campo_etiqueta = None
            for selector in selectores_etiqueta:
                try:
                    self.logger.info(f"🔍 Probando selector etiqueta: {selector}")
                    campo_etiqueta = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Campo Etiqueta encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not campo_etiqueta:
                self.logger.error("❌ No se pudo encontrar el campo Etiqueta")
                return False

            # Capturar screenshot antes de llenar
            self._capturar_screenshot("antes_llenar_etiqueta_debug")

            # Hacer clic en el campo antes de escribir
            campo_etiqueta.click()
            self.logger.info("✅ Clic en campo Etiqueta realizado")

            # Limpiar el campo y escribir el texto
            campo_etiqueta.clear()
            campo_etiqueta.send_keys(texto)
            self.logger.info(f"✅ Campo Etiqueta llenado con: {texto}")

            # Capturar screenshot después de llenar
            self._capturar_screenshot("despues_llenar_etiqueta_debug")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error llenando campo Etiqueta con debug: {e}")
            self._capturar_screenshot("error_llenar_etiqueta_debug")
            return False

    def seleccionar_tipo_dato_debug(self):
        """Selecciona la primera opción de Tipo de Dato con debug"""
        try:
            self.logger.info("🔽 Seleccionando Tipo de Dato con debug...")

            # Intentar múltiples selectores para el dropdown
            selectores_dropdown = [
                (By.XPATH, "//*[@id='tipoDato-0']"),
                (By.XPATH, "//div[@id='tipoDato-0']"),
                (
                    By.XPATH,
                    "//div[contains(@class, 'MuiSelect-select') and contains(@id, 'tipoDato')]",
                ),
                (By.XPATH, "//div[@role='combobox' and contains(@id, 'tipoDato')]"),
                (By.XPATH, "//input[@name='atributos_catalogo[0].tipo_dato']"),
                (By.XPATH, "//input[contains(@name, 'tipo_dato')]"),
                (By.XPATH, "//input[contains(@class, 'MuiSelect-nativeInput')]"),
                (By.CSS_SELECTOR, "div#tipoDato-0"),
                (By.CSS_SELECTOR, "div[role='combobox']"),
            ]

            dropdown_tipo_dato = None
            for selector in selectores_dropdown:
                try:
                    self.logger.info(
                        f"🔍 Probando selector dropdown tipo dato: {selector}"
                    )
                    dropdown_tipo_dato = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Dropdown Tipo de Dato encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not dropdown_tipo_dato:
                self.logger.error("❌ No se pudo encontrar el dropdown de Tipo de Dato")
                return False

            # Capturar screenshot antes de abrir dropdown
            self._capturar_screenshot("antes_abrir_dropdown_tipo_dato_debug")

            # Hacer clic en el dropdown para abrirlo
            dropdown_tipo_dato.click()
            self.logger.info("✅ Dropdown Tipo de Dato abierto")

            # Esperar un momento para que se abra
            time.sleep(0.2)

            # Intentar múltiples selectores para la opción
            selectores_opcion = [
                (By.XPATH, "//*[@id='«r18»']/li[2]"),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiMenuItem-root') and contains(text(), 'Texto')]",
                ),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiMenuItem-root') and @data-value='String']",
                ),
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root')][2]"),
                (
                    By.XPATH,
                    "//li[contains(@class, 'MuiButtonBase-root') and contains(text(), 'Texto')]",
                ),
                (
                    By.XPATH,
                    "//li[contains(@class, 'Mui-selected') and contains(text(), 'Texto')]",
                ),
                (By.XPATH, "//li[2]"),
                (By.CSS_SELECTOR, "li.MuiMenuItem-root:nth-child(2)"),
                (By.CSS_SELECTOR, "li:nth-child(2)"),
            ]

            opcion_tipo_dato = None
            for selector in selectores_opcion:
                try:
                    self.logger.info(
                        f"🔍 Probando selector opción tipo dato: {selector}"
                    )
                    opcion_tipo_dato = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Opción Tipo de Dato encontrada con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not opcion_tipo_dato:
                self.logger.error("❌ No se pudo encontrar la opción de Tipo de Dato")
                return False

            # Hacer clic en la opción usando JavaScript para evitar interceptación
            try:
                opcion_tipo_dato.click()
                self.logger.info("✅ Opción de Tipo de Dato seleccionada")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Clic normal falló, intentando con JavaScript: {e}"
                )
                self.driver.execute_script("arguments[0].click();", opcion_tipo_dato)
                self.logger.info(
                    "✅ Opción de Tipo de Dato seleccionada con JavaScript"
                )

            # Hacer clic en otro lado de la página para cerrar el dropdown
            self.driver.find_element(By.TAG_NAME, "body").click()
            self.logger.info("✅ Clic en otro lado para cerrar dropdown")

            # Capturar screenshot después de seleccionar
            self._capturar_screenshot("despues_seleccionar_tipo_dato_debug")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error seleccionando Tipo de Dato con debug: {e}")
            self._capturar_screenshot("error_seleccionar_tipo_dato_debug")
            return False

    def debug_elementos_estructura_catalogo(self):
        """Debug: Busca todos los elementos disponibles en la página de estructura del catálogo"""
        try:
            self.logger.info(
                "🔍 DEBUG: Buscando elementos de estructura del catálogo..."
            )

            # Buscar todos los inputs
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            self.logger.info(
                f"📝 Encontrados {len(inputs)} elementos input en la página"
            )

            for i, input_elem in enumerate(inputs[:10]):  # Solo mostrar los primeros 10
                try:
                    name = input_elem.get_attribute("name") or "sin_name"
                    id_attr = input_elem.get_attribute("id") or "sin_id"
                    type_attr = input_elem.get_attribute("type") or "sin_type"
                    class_attr = input_elem.get_attribute("class") or "sin_class"
                    self.logger.info(
                        f"Input #{i+1}: name='{name}', id='{id_attr}', type='{type_attr}', class='{class_attr[:50]}...'"
                    )
                except Exception as e:
                    self.logger.info(f"Input #{i+1}: Error obteniendo atributos - {e}")

            # Buscar todos los elementos select
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            self.logger.info(
                f"🔽 Encontrados {len(selects)} elementos select en la página"
            )

            for i, select in enumerate(selects[:5]):  # Solo mostrar los primeros 5
                try:
                    name = select.get_attribute("name") or "sin_name"
                    id_attr = select.get_attribute("id") or "sin_id"
                    class_attr = select.get_attribute("class") or "sin_class"
                    self.logger.info(
                        f"Select #{i+1}: name='{name}', id='{id_attr}', class='{class_attr[:50]}...'"
                    )
                except Exception as e:
                    self.logger.info(f"Select #{i+1}: Error obteniendo atributos - {e}")

            # Buscar todos los elementos li (opciones de dropdown)
            lis = self.driver.find_elements(By.TAG_NAME, "li")
            self.logger.info(f"📋 Encontrados {len(lis)} elementos li en la página")

            for i, li in enumerate(lis[:10]):  # Solo mostrar los primeros 10
                try:
                    text = li.text or "sin_texto"
                    class_attr = li.get_attribute("class") or "sin_class"
                    data_value = li.get_attribute("data-value") or "sin_data_value"
                    self.logger.info(
                        f"Li #{i+1}: text='{text}', class='{class_attr[:50]}...', data-value='{data_value}'"
                    )
                except Exception as e:
                    self.logger.info(f"Li #{i+1}: Error obteniendo atributos - {e}")

            # Capturar screenshot para análisis visual
            self._capturar_screenshot("debug_elementos_estructura_catalogo")

        except Exception as e:
            self.logger.error(f"❌ Error en debug de elementos de estructura: {e}")

    def llenar_estructura_catalogo_completa(self):
        """Llena la estructura completa del catálogo con todos los campos"""
        try:
            self.logger.info("📋 Llenando estructura completa del catálogo...")

            # Debug: Inspeccionar elementos disponibles
            self.debug_elementos_estructura_catalogo()

            # Llenar campo Nombre Técnico
            if not self.llenar_campo_nombre_tecnico_debug("Test"):
                return False

            # Llenar campo Etiqueta
            if not self.llenar_campo_etiqueta_debug("Test"):
                return False

            # Seleccionar Tipo de Dato
            if not self.seleccionar_tipo_dato_debug():
                return False

            self.logger.info("✅ Estructura del catálogo llenada exitosamente")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error llenando estructura del catálogo: {e}")
            self._capturar_screenshot("error_estructura_catalogo_completa")
            return False

    def guardar_estructura_catalogo_debug(self):
        """Guarda la estructura del catálogo con debug"""
        try:
            self.logger.info("💾 Guardando estructura del catálogo con debug...")

            # Esperar 5 segundos antes de guardar
            self.logger.info("⏳ Esperando 5 segundos antes de guardar estructura...")
            time.sleep(5)

            # Intentar múltiples selectores para el botón
            selectores_boton = [
                (By.XPATH, "//*[@id='custom-tabpanel-1']/div/div/form/div[3]/button"),
                (By.XPATH, "//button[contains(text(), 'Guardar estructura')]"),
                (By.XPATH, "//button[contains(text(), 'guardar estructura')]"),
                (By.XPATH, "//button[contains(text(), 'GUARDAR ESTRUCTURA')]"),
                (
                    By.XPATH,
                    "//button[contains(@class, 'MuiButton-contained') and contains(text(), 'Guardar')]",
                ),
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "button.MuiButton-contained"),
            ]

            boton_guardar = None
            for selector in selectores_boton:
                try:
                    self.logger.info(
                        f"🔍 Probando selector botón estructura: {selector}"
                    )
                    boton_guardar = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(selector)
                    )
                    self.logger.info(
                        f"✅ Botón estructura encontrado con selector: {selector}"
                    )
                    break
                except:
                    continue

            if not boton_guardar:
                self.logger.error("❌ No se pudo encontrar el botón Guardar Estructura")
                return False

            # Capturar screenshot antes de guardar
            self._capturar_screenshot("antes_guardar_estructura_debug")

            # Hacer clic en el botón usando JavaScript para evitar interceptación
            try:
                boton_guardar.click()
                self.logger.info("✅ Clic en Guardar Estructura realizado")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Clic normal falló, intentando con JavaScript: {e}"
                )
                self.driver.execute_script("arguments[0].click();", boton_guardar)
                self.logger.info(
                    "✅ Clic en Guardar Estructura realizado con JavaScript"
                )

            # Esperar un momento para que se procese
            time.sleep(0.2)

            # Capturar screenshot después de guardar
            self._capturar_screenshot("despues_guardar_estructura_debug")

            return True

        except Exception as e:
            self.logger.error(
                f"❌ Error guardando estructura del catálogo con debug: {e}"
            )
            self._capturar_screenshot("error_guardar_estructura_debug")
            return False

    def debug_elementos_verificar(self):
        """Debug: Busca todos los elementos posibles para el botón Verificar"""
        try:
            self.logger.info("🔍 DEBUG: Buscando elementos para el botón Verificar...")

            # Lista de selectores a probar
            selectores = [
                ("Selector específico", "//*[@id='form53']/div[2]/input"),
                ("Botón Verificar", "//button[contains(text(), 'Verificar')]"),
                ("Botón Verify", "//button[contains(text(), 'Verify')]"),
                ("Input submit", "//input[@type='submit']"),
                ("Botón submit", "//button[@type='submit']"),
                ("Form input", "//form//input[last()]"),
                ("Form button", "//form//button[last()]"),
                ("CSS submit", "input[type='submit'], button[type='submit']"),
                ("CSS verify", "[class*='verify'], [class*='submit']"),
            ]

            elementos_encontrados = []

            for nombre, selector in selectores:
                try:
                    if selector.startswith("//"):
                        # XPath
                        elementos = self.driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS
                        elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    if elementos:
                        for i, elemento in enumerate(elementos):
                            try:
                                texto = (
                                    elemento.text
                                    or elemento.get_attribute("value")
                                    or elemento.get_attribute("placeholder")
                                    or "Sin texto"
                                )
                                tag = elemento.tag_name
                                tipo = elemento.get_attribute("type") or "Sin tipo"
                                clase = elemento.get_attribute("class") or "Sin clase"
                                id_elem = elemento.get_attribute("id") or "Sin ID"

                                info = f"{nombre} #{i+1}: tag={tag}, type={tipo}, text='{texto}', class='{clase}', id='{id_elem}'"
                                elementos_encontrados.append(info)
                                self.logger.info(f"✅ {info}")
                            except Exception as e:
                                self.logger.info(
                                    f"⚠️ {nombre} #{i+1}: Error obteniendo info - {e}"
                                )
                    else:
                        self.logger.info(f"❌ {nombre}: No encontrado")

                except Exception as e:
                    self.logger.info(f"❌ {nombre}: Error - {e}")

            # Capturar screenshot para análisis
            self._capturar_screenshot("debug_elementos_verificar")

            return elementos_encontrados

        except Exception as e:
            self.logger.error(f"❌ Error en debug de elementos: {e}")
            return []

    def hacer_clic_verificar_debug(self):
        """Intenta hacer clic en Verificar con múltiples métodos"""
        try:
            self.logger.info(
                "🔍 Intentando hacer clic en Verificar con múltiples métodos..."
            )

            # Primero hacer debug de elementos
            elementos = self.debug_elementos_verificar()

            # Lista de métodos a probar
            metodos = [
                (
                    "Selector específico",
                    lambda: self.driver.find_element(
                        By.XPATH, "//*[@id='form53']/div[2]/input"
                    ),
                ),
                (
                    "Botón Verificar",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Verificar')]"
                    ),
                ),
                (
                    "Input submit",
                    lambda: self.driver.find_element(
                        By.XPATH, "//input[@type='submit']"
                    ),
                ),
                (
                    "Botón submit",
                    lambda: self.driver.find_element(
                        By.XPATH, "//button[@type='submit']"
                    ),
                ),
                (
                    "Form input último",
                    lambda: self.driver.find_element(By.XPATH, "//form//input[last()]"),
                ),
                (
                    "Form button último",
                    lambda: self.driver.find_element(
                        By.XPATH, "//form//button[last()]"
                    ),
                ),
            ]

            for nombre, metodo in metodos:
                try:
                    self.logger.info(f"🔄 Probando método: {nombre}")
                    elemento = metodo()

                    if elemento:
                        self.logger.info(f"✅ Elemento encontrado con {nombre}")

                        # Capturar screenshot antes del clic
                        self._capturar_screenshot(
                            f"antes_clic_{nombre.replace(' ', '_')}"
                        )

                        # Intentar clic normal
                        try:
                            elemento.click()
                            self.logger.info(f"✅ Clic exitoso con {nombre}")
                            time.sleep(1)
                            self._capturar_screenshot(
                                f"despues_clic_{nombre.replace(' ', '_')}"
                            )
                            return True
                        except Exception as e:
                            self.logger.info(f"⚠️ Clic normal falló con {nombre}: {e}")

                            # Intentar clic con JavaScript
                            try:
                                self.driver.execute_script(
                                    "arguments[0].click();", elemento
                                )
                                self.logger.info(
                                    f"✅ Clic con JavaScript exitoso con {nombre}"
                                )
                                time.sleep(1)
                                self._capturar_screenshot(
                                    f"despues_clic_js_{nombre.replace(' ', '_')}"
                                )
                                return True
                            except Exception as e2:
                                self.logger.info(
                                    f"❌ Clic con JavaScript también falló con {nombre}: {e2}"
                                )

                except Exception as e:
                    self.logger.info(f"❌ Método {nombre} falló: {e}")

            self.logger.error("❌ Ningún método funcionó para hacer clic en Verificar")
            return False

        except Exception as e:
            self.logger.error(f"❌ Error en clic debug: {e}")
            return False

    def ingresar_contrasena_y_clic_verificar_debug(self, contrasena):
        """Ingresa la contraseña y hace clic en Verificar usando debug"""
        try:
            self.logger.info(
                f"🔍 Ingresando contraseña y haciendo clic en Verificar con debug: {contrasena}"
            )

            # Buscar el campo de contraseña
            try:
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_CONTRASENA)
                )
                self.logger.info("✅ Campo de contraseña encontrado")
            except TimeoutException:
                self.logger.info("Intentando con selector alternativo...")
                campo_contrasena = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        self.locators.OKTA_CAMPO_CONTRASENA_ALT
                    )
                )
                self.logger.info(
                    "✅ Campo de contraseña encontrado con selector alternativo"
                )

            # Limpiar el campo y ingresar la contraseña
            campo_contrasena.clear()
            campo_contrasena.send_keys(contrasena)
            self.logger.info("✅ Contraseña ingresada")

            # Capturar screenshot después de ingresar contraseña
            self._capturar_screenshot("contrasena_ingresada_debug")

            # Usar el método de debug para hacer clic en Verificar
            resultado = self.hacer_clic_verificar_debug()

            if resultado:
                self.logger.info(
                    "✅ Contraseña ingresada y clic en Verificar con debug completado"
                )
                return True
            else:
                self.logger.error("❌ No se pudo hacer clic en Verificar con debug")
                return False

        except Exception as e:
            self.logger.error(
                f"❌ Error en ingreso de contraseña y clic en Verificar con debug: {e}"
            )
            self._capturar_screenshot("error_contrasena_verificar_debug")
            return False

    def _capturar_screenshot(self, nombre_archivo):
        """Captura un screenshot con timestamp en la carpeta de ejecución específica"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Usar la carpeta de ejecución si está configurada, sino usar fallback
            if self.execution_folder:
                screenshot_path = os.path.join(
                    self.execution_folder, f"{nombre_archivo}_{timestamp}.png"
                )
            else:
                # Fallback a estructura antigua
                screenshot_path = f"evidences/{datetime.now().strftime('%Y-%m-%d')}/alta_catalogo/{nombre_archivo}_{timestamp}.png"

            # Crear directorio si no existe
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot capturado: {screenshot_path}")

        except Exception as e:
            self.logger.error(f"❌ Error capturando screenshot: {e}")

    def obtener_estado_pagina(self):
        """Obtiene el estado actual de la página"""
        try:
            estado = {
                "url": self.driver.current_url,
                "titulo": self.driver.title,
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"Estado de la página: {estado}")
            return estado

        except Exception as e:
            self.logger.error(f"❌ Error obteniendo estado de la página: {e}")
            return None
