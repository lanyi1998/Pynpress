
import os
import time

from pynpress import Launcher, WalletType

def main():
    extension_path = "./metamask-chrome-13.15.0"
    
    if not os.path.exists(extension_path):
        print(f"Error: Extension not found at {extension_path}")
        print("Please set METAMASK_PATH env var or place extension in ./metamask-extension")
        return

    print("Launching Pynpress...")
    launcher = Launcher(WalletType.METAMASK)
    context, wallet = launcher.launch(
        seed_phrase="insane medal pioneer design already scorpion wrestle true matrix boil marble cost",
        password="password123",
        headless=False,
        extension_path=extension_path,
    )

    print("Browser launched. Performing setup...")
    # Setup is done inside login if seed/pass provided (conceptually)
    # But in my impl, I call wallet.setup explicitly in login if provided.
    
    page = context.new_page()
    page.goto("https://metamask.github.io/test-dapp/")
    print("Navigated to test dapp.")
    
    # Try to connect
    connect_btn = page.locator("id=connectButton") # hypothetical selector for demo
    if connect_btn.is_visible():
        connect_btn.click()
        print("Clicked connect. Approving in wallet...")
        wallet.approve_connect()
        print("Connected!")
    
    time.sleep(10)
    context.close()

if __name__ == "__main__":
    main()
