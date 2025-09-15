# decrypt_frame.py - FIXED
import base64
import json
import re
from tkinter import filedialog, messagebox

import customtkinter

from .base_frame import BaseFrame, CollapsibleFrame
from ..operations.ciphers import caesar_cipher
# Assuming these imports point to your actual operation functions
from ..operations.encoders import from_base64
from ..operations.hex import from_hex


class DecryptFrame(BaseFrame):
    def __init__(self, master, app, status_bar, **kwargs):
        # Set unique properties for this frame
        self.recipe_title = "Decryption Recipe"
        self.placeholder_text = "🔍 Click an operation or use Auto-Detect to analyze your encrypted data...\n\nTip: Load & Invert reverses encryption recipes!"
        self.load_button_text = "📂Load & Invert"  # No space
        self.load_button_width = 130

        # Inverse operation mapping for recipe inversion
        self.inverse_operations = {
            "To Base64": "From Base64", "From Base64": "To Base64",
            "To Base32": "From Base32", "From Base32": "To Base32",
            "To Base58": "From Base58", "From Base58": "To Base58",
            "To Hex": "From Hex", "From Hex": "To Hex",
            "URL Encode": "URL Decode", "URL Decode": "URL Encode",
            "To Binary": "From Binary", "From Binary": "To Binary",
            "To Morse Code": "From Morse Code", "From Morse Code": "To Morse Code",
            "To QR Code": "From QR Code", "From QR Code": "To QR Code",
            "Caesar Encrypt": "Caesar Decrypt", "Caesar Decrypt": "Caesar Encrypt",
            "Vigenère Encrypt": "Vigenère Decrypt", "Vigenère Decrypt": "Vigenère Encrypt",
            "Playfair Encrypt": "Playfair Decrypt", "Playfair Decrypt": "Playfair Encrypt",
            "Rail Fence Encrypt": "Rail Fence Decrypt", "Rail Fence Decrypt": "Rail Fence Encrypt",
            "AES Encrypt": "AES Decrypt", "AES Decrypt": "AES Encrypt",
            "Blowfish Encrypt": "Blowfish Decrypt", "Blowfish Decrypt": "Blowfish Encrypt",
            "RSA Encrypt": "RSA Decrypt", "RSA Decrypt": "RSA Encrypt",
            "Uppercase": "Lowercase", "Lowercase": "Uppercase",
            "Reverse Text": "Reverse Text"  # Self-inverse
        }

        super().__init__(master, app, status_bar, **kwargs)

    def execute_operation(self, operation_name, input_data, step_frame):
        # ... (This method remains unchanged)
        """Execute decryption operations with enhanced error handling"""
        try:
            # Data Format & Decoding Operations
            if operation_name == "From Base64":
                return from_base64(input_data)
            elif operation_name == "From Base32":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "From Base58":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "From Hex":
                return from_hex(input_data)
            elif operation_name == "URL Decode":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "From Binary":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "From Morse Code":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "From QR Code":
                return self._placeholder_operation(operation_name, input_data)

            # Classic Cipher Decryption
            elif operation_name == "Caesar Decrypt":
                return self._execute_caesar_decrypt(input_data, step_frame)
            elif operation_name == "Atbash Cipher":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "ROT13 Cipher":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Vigenère Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Playfair Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Rail Fence Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Beaufort Cipher":
                return self._placeholder_operation(operation_name, input_data)

            # Modern Symmetric Decryption
            elif operation_name == "AES Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Blowfish Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Twofish Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Serpent Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "ChaCha20-Poly1305":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "Salsa20 Decrypt":
                return self._placeholder_operation(operation_name, input_data)

            # Asymmetric Decryption
            elif operation_name == "RSA Decrypt":
                return self._placeholder_operation(operation_name, input_data)
            elif operation_name == "ECC Decrypt":
                return self._placeholder_operation(operation_name, input_data)

            # Text Processing
            elif operation_name == "Reverse Text":
                return True, input_data[::-1]
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

    def _execute_caesar_decrypt(self, input_data, step_frame):
        # ... (This method remains unchanged)
        """Execute Caesar cipher decryption with validation"""
        try:
            if not hasattr(step_frame, 'param_entry'):
                return False, "Could not find shift parameter."

            shift_text = step_frame.param_entry.get().strip()
            if not shift_text:
                return False, "Shift value cannot be empty."

            shift = int(shift_text)
            if not 1 <= shift <= 25:
                return False, "Shift must be between 1 and 25."

            return caesar_cipher(input_data, shift, decrypt=True)

        except ValueError:
            return False, "Invalid shift value. Must be a number between 1-25."
        except Exception as e:
            return False, f"Caesar decryption failed: {str(e)}"

    def _placeholder_operation(self, operation_name, input_data):
        # ... (This method remains unchanged)
        """Placeholder for operations not yet implemented"""
        placeholder_result = f"[{operation_name} - Implementation Pending] {input_data}"
        return True, placeholder_result

    def create_operations_sidebar(self):
        """Create enhanced operations sidebar for decryption"""
        sidebar_frame = customtkinter.CTkFrame(self, corner_radius=12)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(12, 8), pady=12)
        sidebar_frame.grid_rowconfigure(1, weight=1)
        sidebar_frame.grid_columnconfigure(0, weight=1)

        # Enhanced header
        header_frame = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent", height=50)
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        customtkinter.CTkLabel(
            header_frame, text="🔍Operations", font=customtkinter.CTkFont(size=18, weight="bold")
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

        # Data Formats & Decoders
        decoders_frame = CollapsibleFrame(scrollable_frame, text="🗂Data Formats & Decoders")
        decoders_frame.pack(fill="x", pady=(0, 8))
        decoders_frame.set_algorithm_count(8)
        # (add_button calls remain the same)
        add_button(decoders_frame.content_frame, "From Base64", lambda: self.add_recipe_step("From Base64"), "📋")
        add_button(decoders_frame.content_frame, "From Base32", lambda: self.add_recipe_step("From Base32"), "📋")
        add_button(decoders_frame.content_frame, "From Base58", lambda: self.add_recipe_step("From Base58"), "📋")
        add_button(decoders_frame.content_frame, "From Hex", lambda: self.add_recipe_step("From Hex"), "🔢")
        add_button(decoders_frame.content_frame, "URL Decode", lambda: self.add_recipe_step("URL Decode"), "🌐")
        add_button(decoders_frame.content_frame, "From Binary", lambda: self.add_recipe_step("From Binary"), "💻")
        add_button(decoders_frame.content_frame, "From Morse Code", lambda: self.add_recipe_step("From Morse Code"),
                   "📡")
        add_button(decoders_frame.content_frame, "From QR Code", lambda: self.add_recipe_step("From QR Code"), "📱")

        # Classic Cipher Decryption
        classic_ciphers_frame = CollapsibleFrame(scrollable_frame, text="🏛Classic Cipher Decryption")
        classic_ciphers_frame.pack(fill="x", pady=(0, 8))
        classic_ciphers_frame.set_algorithm_count(7)
        # (add_button calls remain the same)
        add_button(classic_ciphers_frame.content_frame, "Caesar Decrypt",
                   lambda: self.add_recipe_step("Caesar Decrypt"), "🏛")
        add_button(classic_ciphers_frame.content_frame, "Atbash Cipher", lambda: self.add_recipe_step("Atbash Cipher"),
                   "🔄")
        add_button(classic_ciphers_frame.content_frame, "ROT13 Cipher", lambda: self.add_recipe_step("ROT13 Cipher"),
                   "🔄")
        add_button(classic_ciphers_frame.content_frame, "Vigenère Decrypt",
                   lambda: self.add_recipe_step("Vigenère Decrypt"), "🗝")
        add_button(classic_ciphers_frame.content_frame, "Playfair Decrypt",
                   lambda: self.add_recipe_step("Playfair Decrypt"), "🎯")
        add_button(classic_ciphers_frame.content_frame, "Rail Fence Decrypt",
                   lambda: self.add_recipe_step("Rail Fence Decrypt"), "🚂")
        add_button(classic_ciphers_frame.content_frame, "Beaufort Cipher",
                   lambda: self.add_recipe_step("Beaufort Cipher"), "⚓")

        # Modern Symmetric Decryption
        symmetric_frame = CollapsibleFrame(scrollable_frame, text="🛡Modern Symmetric Decryption")
        symmetric_frame.pack(fill="x", pady=(0, 8))
        symmetric_frame.set_algorithm_count(6)
        # (add_button calls remain the same)
        add_button(symmetric_frame.content_frame, "AES Decrypt", lambda: self.add_recipe_step("AES Decrypt"), "🛡")
        add_button(symmetric_frame.content_frame, "Blowfish Decrypt", lambda: self.add_recipe_step("Blowfish Decrypt"),
                   "🐡")
        add_button(symmetric_frame.content_frame, "Twofish Decrypt", lambda: self.add_recipe_step("Twofish Decrypt"),
                   "🐟")
        add_button(symmetric_frame.content_frame, "Serpent Decrypt", lambda: self.add_recipe_step("Serpent Decrypt"),
                   "🐍")
        add_button(symmetric_frame.content_frame, "ChaCha20-Poly1305",
                   lambda: self.add_recipe_step("ChaCha20-Poly1305"), "⚡")
        add_button(symmetric_frame.content_frame, "Salsa20 Decrypt", lambda: self.add_recipe_step("Salsa20 Decrypt"),
                   "💃")

        # Asymmetric Decryption
        asymmetric_frame = CollapsibleFrame(scrollable_frame, text="🔐Asymmetric Decryption")
        asymmetric_frame.pack(fill="x", pady=(0, 8))
        asymmetric_frame.set_algorithm_count(2)
        # (add_button calls remain the same)
        add_button(asymmetric_frame.content_frame, "RSA Decrypt", lambda: self.add_recipe_step("RSA Decrypt"), "🔐")
        add_button(asymmetric_frame.content_frame, "ECC Decrypt", lambda: self.add_recipe_step("ECC Decrypt"), "🌐")

        # Text Utilities
        text_utils_frame = CollapsibleFrame(scrollable_frame, text="📝Text Utilities")
        text_utils_frame.pack(fill="x", pady=(0, 8))
        text_utils_frame.set_algorithm_count(4)
        # (add_button calls remain the same)
        add_button(text_utils_frame.content_frame, "Reverse Text", lambda: self.add_recipe_step("Reverse Text"), "🔄")
        add_button(text_utils_frame.content_frame, "Uppercase", lambda: self.add_recipe_step("Uppercase"), "🔠")
        add_button(text_utils_frame.content_frame, "Lowercase", lambda: self.add_recipe_step("Lowercase"), "🔡")
        add_button(text_utils_frame.content_frame, "Remove Spaces", lambda: self.add_recipe_step("Remove Spaces"), "✂")

        # Statistics at bottom
        stats_frame = customtkinter.CTkFrame(sidebar_frame, fg_color=("gray90", "gray20"), height=40)
        stats_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

        total_algorithms = 8 + 7 + 6 + 2 + 4  # 27 total algorithms
        customtkinter.CTkLabel(
            stats_frame, text=f"📊 Total: {total_algorithms} algorithms available",
            font=customtkinter.CTkFont(size=11, weight="bold"), text_color=("gray30", "gray70")
        ).pack(pady=10)

    def create_recipe_panel(self):
        """Create a consistent recipe panel by calling the base and customizing it."""
        super().create_recipe_panel()  # Create the base structure

        # --- Customizations for DecryptFrame ---

        # Custom Title
        customtkinter.CTkLabel(
            self.title_frame, text="🔓", font=customtkinter.CTkFont(size=20)
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
        """Enhanced recipe loading with inversion capability"""
        filepath = filedialog.askopenfilename(
            title="Load and Invert Recipe",
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
                steps = recipe_data
            elif isinstance(recipe_data, dict) and "steps" in recipe_data:
                steps = recipe_data["steps"]
                # Check if this is already a decryption recipe
                metadata = recipe_data.get("metadata", {})
                recipe_type = metadata.get("recipe_type", "")

                if recipe_type == "decrypt":
                    # This is already a decryption recipe, load normally
                    if messagebox.askyesno("Recipe Type",
                                           "This appears to be a decryption recipe. Load without inversion?"):
                        self._load_normal_recipe(steps)
                        return

            if not steps:
                self.app.show_toast("Warning", "Recipe file is empty or invalid.", "warning")
                return

            # Invert the recipe
            self.clear_recipe()
            inverted_count = 0
            skipped_count = 0

            # Process steps in reverse order for proper inversion
            for step in reversed(steps):
                original_op_name = step.get("operation")
                inverted_op_name = self.inverse_operations.get(original_op_name)

                if inverted_op_name:
                    args = step.get("args", {})
                    self.add_recipe_step(inverted_op_name, args=args)
                    inverted_count += 1
                else:
                    self.app.show_toast("Warning", f"No inverse found for '{original_op_name}'. Skipping.", "warning")
                    skipped_count += 1

            # Provide feedback
            status_msg = f"Inverted {inverted_count} operations"
            if skipped_count > 0:
                status_msg += f" ({skipped_count} skipped)"

            self.app.update_status(status_msg, "success")

            if inverted_count > 0:
                self.app.show_toast(
                    "Recipe Inverted",
                    f"Successfully inverted {inverted_count} operations!\nReady for decryption.",
                    "success"
                )

        except json.JSONDecodeError as e:
            self.app.show_toast("File Error", f"Invalid JSON format: {e}", "error")
        except Exception as e:
            self.app.show_toast("File Error", f"Failed to load recipe: {e}", "error")

    def _load_normal_recipe(self, steps):
        # ... (This method remains unchanged)
        """Load recipe normally without inversion"""
        self.clear_recipe()
        loaded_count = 0

        for step in steps:
            operation_name = step.get("operation")
            args = step.get("args", {})

            if operation_name:
                self.add_recipe_step(operation_name, args=args)
                loaded_count += 1

        if loaded_count > 0:
            self.app.update_status(f"Loaded {loaded_count} decryption operations", "success")
            self.app.show_toast("Recipe Loaded", f"Successfully loaded {loaded_count} decryption operations!",
                                "success")

    def add_recipe_step(self, operation_name, args=None):
        # ... (This method remains unchanged)
        """Override to add helpful tips for decryption operations"""
        if args is None:
            args = {}

        # Call parent method to add the step
        super().add_recipe_step(operation_name, args)

        # Provide helpful tips for complex operations
        if operation_name in ["AES Decrypt", "RSA Decrypt"]:
            self.app.update_status(f"Added {operation_name} - You'll need the correct key", "info")
        elif operation_name == "Caesar Decrypt":
            self.app.update_status(f"Added Caesar Decrypt - Try shifts 1-25 if unknown", "info")
        elif operation_name in ["From Base64", "From Hex"]:
            self.app.update_status(f"Added {operation_name} - Common encoding format", "info")
        else:
            self.app.update_status(f"Added {operation_name} to decryption recipe", "info")

    # --- AUTO-DETECT METHODS ---
    # ... (These methods remain unchanged)
    def auto_detect_from_input(self):
        """Run a series of checks on the input data to suggest decryption methods"""
        text = self.app.get_input_text().strip()
        if not text:
            self.app.show_toast("Auto-Detect", "Input is empty. Nothing to analyze.", "info")
            return

        suggestions = self._run_detection_heuristics(text)

        if not suggestions:
            self.app.show_toast("Auto-Detect", "No common patterns detected.", "info")
        else:
            self._show_suggestions_dialog(suggestions)

    def _run_detection_heuristics(self, text):
        """Core logic for detecting patterns in text"""
        suggestions = []

        # Base64 detection
        if self._is_base64(text):
            suggestions.append({
                "operation": "From Base64",
                "confidence": 0.9,
                "reason": "Text matches Base64 character set and padding",
                "pattern": "Contains A-Z, a-z, 0-9, +, /, ="
            })

        # Hex detection
        if self._is_hex(text):
            suggestions.append({
                "operation": "From Hex",
                "confidence": 0.9,
                "reason": "Text consists of valid hexadecimal characters",
                "pattern": "Contains 0-9, A-F, a-f"
            })

        # Caesar cipher detection (simple frequency analysis)
        caesar_confidence = self._analyze_caesar(text)
        if caesar_confidence > 0.5:
            suggestions.append({
                "operation": "Caesar Decrypt",
                "confidence": caesar_confidence,
                "reason": "Text shows patterns consistent with Caesar cipher",
                "pattern": f"Letter frequency analysis suggests shift cipher (confidence: {caesar_confidence:.1%})"
            })

        # Binary detection
        if self._is_binary(text):
            suggestions.append({
                "operation": "From Binary",
                "confidence": 0.95,
                "reason": "Text appears to be binary encoded",
                "pattern": "Contains only 0s and 1s and grouped by 8 bits"  # More descriptive
            })

        # Morse code detection
        if self._is_morse_code(text):
            suggestions.append({
                "operation": "From Morse Code",
                "confidence": 0.8,
                "reason": "Text appears to be Morse code",
                "pattern": "Contains dots, dashes, and proper spacing"
            })

        # URL encoding detection
        if self._is_url_encoded(text):
            suggestions.append({
                "operation": "URL Decode",
                "confidence": 0.75,
                "reason": "Text appears to be URL encoded",
                "pattern": "Contains % encoding sequences"
            })

        # Sort by confidence
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        return suggestions[:5]  # Return top 5 suggestions

    def _is_base64(self, text):
        """Check if text is likely Base64 encoded"""
        try:
            cleaned = re.sub(r'\s', '', text)
            if len(cleaned) % 4 != 0:
                return False
            # Ensure it's not just a generic string but looks like base64
            if not re.fullmatch(r'[A-Za-z0-9+/]*={0,2}', cleaned):
                return False
            base64.b64decode(cleaned, validate=True)
            return True
        except Exception:
            return False

    def _is_hex(self, text):
        """Check if text is hexadecimal"""
        try:
            cleaned = re.sub(r'\s', '', text)
            if not cleaned: return False
            if not re.fullmatch(r'[0-9A-Fa-f]+', cleaned):
                return False
            int(cleaned, 16)
            return len(cleaned) % 2 == 0
        except ValueError:
            return False

    def _is_binary(self, text):
        """Check if text is binary"""
        cleaned = re.sub(r'\s', '', text)
        return all(c in '01' for c in cleaned) and len(cleaned) > 0 and (len(cleaned) % 8 == 0)

    def _is_morse_code(self, text):
        """Check if text is Morse code"""
        # Improved check: must contain actual morse symbols, not just spaces
        cleaned = text.strip()
        if not cleaned:
            return False
        # Must contain at least one dot or dash
        if not ('.' in cleaned or '-' in cleaned):
            return False
        # Must only contain valid Morse characters and separators
        morse_pattern = re.compile(r"^[.\-/\s]+$")
        return bool(morse_pattern.fullmatch(cleaned))

    def _is_url_encoded(self, text):
        """Check if text is URL encoded"""
        # A simple heuristic: check for % followed by two hex digits, and maybe + for spaces
        return '%' in text and (len(re.findall(r'%[0-9A-Fa-f]{2}', text)) > 0 or '+' in text)

    def _analyze_caesar(self, text):
        """Perform basic frequency analysis for Caesar cipher detection"""
        if not text or len(text) < 10 or not any(c.isalpha() for c in text):
            return 0.0

        alpha_text = "".join(filter(str.isalpha, text.upper()))
        if not alpha_text:
            return 0.0

        letter_count = {chr(i): 0 for i in range(65, 91)}
        for char in alpha_text:
            letter_count[char] += 1

        total_letters = len(alpha_text)
        if total_letters == 0: return 0.0  # Avoid division by zero

        frequencies = [count / total_letters for count in letter_count.values()]

        # Calculate variance (high variance might indicate natural language, low variance might indicate cipher)
        # Using a slightly different threshold for confidence
        mean_freq = sum(frequencies) / len(frequencies)
        variance = sum((f - mean_freq) ** 2 for f in frequencies) / len(frequencies)

        if variance < 0.0005: return 0.8  # Very uniform distribution (high confidence for cipher)
        if variance < 0.001: return 0.7
        if variance < 0.002: return 0.6
        return 0.3  # Higher variance, lower confidence

    def _show_suggestions_dialog(self, suggestions):
        """Show a dialog with decryption suggestions"""
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("🔍 Auto-Detect Results")
        dialog.geometry("600x500")
        dialog.transient(self.app)
        dialog.resizable(False, False)
        dialog.grab_set()

        dialog.update_idletasks()
        # Center the dialog relative to the main app window
        x = self.app.winfo_x() + (self.app.winfo_width() - dialog.winfo_width()) // 2
        y = self.app.winfo_y() + (self.app.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        main_frame = customtkinter.CTkFrame(dialog, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        header_label = customtkinter.CTkLabel(main_frame, text="🎯 Detected Possible Decryption Methods",
                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        header_label.grid(row=0, column=0, pady=(10, 20), sticky="w")

        suggestions_frame = customtkinter.CTkScrollableFrame(main_frame, height=300)
        suggestions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        suggestions_frame.grid_columnconfigure(0, weight=1)

        for i, suggestion in enumerate(suggestions):
            card_frame = customtkinter.CTkFrame(suggestions_frame, corner_radius=8)
            card_frame.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
            card_frame.grid_columnconfigure(1, weight=1)

            confidence = suggestion["confidence"]
            confidence_color, confidence_text = ("#28A745", "HIGH") if confidence >= 0.8 else (
                ("#FFC107", "MEDIUM") if confidence >= 0.6 else ("#DC3545", "LOW"))

            customtkinter.CTkLabel(card_frame, text=f"{confidence_text}\n{confidence:.0%}",
                                   font=customtkinter.CTkFont(size=10, weight="bold"), text_color=confidence_color,
                                   width=60).grid(row=0, column=0, padx=15, pady=15, sticky="w")

            details_frame = customtkinter.CTkFrame(card_frame, fg_color="transparent")
            details_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=15)
            customtkinter.CTkLabel(details_frame, text=f"🔧 {suggestion['operation']}",
                                   font=customtkinter.CTkFont(size=14, weight="bold"), anchor="w").pack(fill="x")
            customtkinter.CTkLabel(details_frame, text=suggestion["reason"], font=customtkinter.CTkFont(size=12),
                                   anchor="w", text_color=("gray20", "gray80")).pack(fill="x", pady=(2, 0))
            customtkinter.CTkLabel(details_frame, text=f"Pattern: {suggestion['pattern']}",
                                   font=customtkinter.CTkFont(size=10), anchor="w", text_color=("gray40", "gray60"),
                                   wraplength=300).pack(fill="x", pady=(2, 0))

            customtkinter.CTkButton(card_frame, text="+Add", width=80, height=30,
                                    command=lambda op=suggestion['operation']: self._add_suggested_operation(op,
                                                                                                             dialog),
                                    font=customtkinter.CTkFont(size=12)).grid(row=0, column=2, padx=15,
                                                                              pady=15)  # No space

        button_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", pady=10)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        customtkinter.CTkButton(button_frame, text="✨Add All High Confidence",
                                command=lambda: self._add_high_confidence_suggestions(suggestions, dialog), height=40,
                                font=customtkinter.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=(0, 10),
                                                                                         sticky="ew")  # No space
        customtkinter.CTkButton(button_frame, text="Close", command=dialog.destroy, height=40,
                                fg_color=("gray60", "gray40"), hover_color=("gray50", "gray50")).grid(row=0, column=1,
                                                                                                      padx=(10, 0),
                                                                                                      sticky="ew")

    def _add_suggested_operation(self, operation_name, dialog):
        """Add a suggested operation to the recipe"""
        self.add_recipe_step(operation_name)
        self.app.show_toast("Added", f"Added {operation_name} to recipe!", "success")
        dialog.destroy()

    def _add_high_confidence_suggestions(self, suggestions, dialog):
        """Add all high confidence suggestions to the recipe"""
        added_count = 0
        for suggestion in suggestions:
            if suggestion["confidence"] >= 0.8:
                self.add_recipe_step(suggestion["operation"])
                added_count += 1

        if added_count > 0:
            self.app.show_toast("Added", f"Added {added_count} high-confidence operations!", "success")
        else:
            self.app.show_toast("Info", "No high-confidence suggestions found.", "info")

        dialog.destroy()
