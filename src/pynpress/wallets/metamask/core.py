from playwright.sync_api import BrowserContext, Page, expect
from playwright.async_api import BrowserContext as AsyncBrowserContext
from typing import Union, Optional, Any
import time

from ..base import BaseWallet
from .locators import MetaMaskLocators


class MetaMask(BaseWallet):
    def __init__(self, context: Union[BrowserContext, AsyncBrowserContext], extension_id: Optional[str] = None, language: str = "en-US"):
        super().__init__(context, extension_id, language)
        # If extension_id is not provided, we might need a way to find it or default it
        # But usually it's passed from the launcher.

    def setup(self, seed_phrase: str, password: str) -> None:
        """
        Automates the MetaMask onboarding flow.
        Assumption: The browser opens with the MetaMask onboarding tab active.
        """
        # Wait for extension to initialize
        time.sleep(3)

        if not self.extension_id:
            raise ValueError("Extension ID not found. Cannot navigate to onboarding page.")

        # Open the specific onboarding page explicitly
        # chrome-extension://{id}/home.html#/onboarding/welcome
        onboarding_url = f"chrome-extension://{self.extension_id}/home.html#/onboarding/welcome"

        # Open new page first to ensure browser doesn't close
        self.page = self.context.new_page()
        self.page.goto(onboarding_url)

        # Close all other pages to clean up chaos
        pages_to_close = [p for p in self.context.pages if p != self.page]
        for p in pages_to_close:
            try:
                p.close()
            except Exception:
                pass

        page = self.page

        # Implementation of setup flow using Locators
        # 1. Check Terms
        # page.check(MetaMaskLocators.ONBOARDING_TERMS_CHECKBOX)
        # 2. Click Import Wallet
        page.click(MetaMaskLocators.ONBOARDING_IMPORT_WALLET_BUTTON)
        # 3. No Thanks to Metrics
        page.click(MetaMaskLocators.ONBOARDING_IMPORT_WITH_SRP_BUTTON)

        # 4. Fill Seed Phrase
        for i, word in enumerate(seed_phrase.split(" ")):
            # metamask usually has separate inputs now, or one big one depending on version
            # Using the locator template for separate inputs
            word += " "
            if i == 0:
                page.locator(MetaMaskLocators.SRP_INPUT_TEMPLATE).type(word)
            else:
                page.type(MetaMaskLocators.SRP_INPUT_TEMPLATE_INDEX.format(index=i), word)
            # page.locator(MetaMaskLocators.SRP_INPUT_TEMPLATE).type(" ")
            time.sleep(.1)

        page.click(MetaMaskLocators.SRP_CONFIRM_BUTTON)

        # 5. Create Password
        page.fill(MetaMaskLocators.CREATE_PASSWORD_NEW, password)
        page.fill(MetaMaskLocators.CREATE_PASSWORD_CONFIRM, password)
        page.check(MetaMaskLocators.CREATE_PASSWORD_TERMS)
        page.click(MetaMaskLocators.CREATE_PASSWORD_IMPORT)
        page.click(MetaMaskLocators.CREATE_PASSWORD_AGREE)

        # 6. Complete
        page.click(MetaMaskLocators.ONBOARDING_COMPLETE_DONE)
        # page.click(MetaMaskLocators.ONBOARDING_NEXT)
        # page.click(MetaMaskLocators.ONBOARDING_PIN_EXTENSION_DONE)
        page.goto(f'chrome-extension://{self.extension_id}/sidepanel.html#/')

    def approve_connect(self) -> None:
        """
        Handles the connection popup.
        """
        # Switch to notification page
        # In a real impl, we'd look for the popup page or window
        self.page.click(MetaMaskLocators.CONNECT_APPROVE_BUTTON)

    def cancel_connect(self) -> None:
        self.page.click(MetaMaskLocators.CONNECT_CANCEL_BUTTON)

    def confirm_transaction(self):
        self.page.click(MetaMaskLocators.CONFIRM_FOOTER_NEXT)

    def cancel_transaction(self):
        self.page.click(MetaMaskLocators.CONFIRM_FOOTER_CANCEL_NEXT)