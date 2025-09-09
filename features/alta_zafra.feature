Feature: Alta de Zafra
    Como usuario del sistema Credicam
    Quiero poder crear una nueva zafra
    Para gestionar las zafras del sistema

    @alta_zafra
    Scenario: Autenticación completa con OKTA para Alta de Zafra
            Given que el navegador está configurado correctamente para zafra
            And que el usuario navega a la página de login y hace clic inmediato
            Then debe redirigirse a la página de autenticación de OKTA
            When el usuario ingresa el usuario consultores-mobiik-okta@zucarmex.com y hace clic en Siguiente de OKTA
            And el usuario ingresa la contraseña D3s4rr0ll02025#_01 y hace clic en Verificar de OKTA con debug
            When el usuario espera para validar manualmente la 2FA
            Then debe verificar que esté en la página principal de Zucarmex
            When el usuario hace clic en Configuración
            And el usuario hace clic en Zafras
            And el usuario hace clic en Nueva zafra
