# Pynpress 🐍

**Pynpress** is a Python-based E2E (End-to-End) testing library for Web3 dApps, heavily inspired by the renowned [Synpress](https://github.com/Synpress/Synpress).

Built on top of [Playwright for Python](https://playwright.dev/python/), Pynpress allows you to automate interactions with cryptocurrency wallets (like **MetaMask**) and dApps directly from your Python test suites.

> ⚠️ **Note**: This project is currently in early development.

## 🌟 Features

- **Wallet Support**: Out-of-the-box support for **MetaMask** (more coming soon).
- **Playwright Native**: Leverages the power and speed of Playwright.
- **Easy Setup**: Automatically launches a browser with the wallet extension pre-loaded.
- **Deterministic**: Initialize wallets with seed phrases and passwords for reproducible tests.
- **Automation**: built-in helpers for common wallet interactions:
  - Connect to dApps (`approve_connect`)
  - Sign messages (Soon)
  - Confirm transactions (Soon)

## 📦 Installation

Requires **Python 3.10+**.

```bash
# Clone the repository
git clone https://github.com/lanyi1998/Pynpress.git
cd Pynpress

# Install dependencies (using uv or pip)
pip install .

# Install Playwright browsers
playwright install
```

## 🚀 Usage

Here is a basic example of how to launch Pynpress with MetaMask and interact with a dApp.

### 1. Prepare Environment
Ensure you have the wallet extension downloaded (e.g., `./metamask-chrome-13.15.0`).

### 2. Write the Test

```python
from pynpress import Launcher, WalletType

def main():
    # Initialize launcher for MetaMask
    launcher = Launcher(WalletType.METAMASK)
    
    # Launch browser with wallet setup
    context, wallet = launcher.launch(
        seed_phrase="your twelve word seed phrase ...",
        password="securePassword123",
        headless=False,
        extension_path="./metamask-chrome-13.15.0"
    )

    # Create a new page and navigate to your dApp
    page = context.new_page()
    page.goto("https://metamask.github.io/test-dapp/")
    
    # Interact with the dApp (e.g., click 'Connect')
    connect_btn = page.locator("#connectButton")
    if connect_btn.is_visible():
        connect_btn.click()
        
        # Approve the connection in MetaMask
        print("Approving connection...")
        wallet.approve_connect()
        print("Connected!")

    # Clean up
    context.close()

if __name__ == "__main__":
    main()
```

## 🛠 Architecture

Pynpress wraps Playwright's `BrowserContext` to inject Web3 wallet extensions. It provides a high-level `Wallet` interface that abstracts away the complexity of switching contexts and interacting with the extension's popups.

## 🤝 Contributing

Contributions are welcome! Please check out the [issues](https://github.com/lanyi1998/Pynpress/issues) or submit a Pull Request.

## 📄 License

MIT
