from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from locators.catalogo_locators import CatalogoLocators
import logging
import time

class CatalogoPage:
    """Page Object para la funcionalidad de catálogos"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(__name__)
    
    def debug_menu_elements(self):
        """Método de debug para verificar elementos del menú"""
        try:
            self.logger.info("=== DEBUG: Elementos del menú ===")
            self.logger.info(f"URL actual: {self.driver.current_url}")
            self.logger.info(f"Título de la página: {self.driver.title}")
            
            # Buscar todos los elementos que contengan "Configurador"
            try:
                configurador_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Configurador')]")
                self.logger.info(f"Encontrados {len(configurador_elements)} elementos con 'Configurador':")
                for i, elem in enumerate(configurador_elements):
                    self.logger.info(f"  Elemento {i+1}: tag='{elem.tag_name}', text='{elem.text}', visible={elem.is_displayed()}")
            except Exception as e:
                self.logger.warning(f"Error buscando elementos Configurador: {str(e)}")
            
            # Buscar todos los elementos que contengan "Gestor de catálogos"
            try:
                gestor_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Gestor de catálogos')]")
                self.logger.info(f"Encontrados {len(gestor_elements)} elementos con 'Gestor de catálogos':")
                for i, elem in enumerate(gestor_elements):
                    self.logger.info(f"  Elemento {i+1}: tag='{elem.tag_name}', text='{elem.text}', visible={elem.is_displayed()}")
            except Exception as e:
                self.logger.warning(f"Error buscando elementos Gestor de catálogos: {str(e)}")
            
            # Buscar todos los elementos que contengan "Catálogos"
            try:
                catalogos_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Catálogos')]")
                self.logger.info(f"Encontrados {len(catalogos_elements)} elementos con 'Catálogos':")
                for i, elem in enumerate(catalogos_elements):
                    self.logger.info(f"  Elemento {i+1}: tag='{elem.tag_name}', text='{elem.text}', visible={elem.is_displayed()}")
            except Exception as e:
                self.logger.warning(f"Error buscando elementos Catálogos: {str(e)}")
            
            self.logger.info("=== FIN DEBUG MENÚ ===")
        except Exception as e:
            self.logger.error(f"Error en debug del menú: {str(e)}")
    
    def expand_configurador_menu(self):
        """Intenta expandir el menú Configurador si está colapsado"""
        try:
            self.logger.info("Verificando si el menú Configurador necesita expansión...")
            
            # Buscar indicadores de menú colapsado (flechas, iconos de expansión)
            expand_selectors = [
                "//span[contains(text(),'Configurador')]/following-sibling::*[contains(@class,'arrow') or contains(@class,'chevron') or contains(@class,'expand')]",
                "//span[contains(text(),'Configurador')]/parent::*/following-sibling::*[contains(@class,'arrow') or contains(@class,'chevron')]",
                "//div[contains(text(),'Configurador')]/following-sibling::*[contains(@class,'arrow') or contains(@class,'chevron')]"
            ]
            
            for selector in expand_selectors:
                try:
                    expand_element = self.driver.find_element(By.XPATH, selector)
                    if expand_element.is_displayed() and expand_element.is_enabled():
                        expand_element.click()
                        self.logger.info("✅ Menú Configurador expandido")
                        time.sleep(1)
                        return True
                except:
                    continue
            
            self.logger.info("No se encontró indicador de expansión o ya está expandido")
            return True
            
        except Exception as e:
            self.logger.warning(f"Error expandiendo menú Configurador: {str(e)}")
            return True  # Continuar aunque falle la expansión
    
    def navigate_to_catalogos(self):
        """Navega al menú Configurador > Gestor de catálogos"""
        try:
            self.logger.info("Iniciando navegación a Gestor de catálogos...")
            
            # Debug: Verificar elementos del menú antes de navegar
            self.debug_menu_elements()
            
            # Intentar hacer clic en el menú Configurador con múltiples selectores
            configurador_selectors = [
                (By.XPATH, CatalogoLocators.MENU_CONFIGURADOR),
                (By.XPATH, CatalogoLocators.MENU_CONFIGURADOR_ALT),
                (By.XPATH, CatalogoLocators.MENU_CONFIGURADOR_ALT2)
            ]
            
            configurador_clicked = False
            for by_type, selector in configurador_selectors:
                try:
                    self.logger.info(f"Intentando selector Configurador: {selector}")
                    menu_configurador = self.wait.until(
                        EC.element_to_be_clickable((by_type, selector))
                    )
                    menu_configurador.click()
                    self.logger.info("✅ Menú Configurador clickeado exitosamente")
                    configurador_clicked = True
                    break
                except Exception as e:
                    self.logger.warning(f"Selector Configurador {selector} falló: {str(e)}")
                    continue
            
            if not configurador_clicked:
                self.logger.error("No se pudo hacer clic en el menú Configurador")
                return False
            
            # Intentar expandir el menú si es necesario
            self.expand_configurador_menu()
            
            # Esperar un momento para que se expanda el menú
            time.sleep(2)
            
            # Debug: Verificar elementos después de expandir
            self.debug_menu_elements()
            
            # Intentar hacer clic en "Gestor de catálogos" con múltiples selectores
            gestor_selectors = [
                (By.XPATH, CatalogoLocators.SUBMENU_GESTOR_CATALOGOS),
                (By.XPATH, CatalogoLocators.SUBMENU_GESTOR_CATALOGOS_ALT),
                (By.XPATH, CatalogoLocators.SUBMENU_GESTOR_CATALOGOS_ALT2),
                (By.XPATH, CatalogoLocators.SUBMENU_CATALOGOS)  # Fallback a "Catálogos"
            ]
            
            gestor_clicked = False
            for by_type, selector in gestor_selectors:
                try:
                    self.logger.info(f"Intentando selector Gestor de catálogos: {selector}")
                    submenu_gestor = self.wait.until(
                        EC.element_to_be_clickable((by_type, selector))
                    )
                    submenu_gestor.click()
                    self.logger.info("✅ Gestor de catálogos clickeado exitosamente")
                    gestor_clicked = True
                    break
                except Exception as e:
                    self.logger.warning(f"Selector Gestor de catálogos {selector} falló: {str(e)}")
                    continue
            
            if not gestor_clicked:
                self.logger.error("No se pudo hacer clic en Gestor de catálogos")
                return False
            
            # Esperar a que se cargue la página de catálogos
            time.sleep(3)
            self.logger.info("✅ Navegación a Gestor de catálogos completada")
            return True
            
        except Exception as e:
            self.logger.error(f"Error navegando a Gestor de catálogos: {str(e)}")
            return False
    
    def click_nuevo_catalogo(self):
        """Hace clic en el botón Nuevo Catálogo"""
        try:
            nuevo_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.NUEVO_CATALOGO_BUTTON))
            )
            nuevo_button.click()
            self.logger.info("Botón Nuevo Catálogo clickeado")
            time.sleep(1)
            return True
        except Exception as e:
            self.logger.error(f"Error clickeando botón Nuevo Catálogo: {str(e)}")
            return False
    
    def fill_catalogo_form(self, nombre, descripcion):
        """Llena el formulario de creación de catálogo"""
        try:
            # Llenar nombre
            nombre_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.NOMBRE_FIELD))
            )
            nombre_field.clear()
            nombre_field.send_keys(nombre)
            self.logger.info(f"Nombre ingresado: {nombre}")
            
            # Llenar descripción
            descripcion_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.DESCRIPCION_FIELD))
            )
            descripcion_field.clear()
            descripcion_field.send_keys(descripcion)
            self.logger.info(f"Descripción ingresada: {descripcion}")
            
            # Seleccionar tipo de catálogo opción 3
            tipo_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.TIPO_CATALOGO_DROPDOWN))
            )
            Select(tipo_dropdown).select_by_value("3")
            self.logger.info("Tipo de catálogo seleccionado: opción 3")
            
            # Seleccionar clasificación opción 3
            clasificacion_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.CLASIFICACION_DROPDOWN))
            )
            Select(clasificacion_dropdown).select_by_value("3")
            self.logger.info("Clasificación seleccionada: opción 3")
            
            return True
        except Exception as e:
            self.logger.error(f"Error llenando formulario de catálogo: {str(e)}")
            return False
    
    def save_catalogo(self):
        """Guarda el catálogo"""
        try:
            guardar_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.GUARDAR_BUTTON))
            )
            guardar_button.click()
            self.logger.info("Catálogo guardado")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.error(f"Error guardando catálogo: {str(e)}")
            return False
    
    def fill_edicion_form(self, nombre_tecnico, etiqueta):
        """Llena el formulario de edición del catálogo"""
        try:
            # Llenar nombre técnico
            nombre_tecnico_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.NOMBRE_TECNICO_FIELD))
            )
            nombre_tecnico_field.clear()
            nombre_tecnico_field.send_keys(nombre_tecnico)
            self.logger.info(f"Nombre técnico ingresado: {nombre_tecnico}")
            
            # Llenar etiqueta
            etiqueta_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.ETIQUETA_FIELD))
            )
            etiqueta_field.clear()
            etiqueta_field.send_keys(etiqueta)
            self.logger.info(f"Etiqueta ingresada: {etiqueta}")
            
            # Seleccionar estructura opción 2
            estructura_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.ESTRUCTURA_DROPDOWN))
            )
            Select(estructura_dropdown).select_by_value("2")
            self.logger.info("Estructura seleccionada: opción 2")
            
            return True
        except Exception as e:
            self.logger.error(f"Error llenando formulario de edición: {str(e)}")
            return False
    
    def save_edicion(self):
        """Guarda la edición del catálogo"""
        try:
            guardar_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, CatalogoLocators.GUARDAR_BUTTON))
            )
            guardar_button.click()
            self.logger.info("Edición del catálogo guardada")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.error(f"Error guardando edición: {str(e)}")
            return False
    
    def is_success_message_displayed(self):
        """Verifica si se muestra un mensaje de éxito"""
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, CatalogoLocators.SUCCESS_MESSAGE))
            )
            self.logger.info("Mensaje de éxito mostrado")
            return True
        except Exception as e:
            self.logger.error(f"Error verificando mensaje de éxito: {str(e)}")
            return False
