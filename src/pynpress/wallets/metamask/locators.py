class MetaMaskLocators:

    # Setup / Onboarding
    ONBOARDING_IMPORT_WALLET_BUTTON = "data-testid=onboarding-import-wallet"
    ONBOARDING_IMPORT_WITH_SRP_BUTTON = "data-testid=onboarding-import-with-srp-button"
    
    # Secret Recovery Phrase
    SRP_INPUT_TEMPLATE = "textarea"
    SRP_INPUT_TEMPLATE_INDEX = 'data-testid=import-srp__srp-word-{index}'
    SRP_CONFIRM_BUTTON = "data-testid=import-srp-confirm"
    
    # Password Creation
    CREATE_PASSWORD_NEW = "data-testid=create-password-new-input"
    CREATE_PASSWORD_CONFIRM = "data-testid=create-password-confirm-input"
    CREATE_PASSWORD_TERMS = "data-testid=create-password-terms"
    CREATE_PASSWORD_IMPORT = "data-testid=create-password-submit"
    CREATE_PASSWORD_AGREE = 'data-testid=metametrics-i-agree'
    
    # Completion
    ONBOARDING_COMPLETE_DONE = "data-testid=onboarding-complete-done"
    ONBOARDING_NEXT = "data-testid=onboarding-next-button"
    ONBOARDING_PIN_EXTENSION = "data-testid=pin-extension-next"
    ONBOARDING_PIN_EXTENSION_DONE = "data-testid=pin-extension-done"

    # Home
    NETWORK_DISPLAY = "data-testid=network-display"
    ACCOUNT_MENU_ICON = "data-testid=account-menu-icon"

    # Notification / Popups
    # Connect
    CONNECT_APPROVE_BUTTON = 'data-testid=confirm-btn'
    CONNECT_CANCEL_BUTTON = "data-testid=cancel-btn"
    
    # Sign
    SIGN_CONFIRM_BUTTON = "data-testid=page-container-footer-next"
    SIGN_CANCEL_BUTTON = "data-testid=page-container-footer-cancel" # Often same as connect
    SIGN_SCROLL_DOWN = "data-testid=signature-request-scroll-button" 
    
    # Transaction
    CONFIRM_FOOTER_NEXT = "data-testid=confirm-footer-button"
    CONFIRM_FOOTER_CANCEL_NEXT = "data-testid=confirm-footer-cancel-button"
    GAS_EDIT_BUTTON = "data-testid=edit-gas-fee-button"
