import customtkinter
import json
from tkinter import filedialog
from .base_frame import BaseFrame, CollapsibleFrame # Make sure CollapsibleFrame is in base_frame.py
from ..operations.encoders import to_base64
from ..operations.ciphers import caesar_cipher
from ..operations.hex import to_hex


class EncryptFrame(BaseFrame):
    def __init__(self, master, app, status_bar, **kwargs):
        # --- Set unique properties for this frame ---
        self.recipe_title = "Recipe"
        self.placeholder_text = "Click an operation to begin..."
        self.load_button_text = "📂 Load"
        self.load_button_width = 70

        super().__init__(master, app, status_bar, **kwargs)

    def execute_operation(self, operation_name, input_data, step_frame):
        # This function will need to be expanded to handle all the new operations.
        if operation_name == "To Base64":
            return to_base64(input_data)
        elif operation_name == "To Hex":
            return to_hex(input_data)
        elif operation_name == "Caesar Encrypt":
            try:
                shift = int(step_frame.param_entry.get())
                if not 1 <= shift <= 25:
                    return False, "Shift must be between 1 and 25."
                return caesar_cipher(input_data, shift, decrypt=False)
            except (ValueError, TypeError):
                return False, "Invalid shift value. Must be an integer."
            except AttributeError:
                return False, "Could not find shift parameter."
        else:
            return False, f"Unknown operation: {operation_name}"

    def create_operations_sidebar(self):
        sidebar_frame = customtkinter.CTkFrame(self)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        sidebar_frame.grid_rowconfigure(1, weight=1)
        sidebar_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(sidebar_frame, text="Operations",
                               font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20,
                                                                                        pady=(10, 10))

        scrollable_frame = customtkinter.CTkScrollableFrame(sidebar_frame, fg_color="transparent", corner_radius=0)
        scrollable_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Helper to create buttons with better padding ---
        def add_button(parent, text, command):
            button = customtkinter.CTkButton(parent, text=text, anchor="w", command=command)
            button.pack(fill="x", padx=5, pady=4) # Increased padding for better spacing

        # --- Section: Data Formats & Encodings ---
        data_formats_frame = CollapsibleFrame(scrollable_frame, text="Data Formats & Encodings")
        data_formats_frame.pack(fill="x", pady=(0, 5))
        add_button(data_formats_frame.content_frame, "To Base64", lambda: self.add_recipe_step("To Base64"))
        add_button(data_formats_frame.content_frame, "To Base32", lambda: self.add_recipe_step("To Base32"))
        add_button(data_formats_frame.content_frame, "To Base58", lambda: self.add_recipe_step("To Base58"))
        add_button(data_formats_frame.content_frame, "To Hex", lambda: self.add_recipe_step("To Hex"))
        add_button(data_formats_frame.content_frame, "URL Encode", lambda: self.add_recipe_step("URL Encode"))
        add_button(data_formats_frame.content_frame, "To Binary", lambda: self.add_recipe_step("To Binary"))
        add_button(data_formats_frame.content_frame, "Morse Code", lambda: self.add_recipe_step("Morse Code"))

        # --- Section: Classic Ciphers ---
        classic_ciphers_frame = CollapsibleFrame(scrollable_frame, text="Classic Ciphers")
        classic_ciphers_frame.pack(fill="x", pady=(0, 5))
        add_button(classic_ciphers_frame.content_frame, "Caesar Encrypt", lambda: self.add_recipe_step("Caesar Encrypt"))
        add_button(classic_ciphers_frame.content_frame, "Atbash Cipher", lambda: self.add_recipe_step("Atbash Cipher"))
        add_button(classic_ciphers_frame.content_frame, "ROT13 Cipher", lambda: self.add_recipe_step("ROT13 Cipher"))
        add_button(classic_ciphers_frame.content_frame, "Vigenère Encrypt", lambda: self.add_recipe_step("Vigenère Encrypt"))
        add_button(classic_ciphers_frame.content_frame, "Playfair Encrypt", lambda: self.add_recipe_step("Playfair Encrypt"))
        add_button(classic_ciphers_frame.content_frame, "Rail Fence Encrypt", lambda: self.add_recipe_step("Rail Fence Encrypt"))

        # --- Section: Symmetric Encryption ---
        symmetric_frame = CollapsibleFrame(scrollable_frame, text="Symmetric Encryption")
        symmetric_frame.pack(fill="x", pady=(0, 5))
        add_button(symmetric_frame.content_frame, "AES Encrypt", lambda: self.add_recipe_step("AES Encrypt"))
        add_button(symmetric_frame.content_frame, "Blowfish Encrypt", lambda: self.add_recipe_step("Blowfish Encrypt"))
        add_button(symmetric_frame.content_frame, "Twofish Encrypt", lambda: self.add_recipe_step("Twofish Encrypt"))
        add_button(symmetric_frame.content_frame, "Serpent Encrypt", lambda: self.add_recipe_step("Serpent Encrypt"))
        add_button(symmetric_frame.content_frame, "ChaCha20-Poly1305", lambda: self.add_recipe_step("ChaCha20-Poly1305"))

        # --- Section: Asymmetric Encryption ---
        asymmetric_frame = CollapsibleFrame(scrollable_frame, text="Asymmetric Encryption")
        asymmetric_frame.pack(fill="x", pady=(0, 5))
        add_button(asymmetric_frame.content_frame, "RSA Encrypt", lambda: self.add_recipe_step("RSA Encrypt"))

        # --- Section: Hashing ---
        hashing_frame = CollapsibleFrame(scrollable_frame, text="Hashing")
        hashing_frame.pack(fill="x", pady=(0, 5))
        add_button(hashing_frame.content_frame, "SHA-256", lambda: self.add_recipe_step("SHA-256"))
        add_button(hashing_frame.content_frame, "SHA-384", lambda: self.add_recipe_step("SHA-384"))
        add_button(hashing_frame.content_frame, "SHA-512", lambda: self.add_recipe_step("SHA-512"))
        add_button(hashing_frame.content_frame, "SHA-3-256", lambda: self.add_recipe_step("SHA-3-256"))
        add_button(hashing_frame.content_frame, "SHA-3-512", lambda: self.add_recipe_step("SHA-3-512"))
        add_button(hashing_frame.content_frame, "BLAKE2b", lambda: self.add_recipe_step("BLAKE2b"))
        add_button(hashing_frame.content_frame, "BLAKE2s", lambda: self.add_recipe_step("BLAKE2s"))
        add_button(hashing_frame.content_frame, "RIPEMD-160", lambda: self.add_recipe_step("RIPEMD-160"))
        add_button(hashing_frame.content_frame, "MD5", lambda: self.add_recipe_step("MD5"))
        add_button(hashing_frame.content_frame, "SHA-1", lambda: self.add_recipe_step("SHA-1"))

        # --- Section: Message Authentication Codes ---
        mac_frame = CollapsibleFrame(scrollable_frame, text="Message Authentication")
        mac_frame.pack(fill="x", pady=(0, 5))
        add_button(mac_frame.content_frame, "HMAC-SHA256", lambda: self.add_recipe_step("HMAC-SHA256"))
        add_button(mac_frame.content_frame, "HMAC-SHA512", lambda: self.add_recipe_step("HMAC-SHA512"))

    def load_recipe(self):
        filepath = filedialog.askopenfilename(title="Load Recipe", filetypes=[("JSON files", "*.json")])
        if not filepath: return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                recipe_data = json.load(f)
            self.clear_recipe()
            for step in recipe_data:
                operation_name = step.get("operation")
                args = step.get("args", {})
                if operation_name: self.add_recipe_step(operation_name, args=args)
            self.status_bar.configure(text=f"Recipe loaded!", text_color="gray70")
        except Exception as e:
            self.app.show_toast("File Error", f"Failed to load recipe: {e}", toast_type="error")