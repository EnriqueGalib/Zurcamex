class CatalogoLocators:
    """Locators para la funcionalidad de catálogos"""
    
    # Menú y navegación
    MENU_CONFIGURADOR = "//span[contains(text(),'Configurador')]"
    MENU_CONFIGURADOR_ALT = "//div[contains(text(),'Configurador')]"
    MENU_CONFIGURADOR_ALT2 = "//a[contains(text(),'Configurador')]"
    SUBMENU_GESTOR_CATALOGOS = "//span[contains(text(),'Gestor de catálogos')]"
    SUBMENU_GESTOR_CATALOGOS_ALT = "//div[contains(text(),'Gestor de catálogos')]"
    SUBMENU_GESTOR_CATALOGOS_ALT2 = "//a[contains(text(),'Gestor de catálogos')]"
    SUBMENU_CATALOGOS = "//span[contains(text(),'Catálogos')]"
    
    # Botones principales
    NUEVO_CATALOGO_BUTTON = "//button[contains(text(),'Nuevo') or contains(text(),'Crear')]"
    GUARDAR_BUTTON = "//button[contains(text(),'Guardar')]"
    CANCELAR_BUTTON = "//button[contains(text(),'Cancelar')]"
    
    # Campos del formulario de catálogo
    NOMBRE_FIELD = "//input[@name='nombre' or @placeholder='Nombre']"
    DESCRIPCION_FIELD = "//textarea[@name='descripcion' or @placeholder='Descripción']"
    TIPO_CATALOGO_DROPDOWN = "//select[@name='tipoCatalogo']"
    TIPO_CATALOGO_OPTION_3 = "//option[@value='3' or contains(text(),'3')]"
    CLASIFICACION_DROPDOWN = "//select[@name='clasificacion']"
    CLASIFICACION_OPTION_3 = "//option[@value='3' or contains(text(),'3')]"
    
    # Campos de edición
    NOMBRE_TECNICO_FIELD = "//input[@name='nombreTecnico' or @placeholder='Nombre Técnico']"
    ETIQUETA_FIELD = "//input[@name='etiqueta' or @placeholder='Etiqueta']"
    ESTRUCTURA_DROPDOWN = "//select[@name='estructura']"
    ESTRUCTURA_OPTION_2 = "//option[@value='2' or contains(text(),'2')]"
    
    # Mensajes y validaciones
    SUCCESS_MESSAGE = "//div[contains(@class,'success') or contains(@class,'alert-success')]"
    ERROR_MESSAGE = "//div[contains(@class,'error') or contains(@class,'alert-danger')]"
    
    # Tabla de catálogos
    CATALOGOS_TABLE = "//table[contains(@class,'table')]"
    CATALOGO_ROW = "//tr[contains(.,'AutoQA1Nom')]"
