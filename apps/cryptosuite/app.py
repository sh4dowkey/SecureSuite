import os
import sys
import threading
import tkinter
import webbrowser

import customtkinter
from PIL import Image

from .gui.decrypt_frame import DecryptFrame
from .gui.encrypt_frame import EncryptFrame
from .gui.toast import ToastNotification


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)


class Tooltip:
    """
    Creates a more robust tooltip (hover text) for a given customtkinter widget.
    It uses a delay to prevent flickering and ensures proper hiding.
    """

    def __init__(self, widget, text, delay_ms=500):
        self.widget = widget
        self.text = text
        self.delay = delay_ms
        self.tooltip_window = None
        self.show_id = None

        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.schedule_hide)
        self.widget.bind("<Button-1>", self.schedule_hide)  # Hide on click

    def schedule_show(self, event=None):
        """Schedules the tooltip to appear after a delay."""
        # Cancel any pending hide events
        self.cancel_show()
        self.show_id = self.widget.after(self.delay, self.show_tooltip)

    def schedule_hide(self, event=None):
        """Schedules the tooltip to disappear."""
        self.cancel_show()
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def cancel_show(self):
        """Cancels a scheduled tooltip appearance."""
        if self.show_id:
            self.widget.after_cancel(self.show_id)
            self.show_id = None

    def show_tooltip(self):
        """Create and show the tooltip window."""
        if self.tooltip_window or not self.text:
            return

        # Calculate position
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2) - 14

        # Create tooltip window
        self.tooltip_window = customtkinter.CTkToplevel(self.widget)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.attributes("-topmost", True)

        # Add label with the text
        label = customtkinter.CTkLabel(
            self.tooltip_window, text=self.text, font=customtkinter.CTkFont(size=12),
            corner_radius=6, fg_color=("gray75", "gray25"), padx=8, pady=4
        )
        label.pack()


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Enhanced window properties
        self.title("SecureSuite - Professional Cryptography Toolkit")
        self.geometry("1400x800")
        self.minsize(1350, 700)

        # Set icon with better error handling
        self._set_application_icon()

        # Enhanced theme setup
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        # State management
        self.active_toast = None
        self.is_processing = False

        # Create UI components
        self._setup_ui()

        # Keyboard shortcuts
        self._setup_keyboard_shortcuts()

    def _set_application_icon(self):
        """Set application icon with proper fallback"""
        try:
            if "win" in sys.platform:
                self.iconbitmap(resource_path("assets/logo.ico"))
            else:
                logo_image = tkinter.PhotoImage(file=resource_path("assets/logo.png"))
                self.iconphoto(True, logo_image)
        except Exception as e:
            print(f"Warning: Could not set application icon: {e}")

    def _setup_ui(self):
        """Set up the main UI components"""
        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create enhanced header
        self._create_enhanced_header()

        # Create main body with improved layout
        self._create_main_body()

        # Create enhanced status bar
        self._create_enhanced_status_bar()

        # Create frames after status bar is created
        self._create_frames()

        # Setup keyboard shortcuts AFTER everything is created
        self._setup_keyboard_shortcuts()

        # Create menu bar
        self._create_menu_bar()

    def _create_frames(self):
        """Create the main application frames"""
        self.frames = {
            "encrypt": EncryptFrame(master=self.frame_container, app=self, status_bar=self.status_bar),
            "decrypt": DecryptFrame(master=self.frame_container, app=self, status_bar=self.status_bar)
        }

        self.select_frame("encrypt")

    def _create_enhanced_header(self):
        """Create an enhanced header with better styling"""
        self.header_frame = customtkinter.CTkFrame(
            self,
            height=70,
            corner_radius=0,
            fg_color=("gray85", "gray20")
        )
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(2, weight=1)

        # Logo with improved styling
        try:
            logo_pil_image = Image.open(resource_path("assets/header_image.png"))
            logo_image = customtkinter.CTkImage(light_image=logo_pil_image, size=(40, 40))

            logo_label = customtkinter.CTkLabel(self.header_frame, image=logo_image, text="")
            logo_label.grid(row=0, column=0, padx=(25, 15), pady=15, sticky="w")
        except Exception:
            # Fallback emoji logo
            logo_label = customtkinter.CTkLabel(
                self.header_frame,
                text="🛡️",
                font=customtkinter.CTkFont(size=30)
            )
            logo_label.grid(row=0, column=0, padx=(25, 15), pady=15, sticky="w")

        # Enhanced title
        self.app_name_label = customtkinter.CTkLabel(
            self.header_frame,
            text="SecureSuite",
            font=customtkinter.CTkFont(family="Helvetica", size=26, weight="bold"),
            text_color=("gray10", "gray90")
        )
        self.app_name_label.grid(row=0, column=1, padx=0, pady=15, sticky="w")

        # Version label
        version_label = customtkinter.CTkLabel(
            self.header_frame,
            text="v2.0 Pro",
            font=customtkinter.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        version_label.grid(row=0, column=3, padx=(0, 25), pady=15, sticky="e")

    def _create_main_body(self):
        """Create the main body with improved layout"""
        self.main_body_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_body_frame.grid(row=1, column=0, sticky="nsew")

        self.main_body_frame.grid_columnconfigure(0, weight=0)

        self.main_body_frame.grid_columnconfigure(1, weight=1)
        self.main_body_frame.grid_rowconfigure(0, weight=1)

        # Enhanced navigation rail
        self._create_enhanced_navigation()

        # Frame container for main content (just create the container, not the frames yet)
        self.frame_container = customtkinter.CTkFrame(self.main_body_frame, fg_color="transparent")
        self.frame_container.grid(row=0, column=1, sticky="nsew")

    def _create_enhanced_navigation(self):
        """
        Fixed-width navigation rail (emoji icons only).
        - Locks the rail width with grid_propagate(False) and main_body_frame column minsize.
        - Forces small button sizes and a small font so emojis do not inflate the request size.
        """

        RAIL_WIDTH = 80  # final rail width in px (adjust 72..100 as you prefer)
        BTN_SIZE = 54  # pixel size for each button (must be <= RAIL_WIDTH - padX*2)
        ICON_FONT_SIZE = 16  # emoji font size (very important on Windows DPI)

        # Outer rail frame - fixed width
        self.navigation_rail = customtkinter.CTkFrame(
            self.main_body_frame,
            width=RAIL_WIDTH,
            corner_radius=0,
            fg_color=("gray90", "gray15")
        )
        self.navigation_rail.grid(row=0, column=0, sticky="ns")
        # Honor the fixed width and don't let children resize it
        self.navigation_rail.grid_propagate(False)

        # Also lock the parent column to the same minimum so layout doesn't expand it
        try:
            self.main_body_frame.grid_columnconfigure(0, minsize=RAIL_WIDTH)
        except Exception:
            # if main_body_frame doesn't exist yet, ignore
            pass

        # Inner container (use pack inside to avoid grid-wide stretching)
        inner = customtkinter.CTkFrame(self.navigation_rail, width=RAIL_WIDTH, fg_color="transparent")
        inner.pack(fill="both", expand=True)
        inner.pack_propagate(False)  # ensure inner keeps the rail width

        # Button style - explicit pixel sizes + small emoji font
        button_style = {
            "width": BTN_SIZE,
            "height": BTN_SIZE,
            "corner_radius": 8,
            "font": customtkinter.CTkFont(size=ICON_FONT_SIZE),
            "anchor": "c",
            "border_spacing": 0
        }

        # Encrypt button
        self.encrypt_button = customtkinter.CTkButton(
            inner,
            text="🔒",
            command=lambda: self.select_frame("encrypt"),
            **button_style
        )
        self.encrypt_button.pack(pady=(16, 6))  # vertical spacing

        # Decrypt button
        self.decrypt_button = customtkinter.CTkButton(
            inner,
            text="🔓",
            command=lambda: self.select_frame("decrypt"),
            **button_style
        )
        self.decrypt_button.pack(pady=6)

        # separator
        separator = customtkinter.CTkFrame(inner, height=2, fg_color=("gray70", "gray30"))
        separator.pack(fill="x", padx=8, pady=12)

        # Tools label
        tools_label = customtkinter.CTkLabel(
            inner,
            text="TOOLS",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color=("gray50", "gray60")
        )
        tools_label.pack(anchor="w", padx=10, pady=(4, 6))

        # Steganography button (same size)
        self.steganography_button = customtkinter.CTkButton(
            inner,
            text="🕵",
            command=self.launch_steganography,
            fg_color="transparent",
            hover_color=("gray80", "gray25"),
            **{k: v for k, v in button_style.items() if k != "corner_radius"}
        )
        self.steganography_button.pack(pady=6)

        # Spacer so HELP sits at the bottom
        spacer = customtkinter.CTkFrame(inner, fg_color="transparent")
        spacer.pack(expand=True, fill="both")

        # Help label & shortcuts button
        help_label = customtkinter.CTkLabel(
            inner,
            text=" HELP",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color=("gray50", "gray60")
        )
        help_label.pack(anchor="w", padx=10, pady=(8, 6))

        # separator
        separator = customtkinter.CTkFrame(inner, height=2, fg_color=("gray70", "gray30"))
        separator.pack(fill="x", padx=8, pady=5)

        shortcuts_button = customtkinter.CTkButton(
            inner,
            text="⌨",
            command=self._show_shortcuts_dialog,
            fg_color="transparent",
            hover_color=("gray80", "gray25"),
            corner_radius=8,
            height=40,
            width=40,
            font=customtkinter.CTkFont(size=12),
            anchor="c",
            border_spacing=0
        )
        shortcuts_button.pack(pady=(12, 14))

        Tooltip(shortcuts_button, "View keyboard shortcuts")
        Tooltip(self.encrypt_button, "Encrypt data")
        Tooltip(self.decrypt_button, "Decrypt data")
        Tooltip(self.steganography_button, "Steganography tools")

    def _create_enhanced_status_bar(self):
        """Create enhanced status bar with progress indicator"""
        status_frame = customtkinter.CTkFrame(self, fg_color=("gray95", "gray10"), corner_radius=0)
        status_frame.grid(row=2, column=0, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        # Status indicator dot
        self.status_dot = customtkinter.CTkLabel(
            status_frame,
            text="●",
            font=customtkinter.CTkFont(size=16),
            text_color="green",
            width=20
        )
        self.status_dot.grid(row=0, column=0, padx=(15, 5), pady=8)

        # Status text
        self.status_bar = customtkinter.CTkLabel(
            status_frame,
            text="Ready - CryptoSuite Professional",
            anchor="w",
            font=customtkinter.CTkFont(size=12)
        )
        self.status_bar.grid(row=0, column=1, sticky="ew", padx=5, pady=8)

        # Mini progress bar (hidden by default)
        self.status_progress = customtkinter.CTkProgressBar(
            status_frame,
            width=100,
            height=8,
            mode="indeterminate"
        )

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for better UX"""
        # Bind keyboard shortcuts
        self.bind("<Control-o>", lambda e: self._get_active_frame().open_from_file())
        self.bind("<Control-s>", lambda e: self._get_active_frame().save_to_file())
        self.bind("<Control-l>", lambda e: self._get_active_frame().load_recipe())
        self.bind("<Control-r>", lambda e: self._get_active_frame().save_recipe())
        self.bind("<Control-c>", lambda e: self._get_active_frame().copy_output())
        self.bind("<Control-v>", lambda e: self._get_active_frame().paste_to_input())
        self.bind("<F5>", lambda e: self._get_active_frame().bake_recipe())
        self.bind("<F1>", lambda e: self._show_shortcuts_dialog())

        # Tab switching
        self.bind("<Control-1>", lambda e: self.select_frame("encrypt"))
        self.bind("<Control-2>", lambda e: self.select_frame("decrypt"))

    def _show_shortcuts_dialog(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_window = customtkinter.CTkToplevel(self)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("500x600")
        shortcuts_window.transient(self)
        shortcuts_window.resizable(False, False)
        shortcuts_window.grab_set()

        # Center the window
        shortcuts_window.update_idletasks()
        x = (shortcuts_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (shortcuts_window.winfo_screenheight() // 2) - (600 // 2)
        shortcuts_window.geometry(f"+{x}+{y}")

        main_frame = customtkinter.CTkFrame(shortcuts_window, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = customtkinter.CTkLabel(
            main_frame,
            text="⌨️ Keyboard Shortcuts",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        shortcuts_text = """
General:
Ctrl + O         Open file
Ctrl + S         Save output
Ctrl + L         Load recipe
Ctrl + R         Save recipe
Ctrl + C         Copy output
Ctrl + V         Paste to input
F5               Execute recipe
F1               Show shortcuts

Navigation:
Ctrl + 1         Switch to Encrypt
Ctrl + 2         Switch to Decrypt

Processing:
Enter            Execute current step
Shift + Enter    Execute full recipe
Escape           Clear all fields
        """.strip()

        shortcuts_label = customtkinter.CTkLabel(
            main_frame,
            text=shortcuts_text,
            font=customtkinter.CTkFont(family="Courier", size=12),
            justify="left",
            anchor="w"
        )
        shortcuts_label.pack(fill="both", expand=True, padx=20)

        close_button = customtkinter.CTkButton(
            main_frame,
            text="Close",
            command=shortcuts_window.destroy,
            width=100
        )
        close_button.pack(pady=20)

    def _get_active_frame(self):
        """Helper to get the currently visible frame."""
        for frame in self.frames.values():
            if frame.winfo_viewable():
                return frame
        return None

    def select_frame(self, name):
        """Shows the selected frame with smooth transition effect."""
        # Update button states with enhanced styling
        for btn_name, button in [("encrypt", self.encrypt_button), ("decrypt", self.decrypt_button)]:
            if btn_name == name:
                button.configure(
                    fg_color=["#3B8ED0", "#1F6AA5"],
                    hover_color=["#36719F", "#144870"]
                )
            else:
                button.configure(
                    fg_color="transparent",
                    hover_color=("gray80", "gray25")
                )

        # Show selected frame
        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

        # Update status
        mode_name = "Encryption" if name == "encrypt" else "Decryption"
        self.update_status(f"Switched to {mode_name} mode", "info")

    def update_status(self, message, status_type="info", show_progress=False):
        """Enhanced status update with visual indicators"""
        # Update status dot color
        colors = {
            "info": ("blue", "#1F6AA5"),
            "success": ("green", "#2D8B2D"),
            "warning": ("orange", "#FF8C00"),
            "error": ("red", "#DC143C"),
            "processing": ("yellow", "#FFD700")
        }

        color = colors.get(status_type, colors["info"])
        self.status_dot.configure(text_color=color)
        self.status_bar.configure(text=message)

        # Handle progress indicator
        if show_progress:
            self.status_progress.grid(row=0, column=2, padx=(5, 15), pady=8, sticky="e")
            self.status_progress.start()
        else:
            self.status_progress.stop()
            self.status_progress.grid_remove()

        # Auto-reset status after delay (except for processing)
        if status_type != "processing":
            self.after(5000, lambda: self._reset_status())

    def _reset_status(self):
        """Reset status to default state"""
        self.status_dot.configure(text_color="green")
        self.status_bar.configure(text="Ready - CryptoSuite Professional")
        self.status_progress.stop()
        self.status_progress.grid_remove()

    def set_processing_state(self, is_processing):
        """Set the global processing state"""
        self.is_processing = is_processing
        if is_processing:
            self.update_status("Processing operation...", "processing", show_progress=True)
        else:
            self.update_status("Operation completed", "success")

    def _create_menu_bar(self):
        """Enhanced menu bar"""
        menu_bar = tkinter.Menu(self)
        menu_font = ("Segoe UI", 18)

        # File Menu
        file_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        file_menu.add_command(
            label="Open Text File...                    Ctrl+O",
            command=lambda: self._get_active_frame().open_from_file()
        )
        file_menu.add_command(
            label="Save Output As...                    Ctrl+S",
            command=lambda: self._get_active_frame().save_to_file()
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Load Recipe...                       Ctrl+L",
            command=lambda: self._get_active_frame().load_recipe()
        )
        file_menu.add_command(
            label="Save Recipe...                       Ctrl+R",
            command=lambda: self._get_active_frame().save_recipe()
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        edit_menu.add_command(
            label="Copy Output                          Ctrl+C",
            command=lambda: self._get_active_frame().copy_output()
        )
        edit_menu.add_command(
            label="Paste Input                          Ctrl+V",
            command=lambda: self._get_active_frame().paste_to_input()
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Clear All                            Esc",
            command=lambda: self._get_active_frame().clear_recipe()
        )
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Tools Menu
        tools_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        tools_menu.add_command(
            label="Steganography Suite...",
            command=self.launch_steganography
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Keyboard Shortcuts                   F1",
            command=self._show_shortcuts_dialog
        )
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        # Help Menu
        help_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        help_menu.add_command(label="About SecureSuite", command=self._show_about_dialog)
        help_menu.add_command(label="View Documentation", command=self._open_documentation)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def _show_about_dialog(self):
        """Enhanced about dialog"""
        about_window = customtkinter.CTkToplevel(self)
        about_window.title("About CryptoSuite Pro")
        about_window.geometry("600x600")
        about_window.transient(self)
        about_window.resizable(False, False)
        about_window.grab_set()

        # Center the window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (about_window.winfo_screenheight() // 2) - (450 // 2)
        about_window.geometry(f"+{x}+{y}")

        main_frame = customtkinter.CTkFrame(about_window, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        # App icon
        try:
            logo_pil = Image.open(resource_path("assets/header_image.png"))
            logo_img = customtkinter.CTkImage(logo_pil, size=(64, 64))
            logo_label = customtkinter.CTkLabel(main_frame, image=logo_img, text="")
            logo_label.grid(row=0, column=0, pady=(30, 10))
        except Exception:
            logo_label = customtkinter.CTkLabel(
                main_frame,
                text="🛡️",
                font=customtkinter.CTkFont(size=48)
            )
            logo_label.grid(row=0, column=0, pady=(30, 10))

        title_label = customtkinter.CTkLabel(
            main_frame,
            text="CryptoSuite Pro v2.0",
            font=customtkinter.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        desc_label = customtkinter.CTkLabel(
            main_frame,
            text="Professional Cryptography Toolkit\n\nA modern, recipe-based approach to encryption,\ndecryption, encoding, and secure data processing.",
            font=customtkinter.CTkFont(size=14),
            justify="center"
        )
        desc_label.grid(row=2, column=0, padx=20, pady=15)

        features_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        features_frame.grid(row=3, column=0, padx=40, pady=20, sticky="ew")

        features_title = customtkinter.CTkLabel(
            features_frame,
            text="Key Features:",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        features_title.pack(anchor="w")

        features_text = """• Recipe-based cryptographic workflows
        
• 50+ encryption and encoding algorithms

• Advanced steganography capabilities

• Professional UI with keyboard shortcuts

• Batch processing for large datasets

• Export/import functionality"""

        features_label = customtkinter.CTkLabel(
            features_frame,
            text=features_text,
            font=customtkinter.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        features_label.pack(anchor="w", pady=(5, 0))

        copyright_label = customtkinter.CTkLabel(
            main_frame,
            text="Copyright © 2025 sh4dowkey\nReleased under the MIT License",
            font=customtkinter.CTkFont(size=12),
            text_color=("gray50", "gray60"),
            justify="center"
        )
        copyright_label.grid(row=4, column=0, pady=20)

        ok_button = customtkinter.CTkButton(
            main_frame,
            text="Close",
            width=120,
            command=about_window.destroy
        )
        ok_button.grid(row=5, column=0, pady=(0, 30))

    def _open_documentation(self):
        """Opens the project's GitHub page in a web browser."""
        webbrowser.open_new_tab("https://github.com/sh4dowkey/SecureSuite")

    def launch_steganography(self):
        """Enhanced steganography launcher with better error handling"""

        def launch_in_thread():
            try:
                # Use the proper module path for the steganography app
                import subprocess
                import sys
                import os

                # Get the project root directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(os.path.dirname(current_dir))

                # Launch steganography module
                module_path = "apps.steganography.main"
                subprocess.Popen([
                    sys.executable, "-m", module_path
                ], cwd=project_root)

                self.after(0, lambda: self.update_status("Steganography Suite launched successfully", "success"))

            except Exception as e:
                error_msg = f"Could not launch Steganography Suite: {str(e)}"
                self.after(0, lambda: self.show_toast("Launch Error", error_msg, "error"))

        # Launch in separate thread to prevent UI blocking
        threading.Thread(target=launch_in_thread, daemon=True).start()
        self.update_status("Launching Steganography Suite...", "info")

    def show_toast(self, title, message, toast_type="info"):
        """Enhanced toast notification system"""
        if self.active_toast is not None and self.active_toast.winfo_exists():
            self.active_toast.destroy()

        toast = ToastNotification(self, title, message, toast_type)
        toast.place(relx=0.99, rely=0.98, anchor="se")
        toast.lift()
        toast.tkraise()

        self.active_toast = toast

        # Auto-dismiss after appropriate time based on message length
        dismiss_time = max(3000, min(8000, len(message) * 50))
        self.after(dismiss_time, lambda: self._dismiss_toast(toast))

    def _dismiss_toast(self, toast):
        """Safely dismiss toast notification"""
        try:
            if toast.winfo_exists():
                toast.destroy()
        except Exception:
            pass
