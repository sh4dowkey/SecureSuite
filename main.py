# The main entry point for the entire SecureSuite application.
# This starts the CryptoSuite window by default.

from apps.cryptosuite.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()