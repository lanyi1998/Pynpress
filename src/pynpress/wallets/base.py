from abc import ABC, abstractmethod
from playwright.sync_api import BrowserContext, Page
from playwright.async_api import BrowserContext as AsyncBrowserContext, Page as AsyncPage
from typing import Union, Optional, Any

class BaseWallet(ABC):
    """
    Abstract base class for all wallet implementations.
    """

    def __init__(self, context: Union[BrowserContext, AsyncBrowserContext], extension_id: Optional[str] = None, language: str = "en-US"):
        self.context = context
        self.extension_id = extension_id
        self.language = language
        self.page: Union[Page, AsyncPage, None] = None

    @abstractmethod
    def setup(self, seed_phrase: str, password: str) -> None:
        """
        Perform initial setup (import wallet, etc.).
        """
        pass

    @abstractmethod
    def approve_connect(self) -> None:
        """
        Approve a connection request from a dApp.
        """
        pass

    @abstractmethod
    def cancel_connect(self) -> None:
        """
        Cancel a connection request from a dApp.
        """
        pass

    @abstractmethod
    def sign(self) -> None:
        """
        Sign a message or transaction.
        """
        pass

    @abstractmethod
    def confirm_transaction(self) -> None:
        """
        Confirm a pending transaction.
        """
        pass

    @abstractmethod
    def add_network(self, network_details: dict[str, Any]) -> None:
        """
        Add a new network to the wallet.
        """
        pass

    @abstractmethod
    def switch_network(self, network_name: str) -> None:
        """
        Switch to a different network.
        """
        pass
