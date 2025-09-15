# The main entry point for the entire SecureSuite application.
# This starts the CryptoSuite window by default.

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def main():
    """Main entry point for SecureSuite"""
    try:
        # Import and run CryptoSuite
        from apps.cryptosuite.main import main as cryptosuite_main
        cryptosuite_main()
    except ImportError as e:
        print(f"Error importing CryptoSuite: {e}")
        print("Please make sure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
