Feature: US12_8 Crear y Configurar un Catalogo
    Como usuario del sistema Credicam
    Quiero poder crear un nuevo catálogo
    Para gestionar los productos del sistema

    @alta_catalogo
    Scenario: SP1_01_Alta_Catalogo 234691
            Given que el navegador está configurado correctamente
            And que el usuario navega a la página de login y hace clic inmediato
            Then debe redirigirse a la página de autenticación de OKTA
            When el usuario ingresa el usuario consultores-mobiik-okta@zucarmex.com y hace clic en Siguiente de OKTA
            And el usuario ingresa la contraseña D3s4rr0ll02025#_01 y hace clic en Verificar de OKTA con debug
            When el usuario espera para validar manualmente la 2FA
            Then debe verificar que esté en la página principal de Zucarmex
            When el usuario hace clic en Configurador
            And el usuario hace clic en Gestor de catálogos
            And el usuario hace clic en NUEVO CATÁLOGO con debug
            When el usuario llena el formulario completo con Test
            And el usuario guarda los datos generales
            When el usuario llena la estructura del catálogo con Test
            And el usuario guarda la estructura del catálogo
            And debe capturar evidencias del proceso
