import os
import platform
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def main():
    """Entry point for the Steganography Suite application"""
    try:
        from .app.gui import SteganographyApp
        from ttkbootstrap import utility

        # This check is important for freezing the app with tools like PyInstaller
        if platform.system() == "Windows":
            try:
                utility.enable_high_dpi_awareness()
            except Exception as e:
                print(f"Warning: Could not set DPI awareness: {e}")

        app = SteganographyApp()
        app.mainloop()

    except ImportError as e:
        print(f"Import error in Steganography Suite: {e}")
        print("Please make sure all dependencies are installed.")
        print("Required: opencv-python, ttkbootstrap, tkinterdnd2, cryptography, numpy, pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting Steganography Suite: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
