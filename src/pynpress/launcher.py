import os
import time
from enum import Enum
from typing import Tuple, Optional, Type, List
from playwright.sync_api import sync_playwright, BrowserContext, Page, Playwright
from urllib.parse import urlparse

from .wallets.base import BaseWallet
from .wallets.metamask.core import MetaMask


class WalletType(Enum):
    METAMASK = "metamask"


def get_wallet_class(wallet_type: WalletType) -> Type[BaseWallet]:
    if wallet_type == WalletType.METAMASK:
        return MetaMask
    raise ValueError(f"Unsupported wallet type: {wallet_type}")


class Launcher:
    def __init__(self, wallet_type: WalletType = WalletType.METAMASK):
        self.wallet_type = wallet_type
        self.playwright = None
        self.context = None
        self.wallet = None
        self.user_data_dir = None

    def launch(
            self,
            seed_phrase: str = "",
            password: str = "",
            user_data_dir=None,
            headless: bool = False,
            extension_path: Optional[str] = None,
            args: List[str] = None,
            **kwargs
    ) -> Tuple[BrowserContext, BaseWallet]:
        """
        Launches a browser context with the specified wallet extension and performs setup.
        
        Args:
            seed_phrase: Seed phrase to import (optional).
            password: Password to use/create (optional).
            user_data_dir: user data dir
            headless: Whether to run in headless mode.
            extension_path: Path to the unpacked extension.
            args: Additional arguments for the browser (Chrome CLI args).
            **kwargs: Additional arguments to pass to launch_persistent_context (e.g. user_agent, locale, etc.)
        """
        if args is None:
            args = []

        # TODO: Resolve extension_path automatically if not provided
        if not extension_path:
            raise ValueError("extension_path must be provided for now")

        full_extension_path = os.path.abspath(extension_path)
        if not os.path.exists(full_extension_path):
            raise FileNotFoundError(f"Extension not found at {full_extension_path}")

        # Prepare arguments for loading extension
        # We enforce these, but user can add more via 'args'
        extension_args = [
            f"--disable-extensions-except={full_extension_path}",
            f"--load-extension={full_extension_path}",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-notifications",
            "--disable-gpu",
            "--disable-blink-features=AutomationControlled"
        ]

        launch_args = args + extension_args

        self.playwright = sync_playwright().start()

        # We use launch_persistent_context to keep the profile
        if user_data_dir is None:
            self.user_data_dir = os.path.join(os.getcwd(), f".pynpress_user_data_{int(time.time())}")
        else:
            self.user_data_dir = user_data_dir

        self.context = self.playwright.chromium.launch_persistent_context(
            self.user_data_dir,
            headless=headless,
            args=launch_args,
            slow_mo=100 if not headless else 0,
            **kwargs
        )

        # Initialize Wallet Class
        wallet_cls = get_wallet_class(self.wallet_type)
        with self.context.expect_page() as page_info:
            pass
        metamask_page = page_info.value
        parsed_url = urlparse(metamask_page.url)
        extension_id = parsed_url.netloc

        self.wallet = wallet_cls(self.context, extension_id)

        if seed_phrase and password:
            self.wallet.setup(seed_phrase, password)

        return self.context, self.wallet

    def close(self):
        """Closes the browser context and stops Playwright."""
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()