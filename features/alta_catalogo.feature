Feature: Inicio de Sesión y Creación de Catálogo
    Como usuario
    Quiero iniciar sesión en el sistema y crear un nuevo catálogo
    Para que pueda gestionar las configuraciones de catálogos

    Scenario: Iniciar Sesión y Crear Nuevo Catálogo con Detalles Técnicos
            Given estoy en la página de inicio de sesión
            When inicio sesión con usuario "consultores-mobiik-okta@zucarmex.com" y contraseña "D3s4rr0ll02025#_01"
            And espero la validación manual de 2FA después de hacer clic en verificar
            Then debería estar completamente autenticado y en la página principal
            When navego al menú Configurador > Catálogos
            And hago clic en el botón "Nuevo" para crear un nuevo catálogo
            And lleno el formulario del catálogo con:
            | Nombre        | AutoQA1Nom         |
            | Descripción   | AutoQA1Descripción |
            | Tipo          | 3                  |
            | Clasificación | 3                  |
            And guardo el catálogo
            Then el catálogo debería crearse exitosamente
            When lleno el formulario de detalles técnicos con:
            | Nombre Técnico | NomTecQA1Aut |
            | Etiqueta       | EtiQA1       |
            | Estructura     | 2            |
            And guardo los detalles técnicos
            Then los detalles técnicos deberían guardarse exitosamente
