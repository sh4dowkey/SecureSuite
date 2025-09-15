# base_frame.py - FIXED
import gc
import json
import queue
import threading
import time
from tkinter import filedialog, messagebox

import customtkinter
import pyperclip


class CollapsibleFrame(customtkinter.CTkFrame):
    """Optimized collapsible frame with minimal overhead"""

    def __init__(self, master, text="", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.collapsed = True

        # Simplified header
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent", height=35)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Toggle button
        self.toggle_button = customtkinter.CTkButton(
            self.header_frame,
            text="▶",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("gray80", "gray25"),
            command=self.toggle,
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        self.toggle_button.grid(row=0, column=0, sticky="w", padx=3, pady=2)

        # Title
        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text=text,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Count indicator
        self.count_label = customtkinter.CTkLabel(
            self.header_frame,
            text="",
            font=customtkinter.CTkFont(size=10),
            text_color=("gray50", "gray60")
        )
        self.count_label.grid(row=0, column=2, sticky="e", padx=8, pady=2)

        self.content_frame = customtkinter.CTkFrame(self, fg_color="transparent")

    def set_algorithm_count(self, count):
        """Update the algorithm count display"""
        self.count_label.configure(text=f"({count})" if count > 0 else "")

    def toggle(self):
        """Fast toggle without animation"""
        if self.collapsed:
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=3)
            self.toggle_button.configure(text="▼")
            self.collapsed = False
        else:
            self.content_frame.grid_forget()
            self.toggle_button.configure(text="▶")
            self.collapsed = True


class BaseFrame(customtkinter.CTkFrame):
    def __init__(self, master, app, status_bar, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.status_bar = status_bar
        self.configure(fg_color="transparent")

        # Optimized state management
        self.current_step_index = 0
        self.recipe_placeholder = None
        self.result_queue = queue.Queue()
        self.processing_cancelled = False
        self.current_thread = None
        self.operation_start_time = 0

        # Performance settings
        self.CHUNK_SIZE = 2 * 1024 * 1024  # 2MB chunks
        self.UPDATE_INTERVAL = 50  # Faster UI updates

        # --- KEY FIX FOR PANEL SIZING AND CLIPPING ---
        # Adjusted weights and minsize to give recipe panel more space
        self.grid_columnconfigure(0, weight=2, minsize=750)  # Sidebar
        self.grid_columnconfigure(1, weight=3, minsize=350)  # Recipe panel
        self.grid_columnconfigure(2, weight=5, minsize=800)  # I/O panel
        self.grid_rowconfigure(0, weight=1)

        # Build UI with deferred loading for speed
        self._build_ui_fast()

        # Setup keyboard shortcuts properly
        self._setup_keyboard_shortcuts()

        # Show frame after everything is built
        self.pack(fill="both", expand=True)

    def _build_ui_fast(self):
        """Optimized UI building for speed"""
        # Use threading for non-critical UI elements
        self.create_operations_sidebar()
        self.create_recipe_panel()
        self.create_io_panel()

        # Defer placeholder update to prevent blocking
        self.after_idle(self.update_recipe_placeholder)

    def _setup_keyboard_shortcuts(self):
        """Working keyboard shortcuts using app-level binding"""
        # Focus the frame to receive keyboard events
        self.focus_set()

        # Bind directly to the app window
        try:
            app_window = self.winfo_toplevel()
            app_window.bind_all("<Return>", self._on_enter_pressed)
            app_window.bind_all("<Shift-Return>", self._on_shift_enter_pressed)
            app_window.bind_all("<Escape>", self._on_escape_pressed)
        except Exception:
            # Fallback to frame binding if app binding fails
            self.bind("<Return>", self._on_enter_pressed)
            self.bind("<Shift-Return>", self._on_shift_enter_pressed)
            self.bind("<Escape>", self._on_escape_pressed)

    def _on_enter_pressed(self, event=None):
        """Handle Enter key - execute single step"""
        if not self.app.is_processing and hasattr(self, 'step_button'):
            self.process_step()
        return "break"

    def _on_shift_enter_pressed(self, event=None):
        """Handle Shift+Enter - execute full recipe"""
        if not self.app.is_processing and hasattr(self, 'bake_button'):
            self.bake_recipe()
        return "break"

    def _on_escape_pressed(self, event=None):
        """Handle Escape key - cancel/clear"""
        if self.app.is_processing:
            self.cancel_processing()
        else:
            self.clear_all_fields()
        return "break"

    def set_processing_state(self, is_processing: bool, progress_text=""):
        """Ultra-fast processing state management"""
        self.app.set_processing_state(is_processing)

        # Batch state updates for performance
        state = "disabled" if is_processing else "normal"
        widgets = [self.bake_button, self.step_button,
                   getattr(self, 'clear_button', None),
                   getattr(self, 'load_button', None),
                   getattr(self, 'save_button', None)]

        for widget in widgets:
            if widget:
                widget.configure(state=state)

        # Optimized cancel button handling
        if is_processing:
            if not hasattr(self, 'cancel_button'):
                self.cancel_button = customtkinter.CTkButton(
                    self.button_frame,
                    text="❌Cancel",  # No space for consistency
                    command=self.cancel_processing,
                    fg_color=("gray70", "gray30"),
                    hover_color=("gray60", "gray40"),
                    width=75
                )
            self.cancel_button.grid(row=0, column=2, padx=(5, 0), sticky="ew")
            if progress_text:
                self.app.update_status(progress_text, "processing", show_progress=True)
        else:
            if hasattr(self, 'cancel_button'):
                self.cancel_button.grid_forget()
            self.processing_cancelled = False

    def cancel_processing(self):
        """Fast processing cancellation"""
        self.processing_cancelled = True
        self.app.update_status("Cancelling...", "warning")

        # Force cleanup after short timeout
        self.after(2000, self._force_cleanup)

    def _force_cleanup(self):
        """Force thread cleanup"""
        if self.current_thread and self.current_thread.is_alive():
            self.app.show_toast("Cancelled", "Operation stopped", "warning")
        self._fast_reset()

    def reset_step_state(self, event=None):
        """Fast step state reset"""
        self.current_step_index = 0
        self.processing_cancelled = False

        # Batch clear visual indicators
        for widget in self.recipe_scrollable_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame):
                widget.configure(border_width=0)

        self.app.update_status("Ready", "info")

    def _fast_reset(self):
        """Optimized reset without UI blocking"""
        self.reset_step_state()
        self.set_processing_state(False)
        gc.collect()

    def process_step(self):
        """Optimized step processing"""
        if self.app.is_processing:
            return

        self.operation_start_time = time.time()
        self.set_processing_state(True, "Processing step...")

        self.current_thread = threading.Thread(target=self._worker_process_step, daemon=True)
        self.current_thread.start()
        self.after(self.UPDATE_INTERVAL, self.check_queue)

    def bake_recipe(self):
        """Optimized recipe baking"""
        if self.app.is_processing:
            return

        self.operation_start_time = time.time()
        self.set_processing_state(True, "Baking recipe...")

        self.current_thread = threading.Thread(target=self._worker_bake_recipe, daemon=True)
        self.current_thread.start()
        self.after(self.UPDATE_INTERVAL, self.check_queue)

    def _worker_process_step(self):
        """Optimized worker with error handling"""
        try:
            recipe_steps = [child for child in self.recipe_scrollable_frame.winfo_children()
                            if isinstance(child, customtkinter.CTkFrame)]

            if not recipe_steps:
                self.result_queue.put(("error", ("Recipe Error", "Please add an operation.")))
                return

            if self.current_step_index >= len(recipe_steps):
                self.result_queue.put(("reset", "Recipe completed. Ready for new operation."))
                return

            current_data = self.input_textbox.get("1.0", "end-1c")

            if self.processing_cancelled:
                return

            # Process with optimized error handling
            for i in range(self.current_step_index + 1):
                if self.processing_cancelled:
                    return

                step_frame = recipe_steps[i]
                operation_name = step_frame.op_name

                try:
                    success, current_data = self.execute_operation(operation_name, current_data, step_frame)
                    if not success:
                        self.result_queue.put(("error", ("Operation Failed",
                                                         f"{operation_name}: {current_data}")))
                        return
                except Exception as e:
                    self.result_queue.put(("error", ("Execution Error",
                                                     f"{operation_name} failed: {str(e)}")))
                    return

            self.result_queue.put(("step_success", (current_data, self.current_step_index)))

        except Exception as e:
            self.result_queue.put(("error", ("System Error", f"Processing failed: {str(e)}")))

    def _worker_bake_recipe(self):
        """Optimized recipe baking with robust error handling"""
        try:
            self.reset_step_state()
            current_data = self.input_textbox.get("1.0", "end-1c")
            recipe_steps = [child for child in self.recipe_scrollable_frame.winfo_children()
                            if isinstance(child, customtkinter.CTkFrame)]

            if not current_data.strip():
                self.result_queue.put(("error", ("Input Error", "Input field is empty.")))
                return

            if not recipe_steps:
                self.result_queue.put(("error", ("Recipe Error", "No operations in recipe.")))
                return

            # Optimized processing with progress tracking
            total_steps = len(recipe_steps)
            for step_idx, step_frame in enumerate(recipe_steps):
                if self.processing_cancelled:
                    return

                operation_name = step_frame.op_name
                self.result_queue.put(("progress", f"Step {step_idx + 1}/{total_steps}: {operation_name}"))

                try:
                    success, current_data = self.execute_operation(operation_name, current_data, step_frame)
                    if not success:
                        self.result_queue.put(("error", ("Operation Failed",
                                                         f"{operation_name}: {current_data}")))
                        return
                except Exception as e:
                    self.result_queue.put(("error", ("Execution Error",
                                                     f"{operation_name} failed: {str(e)}")))
                    return

                # Memory management for large data
                if len(current_data) > self.CHUNK_SIZE * 5:
                    gc.collect()

            self.result_queue.put(("bake_success", current_data))

        except Exception as e:
            self.result_queue.put(("error", ("System Error", f"Recipe failed: {str(e)}")))

    def check_queue(self):
        """Ultra-fast queue processing"""
        processed_messages = 0
        max_messages_per_check = 10  # Prevent UI blocking

        try:
            while processed_messages < max_messages_per_check:
                try:
                    message = self.result_queue.get_nowait()
                    msg_type, data = message
                    processed_messages += 1

                    if msg_type == "progress":
                        self.app.update_status(data, "processing", show_progress=True)

                    elif msg_type == "bake_success":
                        self._handle_success(data, "Recipe completed successfully!")
                        return  # Stop processing

                    elif msg_type == "step_success":
                        self._handle_step_success(data)
                        return  # Stop processing

                    elif msg_type == "reset":
                        self.app.update_status(data, "info")
                        self._fast_reset()
                        return  # Stop processing

                    elif msg_type == "error":
                        title, msg = data
                        self.app.show_toast(title, msg, "error")
                        self._fast_reset()
                        return  # Stop processing

                except queue.Empty:
                    break

        except Exception as e:
            print(f"Queue error: {e}")
            self._fast_reset()
            return

        # Continue if still processing
        if self.app.is_processing:
            self.after(self.UPDATE_INTERVAL, self.check_queue)

    def _handle_success(self, result_data, success_message):
        """Fast success handling with performance metrics"""
        # Batch UI updates
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", result_data)
        self.output_textbox.configure(state="disabled")

        # Performance metrics
        elapsed = time.time() - self.operation_start_time
        size = len(result_data)

        if elapsed > 0.1 and size > 1000:
            rate = size / elapsed / 1024
            success_message += f" ({size:,} chars, {elapsed:.2f}s, {rate:.1f} KB/s)"

        self.app.update_status(success_message, "success")
        self.set_processing_state(False)

    def _handle_step_success(self, data):
        """Fast step success handling"""
        result_data, step_index = data

        # Update output
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", result_data)
        self.output_textbox.configure(state="disabled")

        # Visual feedback
        recipe_steps = [child for child in self.recipe_scrollable_frame.winfo_children()
                        if isinstance(child, customtkinter.CTkFrame)]

        # Clear all borders first
        for widget in recipe_steps:
            widget.configure(border_width=0)

        # Highlight current step
        if step_index < len(recipe_steps):
            current_step_frame = recipe_steps[step_index]
            current_step_frame.configure(border_width=2, border_color=("#3B8ED0", "#1F6AA5"))

            elapsed = time.time() - self.operation_start_time
            step_info = f"Step {step_index + 1}: {current_step_frame.op_name} completed"
            if elapsed > 0.05:
                step_info += f" ({elapsed:.2f}s)"

            self.app.update_status(step_info, "success")
            self.current_step_index += 1

        self.set_processing_state(False)

    def clear_all_fields(self):
        """Fast field clearing"""
        if hasattr(self, 'input_textbox'):
            self.input_textbox.delete("1.0", "end")
        if hasattr(self, 'output_textbox'):
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.configure(state="disabled")
        self.clear_recipe()
        self.app.update_status("All fields cleared", "info")

    def add_recipe_step(self, operation_name, args=None):
        """Optimized recipe step addition"""
        if args is None:
            args = {}

        self.update_recipe_placeholder()

        # Create optimized step frame
        step_frame = customtkinter.CTkFrame(
            self.recipe_scrollable_frame,
            corner_radius=6,
            height=50
        )
        step_frame.pack(fill="x", padx=6, pady=2)
        step_frame.op_name = operation_name
        step_frame.op_args = args

        # Optimized icon selection
        icon = "🔒" if "Encrypt" in operation_name else "🔓" if "Decrypt" in operation_name else "⚙️"

        icon_label = customtkinter.CTkLabel(
            step_frame,
            text=icon,
            font=customtkinter.CTkFont(size=16),
            width=35
        )
        icon_label.pack(side="left", padx=(10, 5), pady=10)

        # Parameter container
        param_container = customtkinter.CTkFrame(step_frame, fg_color="transparent")
        param_container.pack(side="left", fill="x", expand=True, padx=3, pady=6)

        # Operation name
        name_label = customtkinter.CTkLabel(
            param_container,
            text=operation_name,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        name_label.pack(side="top", anchor="w")

        # Parameter inputs
        if "Caesar" in operation_name:
            shift_val = args.get("shift", "")
            entry = customtkinter.CTkEntry(
                param_container,
                placeholder_text="Shift (1-25)",
                width=100,
                height=25
            )
            entry.insert(0, str(shift_val))
            entry.pack(side="top", anchor="w", pady=(2, 0))
            step_frame.param_entry = entry

        elif "AES" in operation_name:
            key = args.get("key", "")
            entry = customtkinter.CTkEntry(
                param_container,
                placeholder_text="Enter Key...",
                height=25
            )
            entry.insert(0, key)
            entry.pack(side="top", anchor="w", pady=(2, 0))
            step_frame.param_entry = entry

        # Remove button
        remove_button = customtkinter.CTkButton(
            step_frame,
            text="✖",
            width=28,
            height=28,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=lambda sf=step_frame: self._remove_step(sf)
        )
        remove_button.pack(side="right", padx=(3, 8), pady=10)

        # Update UI efficiently
        self.reset_step_state()
        self.after_idle(self.update_recipe_placeholder)

        # Auto-scroll to new step
        self.after_idle(lambda: self.recipe_scrollable_frame._parent_canvas.yview_moveto(1.0))

    def _remove_step(self, step_frame):
        """Fast step removal"""
        step_frame.destroy()
        self.after_idle(self.update_recipe_placeholder)
        self.reset_step_state()
        self.app.update_status(f"Removed: {step_frame.op_name}", "info")

    def save_recipe(self):
        """Fast recipe saving"""
        recipe_steps = [child for child in self.recipe_scrollable_frame.winfo_children()
                        if isinstance(child, customtkinter.CTkFrame)]

        if not recipe_steps:
            self.app.show_toast("Warning", "Recipe is empty", "warning")
            return

        recipe_data = {
            "metadata": {
                "version": "2.0",
                "created": time.strftime("%Y-%m-%d %H:%M:%S"),
                "step_count": len(recipe_steps),
                "recipe_type": self.__class__.__name__.replace("Frame", "").lower()
            },
            "steps": []
        }

        # Fast data collection
        for step_frame in recipe_steps:
            operation_name = step_frame.op_name
            args = {}

            if hasattr(step_frame, 'param_entry'):
                param_value = step_frame.param_entry.get()
                if "Caesar" in operation_name:
                    args["shift"] = param_value
                elif "AES" in operation_name:
                    args["key"] = param_value

            recipe_data["steps"].append({
                "operation": operation_name,
                "args": args
            })

        filepath = filedialog.asksaveasfilename(
            title="Save Recipe",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(recipe_data, f, indent=2)

                self.app.show_toast("Success", f"Recipe saved! ({len(recipe_steps)} steps)", "success")

            except Exception as e:
                self.app.show_toast("Save Error", f"Failed to save: {str(e)}", "error")

    def update_recipe_placeholder(self):
        """Fast placeholder management"""
        has_steps = any(isinstance(child, customtkinter.CTkFrame)
                        for child in self.recipe_scrollable_frame.winfo_children())

        if not has_steps:
            if not (self.recipe_placeholder and self.recipe_placeholder.winfo_exists()):
                self.recipe_placeholder = customtkinter.CTkLabel(
                    self.recipe_scrollable_frame,
                    text=self.placeholder_text,
                    font=customtkinter.CTkFont(size=13),
                    text_color=("gray50", "gray60"),
                    wraplength=320,  # Increased wraplength for wider panel
                    justify="center"
                )
            self.recipe_placeholder.pack(expand=True, pady=30)
        else:
            if self.recipe_placeholder and self.recipe_placeholder.winfo_exists():
                self.recipe_placeholder.pack_forget()

    def create_recipe_panel(self):
        """ This method is now overridden in Encrypt/Decrypt frames to set specific titles/buttons """
        # The base logic is here, but child classes will call super() and then customize
        recipe_frame = customtkinter.CTkFrame(self, corner_radius=12)
        recipe_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=12)
        recipe_frame.grid_rowconfigure(1, weight=1)
        recipe_frame.grid_columnconfigure(0, weight=1)

        # Header
        recipe_header = customtkinter.CTkFrame(recipe_frame, fg_color="transparent", height=50)
        recipe_header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")
        recipe_header.grid_columnconfigure(1, weight=1)

        # Title will be set by subclass
        self.title_frame = customtkinter.CTkFrame(recipe_header, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="w")

        # Control buttons will be added by subclass
        self.button_frame_controls = customtkinter.CTkFrame(recipe_header, fg_color="transparent")
        self.button_frame_controls.grid(row=0, column=2, sticky="e")

        # Recipe area
        self.recipe_scrollable_frame = customtkinter.CTkScrollableFrame(
            recipe_frame,
            corner_radius=8
        )
        self.recipe_scrollable_frame.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

        # Main action button panel
        self.button_frame = customtkinter.CTkFrame(recipe_frame, fg_color="transparent", height=60)
        self.button_frame.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        # Action Buttons - NO SPACES in text
        self.step_button = customtkinter.CTkButton(
            self.button_frame,
            text="▶️Step",
            height=45,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            fg_color=("gray65", "gray35"),
            hover_color=("gray55", "gray45"),
            command=self.process_step
        )
        self.step_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.bake_button = customtkinter.CTkButton(
            self.button_frame,
            text="🏭Bake Recipe!",
            height=45,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            command=self.bake_recipe
        )
        self.bake_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def create_io_panel(self):
        """Create MUCH LARGER I/O panel for professional use"""
        io_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        io_frame.grid(row=0, column=2, sticky="nsew", padx=(8, 12), pady=12)  # Consistent padding
        io_frame.grid_rowconfigure((1, 3), weight=1)  # Both text areas get equal weight
        io_frame.grid_columnconfigure(0, weight=1)

        # Input section header
        input_header = customtkinter.CTkFrame(io_frame, fg_color="transparent", height=40)
        input_header.grid(row=0, column=0, padx=8, pady=(0, 5), sticky="ew")
        input_header.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(
            input_header,
            text="📝Input",
            font=customtkinter.CTkFont(size=18, weight="bold")  # Larger font
        ).grid(row=0, column=0, sticky="w")

        # Input controls
        input_controls = customtkinter.CTkFrame(input_header, fg_color="transparent")
        input_controls.grid(row=0, column=2, sticky="e")

        customtkinter.CTkButton(
            input_controls, text="📋Paste", width=70, height=30, command=self.paste_to_input
        ).pack(side="left", padx=2)

        customtkinter.CTkButton(
            input_controls, text="📂Open", width=65, height=30, command=self.open_from_file
        ).pack(side="left", padx=2)

        customtkinter.CTkButton(
            input_controls, text="❌Clear", width=65, height=30, command=self.clear_input,
            fg_color=("gray65", "gray35"), hover_color=("gray55", "gray45")
        ).pack(side="left", padx=2)

        # LARGER Input textbox
        input_container = customtkinter.CTkFrame(io_frame)
        input_container.grid(row=1, column=0, padx=8, pady=(0, 5), sticky="nsew")
        input_container.grid_rowconfigure(0, weight=1)
        input_container.grid_columnconfigure(0, weight=1)

        self.input_textbox = customtkinter.CTkTextbox(
            input_container, corner_radius=8, font=customtkinter.CTkFont(family="Consolas", size=12)  # Larger font
        )
        self.input_textbox.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.input_textbox.bind("<KeyRelease>", self._on_input_change)

        self.input_counter = customtkinter.CTkLabel(
            input_container, text="0 characters", font=customtkinter.CTkFont(size=10), text_color=("gray50", "gray60")
        )
        self.input_counter.grid(row=1, column=0, sticky="se", padx=8, pady=(0, 4))

        # Output section header
        output_header = customtkinter.CTkFrame(io_frame, fg_color="transparent", height=40)
        output_header.grid(row=2, column=0, padx=8, pady=(10, 5), sticky="ew")
        output_header.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(
            output_header, text="📤Output", font=customtkinter.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        # Output controls
        output_controls = customtkinter.CTkFrame(output_header, fg_color="transparent")
        output_controls.grid(row=0, column=2, sticky="e")

        customtkinter.CTkButton(
            output_controls, text="📝Copy", width=65, height=30, command=self.copy_output
        ).pack(side="left", padx=2)

        customtkinter.CTkButton(
            output_controls, text="💾Save", width=65, height=30, command=self.save_to_file
        ).pack(side="left", padx=2)

        customtkinter.CTkButton(
            output_controls, text="❌Clear", width=65, height=30, command=self.clear_output,
            fg_color=("gray65", "gray35"), hover_color=("gray55", "gray45")
        ).pack(side="left", padx=2)

        # LARGER Output textbox
        output_container = customtkinter.CTkFrame(io_frame)
        output_container.grid(row=3, column=0, padx=8, pady=(0, 0), sticky="nsew")
        output_container.grid_rowconfigure(0, weight=1)
        output_container.grid_columnconfigure(0, weight=1)

        self.output_textbox = customtkinter.CTkTextbox(
            output_container, state="disabled", corner_radius=8, font=customtkinter.CTkFont(family="Consolas", size=12)
        )
        self.output_textbox.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        self.output_counter = customtkinter.CTkLabel(
            output_container, text="0 characters", font=customtkinter.CTkFont(size=10), text_color=("gray50", "gray60")
        )
        self.output_counter.grid(row=1, column=0, sticky="se", padx=8, pady=(0, 4))

    def _on_input_change(self, event=None):
        """Fast input change handling"""
        content = self.input_textbox.get("1.0", "end-1c")
        char_count = len(content)
        byte_count = len(content.encode('utf-8'))

        # Update counter efficiently
        counter_text = f"{char_count:,} chars" + (f" ({byte_count:,} bytes)" if byte_count != char_count else "")
        self.input_counter.configure(text=counter_text)

        # Reset step state
        self.reset_step_state()

    # Fast I/O operations with robust error handling
    def copy_output(self):
        """Fast copy with error handling"""
        try:
            content = self.output_textbox.get("1.0", "end-1c")
            if content:
                pyperclip.copy(content)
                self.app.update_status(f"Copied {len(content):,} characters", "success")
            else:
                self.app.show_toast("Warning", "Output is empty", "warning")
        except Exception as e:
            self.app.show_toast("Copy Error", f"Failed to copy: {str(e)}", "error")

    def open_from_file(self):
        """Fast file opening with encoding detection"""
        filepath = filedialog.askopenfilename(
            title="Open Text File",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            # Try multiple encodings quickly
            for encoding in ['utf-8', 'utf-16', 'ascii', 'latin-1']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise Exception("Could not decode file")

            # Check size and warn if large
            if len(content) > 5 * 1024 * 1024:  # 5MB
                if not messagebox.askyesno("Large File",
                                           f"File is {len(content) / (1024 * 1024):.1f}MB. Continue?"):
                    return

            self.input_textbox.delete("1.0", "end")
            self.input_textbox.insert("1.0", content)
            self.reset_step_state()

            filename = filepath.split('/')[-1] if '/' in filepath else filepath.split('\\')[-1]
            self.app.update_status(f"Loaded: {filename} ({len(content):,} chars)", "success")

        except Exception as e:
            self.app.show_toast("File Error", f"Failed to read file: {str(e)}", "error")

    def save_to_file(self):
        """Fast file saving"""
        content = self.output_textbox.get("1.0", "end-1c")
        if not content:
            self.app.show_toast("Warning", "Output is empty", "warning")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            filename = filepath.split('/')[-1] if '/' in filepath else filepath.split('\\')[-1]
            self.app.update_status(f"Saved: {filename} ({len(content):,} chars)", "success")

        except Exception as e:
            self.app.show_toast("Save Error", f"Failed to save: {str(e)}", "error")

    def paste_to_input(self):
        """Fast paste with size checking"""
        try:
            clipboard_content = pyperclip.paste()

            if len(clipboard_content) > 10 * 1024 * 1024:  # 10MB
                if not messagebox.askyesno("Large Clipboard",
                                           f"Clipboard has {len(clipboard_content):,} characters. Continue?"):
                    return

            self.input_textbox.delete("1.0", "end")
            self.input_textbox.insert("1.0", clipboard_content)
            self.reset_step_state()

            self.app.update_status(f"Pasted {len(clipboard_content):,} characters", "success")

        except Exception as e:
            self.app.show_toast("Paste Error", f"Failed to paste: {str(e)}", "error")

    def clear_input(self):
        """Fast input clearing"""
        self.input_textbox.delete("1.0", "end")
        self.input_counter.configure(text="0 characters")
        self.reset_step_state()

    def clear_output(self):
        """Fast output clearing"""
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.configure(state="disabled")
        self.output_counter.configure(text="0 characters")

    def clear_recipe(self):
        """Fast recipe clearing"""
        for widget in self.recipe_scrollable_frame.winfo_children():
            widget.destroy()
        self.recipe_placeholder = None
        self.after_idle(self.update_recipe_placeholder)
        self.reset_step_state()

    # Abstract methods for subclasses
    def execute_operation(self, operation_name, input_data, step_frame):
        """Execute operation - implemented by subclasses"""
        raise NotImplementedError("Subclass must implement execute_operation")

    def create_operations_sidebar(self):
        """Create sidebar - implemented by subclasses"""
        raise NotImplementedError("Subclass must implement create_operations_sidebar")

    def load_recipe(self):
        """Load recipe - implemented by subclasses"""
        raise NotImplementedError("Subclass must implement load_recipe")
