"""
Page Object para la página de Alta de Zafra
Sistema de Automatización - Zucarmex QA
"""

import logging
import os
import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.US13_8_Crear_y_Configurar_una_Nueva_Zafra_locators import (
    AltaZafraLocators,
)


class AltaZafraPage:
    """Page Object para la página de Alta de Zafra"""

    def __init__(self, driver):
        self.driver = driver
        self.locators = AltaZafraLocators()
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
                f"evidences/{datetime.now().strftime('%Y-%m-%d')}/alta_zafra"
            )

    # Reutilizar métodos de autenticación y navegación básica
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

            # Hacer clic inmediato
            boton_okta.click()
            self.logger.info("✅ Clic inmediato en OKTA realizado")

            # Capturar screenshot después del clic
            self._capturar_screenshot("clic_okta_inmediato")

            return True

        except TimeoutException:
            self.logger.error("❌ Timeout al hacer clic inmediato en OKTA")
            self._capturar_screenshot("error_timeout_clic_okta")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error al hacer clic inmediato en OKTA: {e}")
            self._capturar_screenshot("error_clic_okta")
            return False

    def verificar_redireccion_okta(self):
        """Verifica que se haya producido la redirección a OKTA"""
        try:
            self.logger.info("Verificando redirección a OKTA...")

            # Esperar un momento para que se complete la redirección
            time.sleep(2)

            # Verificar que la URL contenga OKTA
            current_url = self.driver.current_url
            if self.locators.URL_OKTA in current_url:
                self.logger.info(f"✅ Redirección a OKTA confirmada: {current_url}")
                self._capturar_screenshot("redireccion_okta_confirmada")
                return True
            else:
                self.logger.warning(f"⚠️ URL actual no contiene OKTA: {current_url}")
                self._capturar_screenshot("redireccion_okta_no_confirmada")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando redirección a OKTA: {e}")
            self._capturar_screenshot("error_verificacion_redireccion")
            return False

    def verificar_pagina_okta(self):
        """Verifica que estemos en la página de OKTA"""
        try:
            self.logger.info("Verificando página de OKTA...")

            # Buscar elementos característicos de OKTA
            elementos_okta = [
                self.locators.OKTA_TITULO,
                self.locators.OKTA_LOGO_ZUCARMEX,
                self.locators.OKTA_CAMPO_USUARIO,
            ]

            for elemento in elementos_okta:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(elemento)
                    )
                    self.logger.info("✅ Elemento de OKTA encontrado")
                    return True
                except TimeoutException:
                    continue

            self.logger.warning("⚠️ No se encontraron elementos característicos de OKTA")
            return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando página de OKTA: {e}")
            return False

    def ingresar_usuario_y_clic_siguiente_okta(self, usuario):
        """Ingresa el usuario y hace clic en Siguiente de forma ultra rápida"""
        try:
            self.logger.info(
                f"Ingresando usuario y haciendo clic en Siguiente: {usuario}"
            )

            # Buscar campo de usuario
            campo_usuario = None
            try:
                campo_usuario = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_USUARIO)
                )
            except TimeoutException:
                campo_usuario = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_USUARIO_ALT)
                )

            # Limpiar campo e ingresar usuario
            campo_usuario.clear()
            campo_usuario.send_keys(usuario)
            self.logger.info("✅ Usuario ingresado")

            # Buscar botón Siguiente
            boton_siguiente = None
            try:
                boton_siguiente = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_SIGUIENTE)
                )
            except TimeoutException:
                boton_siguiente = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_SIGUIENTE_ALT)
                )

            # Hacer clic en Siguiente
            boton_siguiente.click()
            self.logger.info("✅ Clic en Siguiente realizado")

            # Capturar screenshot
            self._capturar_screenshot("usuario_ingresado_y_siguiente")

            return True

        except Exception as e:
            self.logger.error(
                f"❌ Error ingresando usuario y haciendo clic en Siguiente: {e}"
            )
            self._capturar_screenshot("error_usuario_siguiente")
            return False

    def verificar_pagina_contrasena_okta(self):
        """Verifica que estemos en la página de contraseña de OKTA"""
        try:
            self.logger.info("Verificando página de contraseña de OKTA...")

            # Buscar elementos característicos de la página de contraseña
            elementos_contrasena = [
                self.locators.OKTA_ICONO_CANDADO,
                self.locators.OKTA_TEXTO_VERIFICAR,
                self.locators.OKTA_CAMPO_CONTRASENA,
            ]

            for elemento in elementos_contrasena:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(elemento)
                    )
                    self.logger.info("✅ Elemento de página de contraseña encontrado")
                    return True
                except TimeoutException:
                    continue

            self.logger.warning("⚠️ No se encontraron elementos de página de contraseña")
            return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando página de contraseña: {e}")
            return False

    def ingresar_contrasena_y_clic_verificar_debug(self, contrasena):
        """Ingresa la contraseña y hace clic en Verificar usando debug"""
        try:
            self.logger.info(
                f"Ingresando contraseña y haciendo clic en Verificar con debug: {contrasena}"
            )

            # Buscar campo de contraseña
            campo_contrasena = None
            try:
                campo_contrasena = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(self.locators.OKTA_CAMPO_CONTRASENA)
                )
            except TimeoutException:
                campo_contrasena = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        self.locators.OKTA_CAMPO_CONTRASENA_ALT
                    )
                )

            # Limpiar campo e ingresar contraseña
            campo_contrasena.clear()
            campo_contrasena.send_keys(contrasena)
            self.logger.info("✅ Contraseña ingresada")

            # Buscar botón Verificar con selector específico
            boton_verificar = None
            try:
                boton_verificar = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.locators.OKTA_BOTON_VERIFICAR)
                )
                self.logger.info(
                    "✅ Botón Verificar encontrado con selector específico"
                )
            except TimeoutException:
                try:
                    boton_verificar = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con selector alternativo"
                    )
                except TimeoutException:
                    boton_verificar = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(
                            self.locators.OKTA_BOTON_VERIFICAR_ALT2
                        )
                    )
                    self.logger.info(
                        "✅ Botón Verificar encontrado con segundo selector alternativo"
                    )

            # Hacer clic en Verificar
            boton_verificar.click()
            self.logger.info("✅ Clic en Verificar realizado")

            # Capturar screenshot
            self._capturar_screenshot("contrasena_ingresada_y_verificar")

            return True

        except Exception as e:
            self.logger.error(
                f"❌ Error ingresando contraseña y haciendo clic en Verificar: {e}"
            )
            self._capturar_screenshot("error_contrasena_verificar")
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

            # Buscar elementos característicos de la página principal
            elementos_principales = [
                self.locators.ZULKA_LOGO,
                self.locators.BIENVENIDO_TEXTO,
                self.locators.NAVEGACION_CONFIGURACION,
            ]

            elementos_encontrados = 0
            for elemento in elementos_principales:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(elemento)
                    )
                    elementos_encontrados += 1
                    self.logger.info("✅ Elemento de página principal encontrado")
                except TimeoutException:
                    self.logger.warning(f"⚠️ Elemento no encontrado: {elemento}")

            # Capturar screenshot de la página principal
            self._capturar_screenshot("pagina_principal_zucarmex")

            if elementos_encontrados > 0:
                self.logger.info(
                    f"✅ Página principal verificada ({elementos_encontrados} elementos encontrados)"
                )
                return True
            else:
                self.logger.warning("⚠️ No se encontraron elementos de página principal")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error verificando página principal: {e}")
            self._capturar_screenshot("error_verificacion_pagina_principal")
            return False

    def hacer_clic_configuracion(self):
        """Hace clic en el menú Configuración"""
        try:
            self.logger.info("Haciendo clic en Configuración...")

            # Buscar el elemento de Configuración
            elemento_configuracion = None
            try:
                elemento_configuracion = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators.CONFIGURACION_MENU)
                )
                self.logger.info("✅ Elemento Configuración encontrado")
            except TimeoutException:
                elemento_configuracion = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators.CONFIGURACION_MENU_ALT)
                )
                self.logger.info(
                    "✅ Elemento Configuración encontrado con selector alternativo"
                )

            # Hacer clic en Configuración
            elemento_configuracion.click()
            self.logger.info("✅ Clic en Configuración realizado exitosamente")

            # Capturar screenshot después del clic
            self._capturar_screenshot("clic_configuracion_realizado")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en Configuración: {e}")
            self._capturar_screenshot("error_clic_configuracion")
            return False

    def hacer_clic_zafras(self):
        """Hace clic en el submenú Zafras"""
        try:
            self.logger.info("Haciendo clic en Zafras...")

            # Buscar el elemento de Zafras
            elemento_zafras = None
            try:
                elemento_zafras = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators.ZAFRAS_MENU)
                )
                self.logger.info("✅ Elemento Zafras encontrado")
            except TimeoutException:
                elemento_zafras = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators.ZAFRAS_MENU_ALT)
                )
                self.logger.info(
                    "✅ Elemento Zafras encontrado con selector alternativo"
                )

            # Hacer clic en Zafras
            elemento_zafras.click()
            self.logger.info("✅ Clic en Zafras realizado exitosamente")

            # Capturar screenshot después del clic
            self._capturar_screenshot("clic_zafras_realizado")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en Zafras: {e}")
            self._capturar_screenshot("error_clic_zafras")
            return False

    def hacer_clic_nueva_zafra(self):
        """Hace clic en el botón Nueva zafra"""
        try:
            self.logger.info("Haciendo clic en Nueva zafra...")

            # Buscar el botón Nueva zafra
            boton_nueva_zafra = None
            try:
                boton_nueva_zafra = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators.BOTON_NUEVA_ZAFRA)
                )
                self.logger.info("✅ Botón Nueva zafra encontrado")
            except TimeoutException:
                boton_nueva_zafra = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators.BOTON_NUEVA_ZAFRA_ALT)
                )
                self.logger.info(
                    "✅ Botón Nueva zafra encontrado con selector alternativo"
                )

            # Hacer clic en Nueva zafra
            boton_nueva_zafra.click()
            self.logger.info("✅ Clic en Nueva zafra realizado exitosamente")

            # Capturar screenshot después del clic
            self._capturar_screenshot("clic_nueva_zafra_realizado")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error haciendo clic en Nueva zafra: {e}")
            self._capturar_screenshot("error_clic_nueva_zafra")
            return False

    def verificar_elementos_pagina(self):
        """Verifica que los elementos de la página estén presentes"""
        try:
            self.logger.info("Verificando elementos de la página...")

            elementos_verificar = [
                self.locators.LOGO_ZULKA,
                self.locators.BOTON_OKTA,
                self.locators.TARJETA_LOGIN,
            ]

            elementos_encontrados = 0
            for elemento in elementos_verificar:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(elemento)
                    )
                    elementos_encontrados += 1
                except TimeoutException:
                    continue

            self.logger.info(
                f"✅ Elementos verificados: {elementos_encontrados}/{len(elementos_verificar)}"
            )
            return elementos_encontrados > 0

        except Exception as e:
            self.logger.error(f"❌ Error verificando elementos: {e}")
            return False

    def obtener_estado_pagina(self):
        """Obtiene el estado actual de la página"""
        try:
            estado = {
                "url": self.driver.current_url,
                "titulo": self.driver.title,
                "timestamp": datetime.now().isoformat(),
            }
            return estado
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo estado de página: {e}")
            return None

    def _capturar_screenshot(self, nombre_archivo):
        """Captura un screenshot y lo guarda en la carpeta de evidencias"""
        try:
            if not self.execution_folder:
                self.execution_folder = (
                    f"evidences/{datetime.now().strftime('%Y-%m-%d')}/alta_zafra"
                )

            # Crear directorio si no existe
            os.makedirs(self.execution_folder, exist_ok=True)

            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.png"
            ruta_completa = os.path.join(self.execution_folder, nombre_completo)

            # Capturar screenshot
            self.driver.save_screenshot(ruta_completa)
            self.logger.info(f"📸 Screenshot capturado: {ruta_completa}")

        except Exception as e:
            self.logger.error(f"❌ Error capturando screenshot: {e}")
