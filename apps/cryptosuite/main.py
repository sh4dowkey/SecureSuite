# File: apps/cryptosuite/main.py

from .app import App


def main():
    """Entry point for the SecureSuite application"""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
