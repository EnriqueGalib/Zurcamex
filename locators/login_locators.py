class LoginLocators:
    """Locators para la página de login"""
    
    # Botón inicial de autenticación OKTA
    OKTA_AUTH_BUTTON = "button:contains('AUTENTICARSE CON OKTA')"
    OKTA_AUTH_BUTTON_ALT = "//button[contains(text(), 'AUTENTICARSE CON OKTA')]"
    
    # Campos de entrada en OKTA - Múltiples selectores para mayor robustez
    OKTA_USERNAME_FIELD = "input[name='username']"
    OKTA_USERNAME_FIELD_ALT1 = "input[type='text']"
    OKTA_USERNAME_FIELD_ALT2 = "input[placeholder*='usuario' i]"
    OKTA_USERNAME_FIELD_ALT3 = "input[id*='username']"
    OKTA_USERNAME_FIELD_ALT4 = "//input[@name='username']"
    OKTA_USERNAME_FIELD_ALT5 = "//input[@type='text']"
    
    OKTA_PASSWORD_FIELD = "input[name='password']"
    OKTA_PASSWORD_FIELD_ALT1 = "input[type='password']"
    OKTA_PASSWORD_FIELD_ALT2 = "//input[@name='password']"
    
    # Botones en OKTA - Múltiples selectores
    OKTA_NEXT_BUTTON = "//button[contains(text(), 'Siguiente')]"
    OKTA_NEXT_BUTTON_ALT1 = "//button[contains(text(), 'Next')]"
    OKTA_NEXT_BUTTON_ALT2 = "//input[@type='submit']"
    OKTA_NEXT_BUTTON_ALT3 = "//button[@type='submit']"
    OKTA_NEXT_BUTTON_ALT4 = "button[type='submit']"
    OKTA_NEXT_BUTTON_ALT5 = "input[type='submit']"
    
    OKTA_SIGNIN_BUTTON = "//button[contains(text(), 'Verificar')]"
    OKTA_SIGNIN_BUTTON_ALT1 = "//input[@value='Verificar']"
    OKTA_SIGNIN_BUTTON_ALT2 = "//button[contains(text(), 'Iniciar sesión')]"
    OKTA_SIGNIN_BUTTON_ALT3 = "//button[contains(text(), 'Sign In')]"
    OKTA_SIGNIN_BUTTON_ALT4 = "//input[@type='submit']"
    OKTA_SIGNIN_BUTTON_ALT5 = "//input[@value='Iniciar sesión']"
    OKTA_SIGNIN_BUTTON_ALT6 = "//input[@value='Sign In']"
    OKTA_SIGNIN_BUTTON_ALT7 = "//input[@value='Siguiente']"
    OKTA_SIGNIN_BUTTON_ALT8 = "//input[@value='Next']"
    
    # Campos de entrada genéricos (fallback)
    USERNAME_FIELD = "input[name='username']"
    PASSWORD_FIELD = "input[name='password']"
    
    # Botones genéricos (fallback)
    LOGIN_BUTTON = "button[type='submit']"
    
    # Elementos de validación
    LOGIN_FORM = "form"
    ERROR_MESSAGE = ".error-message"
