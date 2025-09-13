import platform
from .app.gui import SteganographyApp
from ttkbootstrap import utility

if __name__ == "__main__":
    # This check is important for freezing the app with tools like PyInstaller
    if platform.system() == "Windows":
        try:
            utility.enable_high_dpi_awareness()
        except Exception as e:
            print(f"Warning: Could not set DPI awareness: {e}")

    app = SteganographyApp()
    app.mainloop()