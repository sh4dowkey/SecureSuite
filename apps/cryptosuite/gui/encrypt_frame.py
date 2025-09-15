# encrypt_frame.py - FIXED
import json
from tkinter import filedialog, messagebox

import customtkinter

from .base_frame import BaseFrame, CollapsibleFrame
from ..operations.encoders import to_base64
from ..operations.hex import to_hex


class EncryptFrame(BaseFrame):
    def __init__(self, master, app, status_bar, **kwargs):
        # Set unique properties for this frame
        self.recipe_title = "Encryption Recipe"
        self.placeholder_text = "🚀 Click an operation to begin building your encryption recipe...\n\nTip: Use Ctrl+1 to switch tabs, F5 to execute!"
        self.load_button_text = "📂Load"  # No space
        self.load_button_width = 80

        super().__init__(master, app, status_bar, **kwargs)

    def execute_operation(self, operation_name, input_data, step_frame):
        # ... (This method remains unchanged)
        """Execute cryptographic operations with enhanced error handling"""
        try:
            # Data Format & Encoding Operations
            if operation_name == "To Base64":
                return to_base64(input_data)
            elif operation_name == "To Base32":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "To Base58":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "To Hex":
                return to_hex(input_data)
            elif operation_name == "URL Encode":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "To Binary":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "To Morse Code":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "To QR Code":
                return self._placeholder_operation(operation_name, input_data)

            # Classic Cipher Operations
            elif operation_name == "Caesar Encrypt":
                return self._execute_caesar_encrypt(input_data, step_frame)
            elif operation_name == "Atbash Cipher":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "ROT13 Cipher":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Vigenère Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Playfair Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Rail Fence Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Beaufort Cipher":
                return self._placeholder_operation(operation_name, input_data)

            # Modern Symmetric Encryption
            elif operation_name == "AES Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Blowfish Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Twofish Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Serpent Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "ChaCha20-Poly1305":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Salsa20 Encrypt":
                return self._placeholder_operation(operation_name, input_data)

            # Asymmetric Encryption
            elif operation_name == "RSA Encrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "ECC Encrypt":
                return self._placeholder_operation(operation_name, input_data)

            # Hash Functions
            elif operation_name == "SHA-256":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "SHA-384":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "SHA-512":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "SHA-3-256":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "SHA-3-512":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "BLAKE2b":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "BLAKE2s":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "BLAKE3":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "RIPEMD-160":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Whirlpool":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "MD5":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "SHA-1":
                return self._placeholder_operation(operation_name, input_data)

            # Message Authentication Codes
            elif operation_name == "HMAC-SHA256":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "HMAC-SHA512":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "HMAC-MD5":
                return self._placeholder_operation(operation_name, input_data)

            # Key Derivation Functions
            elif operation_name == "PBKDF2":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Scrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Argon2":
                return self._placeholder_operation(operation_name, input_data)

            # Text Processing
            elif operation_name == "Reverse Text":
                return True, input_data[::-1]  # Fixed to return actual reversed text, not placeholder
            elif operation_name == "Uppercase":
                return True, input_data.upper()
            elif operation_name == "Lowercase":
                return True, input_data.lower()
            elif operation_name == "Remove Spaces":
                return True, input_data.replace(" ", "")

            else:
                return False, f"Unknown operation: {operation_name}"

        except Exception as e:
            return False, f"Operation '{operation_name}' failed: {str(e)}"

    def _placeholder_operation(self, operation_name, input_data):
        # ... (This method remains unchanged)
        """Placeholder for operations not yet implemented"""
        # For demonstration, we'll just return the input with a prefix
        # You can replace this with actual implementation later
        placeholder_result = f"[{operation_name}] {input_data}"
        return True, placeholder_result

    def create_operations_sidebar(self):
        """Create enhanced operations sidebar with organized categories"""
        sidebar_frame = customtkinter.CTkFrame(self, corner_radius=12)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(12, 8), pady=12)
        sidebar_frame.grid_rowconfigure(1, weight=1)
        sidebar_frame.grid_columnconfigure(0, weight=1)

        # Enhanced header
        header_frame = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", height=50)
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        customtkinter.CTkLabel(
            header_frame, text="⚙️Operations", font=customtkinter.CTkFont(size=18, weight="bold")
        ).pack(side="top", anchor="w")

        customtkinter.CTkLabel(
            header_frame, text="Click to add to recipe", font=customtkinter.CTkFont(size=11),
            text_color=("gray50", "gray60")
        ).pack(side="top", anchor="w")

        # Scrollable operations area
        scrollable_frame = customtkinter.CTkScrollableFrame(
            sidebar_frame, fg_color="transparent", corner_radius=8
        )
        scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Helper function for creating buttons (NO SPACE)
        def add_button(parent, text, command, icon="🔧"):
            button = customtkinter.CTkButton(
                parent, text=f"{icon}{text}", anchor="w", command=command, height=38,
                font=customtkinter.CTkFont(size=13), corner_radius=6
            )
            button.pack(fill="x", padx=6, pady=2)
            return button

        # Data Formats & Encodings
        data_formats_frame = CollapsibleFrame(scrollable_frame, text="🗂Data Formats & Encodings")
        data_formats_frame.pack(fill="x", pady=(0, 8))
        data_formats_frame.set_algorithm_count(8)
        # (add_button calls remain the same)
        add_button(data_formats_frame.content_frame, "To Base64", lambda: self.add_recipe_step("To Base64"), "📋")
        add_button(data_formats_frame.content_frame, "To Base32", lambda: self.add_recipe_step("To Base32"), "📋")
        add_button(data_formats_frame.content_frame, "To Base58", lambda: self.add_recipe_step("To Base58"), "📋")
        add_button(data_formats_frame.content_frame, "To Hex", lambda: self.add_recipe_step("To Hex"), "🔢")
        add_button(data_formats_frame.content_frame, "URL Encode", lambda: self.add_recipe_step("URL Encode"), "🌐")
        add_button(data_formats_frame.content_frame, "To Binary", lambda: self.add_recipe_step("To Binary"), "💻")
        add_button(data_formats_frame.content_frame, "To Morse Code", lambda: self.add_recipe_step("To Morse Code"),
                   "📡")
        add_button(data_formats_frame.content_frame, "To QR Code", lambda: self.add_recipe_step("To QR Code"), "📱")

        # Classic Ciphers
        classic_ciphers_frame = CollapsibleFrame(scrollable_frame, text="🏛Classic Ciphers")
        classic_ciphers_frame.pack(fill="x", pady=(0, 8))
        classic_ciphers_frame.set_algorithm_count(7)
        # (add_button calls remain the same)
        add_button(classic_ciphers_frame.content_frame, "Caesar Encrypt",
                   lambda: self.add_recipe_step("Caesar Encrypt"), "🏛")
        add_button(classic_ciphers_frame.content_frame, "Atbash Cipher", lambda: self.add_recipe_step("Atbash Cipher"),
                   "🔄")
        add_button(classic_ciphers_frame.content_frame, "ROT13 Cipher", lambda: self.add_recipe_step("ROT13 Cipher"),
                   "🔄")
        add_button(classic_ciphers_frame.content_frame, "Vigenère Encrypt",
                   lambda: self.add_recipe_step("Vigenère Encrypt"), "🗝")
        add_button(classic_ciphers_frame.content_frame, "Playfair Encrypt",
                   lambda: self.add_recipe_step("Playfair Encrypt"), "🎯")
        add_button(classic_ciphers_frame.content_frame, "Rail Fence Encrypt",
                   lambda: self.add_recipe_step("Rail Fence Encrypt"), "🚂")
        add_button(classic_ciphers_frame.content_frame, "Beaufort Cipher",
                   lambda: self.add_recipe_step("Beaufort Cipher"), "⚓")

        # Modern Symmetric Encryption
        symmetric_frame = CollapsibleFrame(scrollable_frame, text="🛡Modern Symmetric Encryption")
        symmetric_frame.pack(fill="x", pady=(0, 8))
        symmetric_frame.set_algorithm_count(6)
        # (add_button calls remain the same)
        add_button(symmetric_frame.content_frame, "AES Encrypt", lambda: self.add_recipe_step("AES Encrypt"), "🛡")
        add_button(symmetric_frame.content_frame, "Blowfish Encrypt", lambda: self.add_recipe_step("Blowfish Encrypt"),
                   "🐡")
        add_button(symmetric_frame.content_frame, "Twofish Encrypt", lambda: self.add_recipe_step("Twofish Encrypt"),
                   "🐟")
        add_button(symmetric_frame.content_frame, "Serpent Encrypt", lambda: self.add_recipe_step("Serpent Encrypt"),
                   "🐍")
        add_button(symmetric_frame.content_frame, "ChaCha20-Poly1305",
                   lambda: self.add_recipe_step("ChaCha20-Poly1305"), "⚡")
        add_button(symmetric_frame.content_frame, "Salsa20 Encrypt", lambda: self.add_recipe_step("Salsa20 Encrypt"),
                   "💃")

        # Asymmetric Encryption
        asymmetric_frame = CollapsibleFrame(scrollable_frame, text="🔐Asymmetric Encryption")
        asymmetric_frame.pack(fill="x", pady=(0, 8))
        asymmetric_frame.set_algorithm_count(2)
        # (add_button calls remain the same)
        add_button(asymmetric_frame.content_frame, "RSA Encrypt", lambda: self.add_recipe_step("RSA Encrypt"), "🔐")
        add_button(asymmetric_frame.content_frame, "ECC Encrypt", lambda: self.add_recipe_step("ECC Encrypt"), "🌐")

        # Hash Functions
        hashing_frame = CollapsibleFrame(scrollable_frame, text="✨Hash Functions")
        hashing_frame.pack(fill="x", pady=(0, 8))
        hashing_frame.set_algorithm_count(12)
        # (add_button calls remain the same)
        add_button(hashing_frame.content_frame, "SHA-256", lambda: self.add_recipe_step("SHA-256"), "🔷")
        add_button(hashing_frame.content_frame, "SHA-384", lambda: self.add_recipe_step("SHA-384"), "🔷")
        add_button(hashing_frame.content_frame, "SHA-512", lambda: self.add_recipe_step("SHA-512"), "🔷")
        add_button(hashing_frame.content_frame, "SHA-3-256", lambda: self.add_recipe_step("SHA-3-256"), "🔸")
        add_button(hashing_frame.content_frame, "SHA-3-512", lambda: self.add_recipe_step("SHA-3-512"), "🔸")
        add_button(hashing_frame.content_frame, "BLAKE2b", lambda: self.add_recipe_step("BLAKE2b"), "🔹")
        add_button(hashing_frame.content_frame, "BLAKE2s", lambda: self.add_recipe_step("BLAKE2s"), "🔹")
        add_button(hashing_frame.content_frame, "BLAKE3", lambda: self.add_recipe_step("BLAKE3"), "🔹")
        add_button(hashing_frame.content_frame, "RIPEMD-160", lambda: self.add_recipe_step("RIPEMD-160"), "💎")
        add_button(hashing_frame.content_frame, "Whirlpool", lambda: self.add_recipe_step("Whirlpool"), "🌪")
        add_button(hashing_frame.content_frame, "MD5", lambda: self.add_recipe_step("MD5"), "⚠")
        add_button(hashing_frame.content_frame, "SHA-1", lambda: self.add_recipe_step("SHA-1"), "⚠")

        # Message Authentication Codes
        mac_frame = CollapsibleFrame(scrollable_frame, text="🔏Message Authentication")
        mac_frame.pack(fill="x", pady=(0, 8))
        mac_frame.set_algorithm_count(3)
        # (add_button calls remain the same)
        add_button(mac_frame.content_frame, "HMAC-SHA256", lambda: self.add_recipe_step("HMAC-SHA256"), "🔏")
        add_button(mac_frame.content_frame, "HMAC-SHA512", lambda: self.add_recipe_step("HMAC-SHA512"), "🔏")
        add_button(mac_frame.content_frame, "HMAC-MD5", lambda: self.add_recipe_step("HMAC-MD5"), "🔏")

        # Key Derivation Functions
        kdf_frame = CollapsibleFrame(scrollable_frame, text="🔑Key Derivation Functions")
        kdf_frame.pack(fill="x", pady=(0, 8))
        kdf_frame.set_algorithm_count(3)
        # (add_button calls remain the same)
        add_button(kdf_frame.content_frame, "PBKDF2", lambda: self.add_recipe_step("PBKDF2"), "🗝")
        add_button(kdf_frame.content_frame, "Scrypt", lambda: self.add_recipe_step("Scrypt"), "⚙")
        add_button(kdf_frame.content_frame, "Argon2", lambda: self.add_recipe_step("Argon2"), "🛡")

        # Text Utilities
        text_utils_frame = CollapsibleFrame(scrollable_frame, text="📝Text Utilities")
        text_utils_frame.pack(fill="x", pady=(0, 8))
        text_utils_frame.set_algorithm_count(4)
        # (add_button calls remain the same)
        add_button(text_utils_frame.content_frame, "Reverse Text", lambda: self.add_recipe_step("Reverse Text"), "🔄")
        add_button(text_utils_frame.content_frame, "Uppercase", lambda: self.add_recipe_step("Uppercase"), "🔠")
        add_button(text_utils_frame.content_frame, "Lowercase", lambda: self.add_recipe_step("Lowercase"), "🔡")
        add_button(text_utils_frame.content_frame, "Remove Spaces", lambda: self.add_recipe_step("Remove Spaces"), "✂️")

        # Statistics at bottom
        stats_frame = customtkinter.CTkFrame(sidebar_frame, fg_color=("gray90", "gray20"), height=40)
        stats_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

        total_algorithms = 8 + 7 + 6 + 2 + 12 + 3 + 3 + 4  # 45 total algorithms
        customtkinter.CTkLabel(
            stats_frame, text=f"📊 Total: {total_algorithms} algorithms available",
            font=customtkinter.CTkFont(size=11, weight="bold"), text_color=("gray30", "gray70")
        ).pack(pady=10)

    def create_recipe_panel(self):
        """Create a consistent recipe panel by calling the base and customizing it."""
        super().create_recipe_panel()  # Create the base structure

        # --- Customizations for EncryptFrame ---

        # Custom Title
        customtkinter.CTkLabel(
            self.title_frame, text="🔒", font=customtkinter.CTkFont(size=20)
        ).pack(side="left", padx=(0, 8))
        customtkinter.CTkLabel(
            self.title_frame, text=self.recipe_title, font=customtkinter.CTkFont(size=18, weight="bold")
        ).pack(side="left")

        # Custom Control Buttons
        self.clear_button = customtkinter.CTkButton(
            self.button_frame_controls, text="🗑Clear", width=75, height=32, command=self.clear_recipe,
            fg_color=("gray60", "gray40"), hover_color=("gray50", "gray50")
        )
        self.clear_button.pack(side="left", padx=2)

        self.save_button = customtkinter.CTkButton(
            self.button_frame_controls, text="💾Save", width=65, height=32, command=self.save_recipe
        )
        self.save_button.pack(side="left", padx=2)

        self.load_button = customtkinter.CTkButton(
            self.button_frame_controls, text=self.load_button_text, width=self.load_button_width,
            height=32, command=self.load_recipe
        )
        self.load_button.pack(side="left", padx=2)

    def load_recipe(self):
        # ... (This method remains unchanged)
        """Enhanced recipe loading with validation and metadata support"""
        filepath = filedialog.askopenfilename(
            title="Load Encryption Recipe",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                recipe_data = json.load(f)

            # Handle both old and new recipe formats
            steps = []
            if isinstance(recipe_data, list):
                # Old format - just a list of steps
                steps = recipe_data
            elif isinstance(recipe_data, dict) and "steps" in recipe_data:
                # New format with metadata
                steps = recipe_data["steps"]
                metadata = recipe_data.get("metadata", {})

                # Show metadata info if available
                if metadata:
                    version = metadata.get("version", "Unknown")
                    created = metadata.get("created", "Unknown")
                    step_count = metadata.get("step_count", len(steps))

                    info_msg = f"Recipe Info:\nVersion: {version}\nCreated: {created}\nSteps: {step_count}"
                    if messagebox.showinfo("Recipe Loaded", info_msg):
                        pass  # User acknowledged the info

            if not steps:
                self.app.show_toast("Warning", "Recipe file is empty or invalid.", "warning")
                return

            self.clear_recipe()
            loaded_count = 0
            skipped_count = 0

            for step in steps:
                operation_name = step.get("operation")
                args = step.get("args", {})

                if operation_name:
                    self.add_recipe_step(operation_name, args=args)
                    loaded_count += 1
                else:
                    skipped_count += 1

            # Provide detailed feedback
            status_msg = f"Loaded {loaded_count} operations"
            if skipped_count > 0:
                status_msg += f" ({skipped_count} skipped)"

            self.app.update_status(status_msg, "success")

            if loaded_count > 0:
                self.app.show_toast(
                    "Recipe Loaded",
                    f"Successfully loaded {loaded_count} encryption operations!",
                    "success"
                )

        except json.JSONDecodeError as e:
            self.app.show_toast("File Error", f"Invalid JSON format: {e}", toast_type="error")
        except Exception as e:
            self.app.show_toast("File Error", f"Failed to load recipe: {e}", toast_type="error")

    def add_recipe_step(self, operation_name, args=None):
        # ... (This method remains unchanged)
        """Override to add parameter validation for encryption operations"""
        if args is None:
            args = {}

        # Pre-validate parameters for certain operations
        if operation_name in ["Caesar Encrypt", "Vigenère Encrypt", "Rail Fence Encrypt"]:
            if operation_name == "Caesar Encrypt" and "shift" in args:
                try:
                    shift = int(args["shift"])
                    if not 1 <= shift <= 25:
                        self.app.show_toast("Parameter Error",
                                            f"Invalid Caesar shift: {shift}. Must be 1-25.", "warning")
                        args["shift"] = ""  # Reset to empty for user to fix
                except (ValueError, TypeError):
                    args["shift"] = ""

        # Call parent method to add the step
        super().add_recipe_step(operation_name, args)

        # Provide helpful tips for complex operations
        if operation_name in ["AES Encrypt", "RSA Encrypt", "HMAC-SHA256"]:
            self.app.update_status(f"Added {operation_name} - Remember to set a strong key/password", "info")
        elif operation_name in ["SHA-256", "BLAKE2b", "MD5"]:
            self.app.update_status(f"Added {operation_name} - Hash functions are one-way operations", "info")
        else:
            self.app.update_status(f"Added {operation_name} to encryption recipe", "info")
