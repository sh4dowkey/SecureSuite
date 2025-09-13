import customtkinter
import tkinter
from tkinter import messagebox
import webbrowser
from .gui.encrypt_frame import EncryptFrame
from .gui.decrypt_frame import DecryptFrame
from .gui.toast import ToastNotification
import subprocess
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("CryptoSuite")
        self.geometry("1200x700")
        self.minsize(1100, 600)

        # usage
        self.iconbitmap(resource_path("apps/assets/logo.ico"))

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        self.active_toast = None

        # --- Create Top Menu Bar ---
        self._create_menu_bar()

        # --- Main Layout ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = customtkinter.CTkFrame(self, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.app_name_label = customtkinter.CTkLabel(self.header_frame, text="CryptoSuite 🔐",
                                                     font=customtkinter.CTkFont(family="Helvetica", size=24,
                                                                                weight="bold"))
        self.app_name_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.main_body_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_body_frame.grid(row=1, column=0, sticky="nsew")
        self.main_body_frame.grid_columnconfigure(1, weight=1)
        self.main_body_frame.grid_rowconfigure(0, weight=1)

        # --- Navigation Rail (Left Side) ---
        self.navigation_rail = customtkinter.CTkFrame(self.main_body_frame, width=150, corner_radius=0)
        self.navigation_rail.grid(row=0, column=0, sticky="nsw")
        self.navigation_rail.grid_rowconfigure(4, weight=1)

        self.encrypt_button = customtkinter.CTkButton(self.navigation_rail, text="🔒  Encrypt",
                                                      command=lambda: self.select_frame("encrypt"), corner_radius=0,
                                                      height=50, font=("", 16), anchor="w", border_spacing=10)
        self.encrypt_button.grid(row=0, column=0, sticky="ew", pady=(5, 0))

        self.decrypt_button = customtkinter.CTkButton(self.navigation_rail, text="🔓  Decrypt",
                                                      command=lambda: self.select_frame("decrypt"), corner_radius=0,
                                                      height=50, font=("", 16), anchor="w", border_spacing=10)
        self.decrypt_button.grid(row=1, column=0, sticky="ew")

        # --- Separator ---
        separator = customtkinter.CTkFrame(self.navigation_rail, height=1, fg_color="gray25")
        separator.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.steganography_button = customtkinter.CTkButton(self.navigation_rail, text="SecretInImage 🕵️️",
                                                            command=self.launch_steganography, corner_radius=0,
                                                            height=50, font=("", 16), anchor="w",
                                                            border_spacing=10, fg_color="transparent")
        self.steganography_button.grid(row=3, column=0, sticky="ew")

        # --- Frame Container for Encrypt/Decrypt views ---
        self.frame_container = customtkinter.CTkFrame(self.main_body_frame, fg_color="transparent")
        self.frame_container.grid(row=0, column=1, sticky="nsew")

        self.status_bar = customtkinter.CTkLabel(self, text="Ready", anchor="w", font=("", 12))
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 5))

        # --- Create and manage the frames ---
        self.frames = {
            "encrypt": EncryptFrame(master=self.frame_container, app=self, status_bar=self.status_bar),
            "decrypt": DecryptFrame(master=self.frame_container, app=self, status_bar=self.status_bar)
        }

        self.select_frame("encrypt")

    def _get_active_frame(self):
        """Helper to get the currently visible frame."""
        for frame in self.frames.values():
            if frame.winfo_viewable():
                return frame
        return None

    def select_frame(self, name):
        """Shows the selected frame and hides the others."""
        self.encrypt_button.configure(
            fg_color="transparent" if name != "encrypt" else customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        self.decrypt_button.configure(
            fg_color="transparent" if name != "decrypt" else customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def _create_menu_bar(self):
        menu_bar = tkinter.Menu(self)

        menu_font = ("Segoe UI", 19)

        # --- File Menu ---
        file_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        file_menu.add_command(label="Open Text File...", command=lambda: self._get_active_frame().open_from_file())
        file_menu.add_command(label="Save Output As...", command=lambda: self._get_active_frame().save_to_file())
        file_menu.add_separator()
        file_menu.add_command(label="Load Recipe...", command=lambda: self._get_active_frame().load_recipe())
        file_menu.add_command(label="Save Recipe...", command=lambda: self._get_active_frame().save_recipe())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # --- Edit Menu ---
        edit_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        edit_menu.add_command(label="Copy Output", command=lambda: self._get_active_frame().copy_output())
        edit_menu.add_command(label="Paste Input", command=lambda: self._get_active_frame().paste_to_input())
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=lambda: self._get_active_frame().clear_recipe())
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # --- Tools Menu ---
        tools_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        tools_menu.add_command(label="Hide Secret in Image...", command=self.launch_steganography)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        # --- Help Menu ---
        help_menu = tkinter.Menu(menu_bar, tearoff=0, font=menu_font)
        help_menu.add_command(label="About CryptoSuite", command=self._show_about_dialog)
        help_menu.add_command(label="View Documentation", command=self._open_documentation)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def _show_about_dialog(self):
        """Displays a custom, modern 'About' window with an improved layout."""
        about_window = customtkinter.CTkToplevel(self)
        about_window.title("About CryptoSuite")
        about_window.geometry("500x380")
        about_window.transient(self)
        about_window.resizable(False, False)
        about_window.grab_set()

        main_frame = customtkinter.CTkFrame(about_window, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        title_label = customtkinter.CTkLabel(main_frame, text="CryptoSuite v1.0",
                                             font=customtkinter.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        desc_label = customtkinter.CTkLabel(main_frame, text="A modern toolkit for cryptographic operations.",
                                            wraplength=400, justify="center")
        desc_label.grid(row=1, column=0, padx=20, pady=5)

        ack_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        ack_frame.grid(row=2, column=0, padx=20, pady=15)

        ack_title = customtkinter.CTkLabel(ack_frame, text="Acknowledgements",
                                           font=customtkinter.CTkFont(size=14, weight="bold"))
        ack_title.pack()

        ack_text = customtkinter.CTkLabel(ack_frame,
                                          text="This application is proudly built using Python,\nCustomTkinter, and other open-source libraries.",
                                          text_color="gray60", justify="center")
        ack_text.pack(pady=(0, 10))

        footer_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.grid(row=4, column=0, padx=20, pady=20, sticky="s")
        footer_frame.grid_columnconfigure(0, weight=1)

        separator = customtkinter.CTkFrame(footer_frame, height=1, fg_color="gray25")
        separator.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        copyright_label = customtkinter.CTkLabel(footer_frame,
                                                 text="Copyright © 2025 sh4dowkey. Released under the MIT License.",
                                                 font=customtkinter.CTkFont(size=12), text_color="gray60")
        copyright_label.grid(row=1, column=0)

        ok_button = customtkinter.CTkButton(footer_frame, text="OK", width=100, command=about_window.destroy)
        ok_button.grid(row=2, column=0, pady=(15, 0))

    def _open_documentation(self):
        """Opens the project's GitHub page in a web browser."""
        webbrowser.open_new_tab("https://github.com/sh4dowkey/SecureSuite")

    def launch_steganography(self):
        """Launches the Steganography app in a new window."""
        try:
            module_path = "apps.steganography.main"
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            subprocess.Popen([sys.executable, "-m", module_path], cwd=project_root)
            self.status_bar.configure(text="Launched Steganography app...")
        except Exception as e:
            self.show_toast("Error", f"Could not launch Steganography app: {e}", "error")

    def show_toast(self, title, message, toast_type="info"):
        if self.active_toast is not None and self.active_toast.winfo_exists():
            self.active_toast.destroy()
        toast = ToastNotification(self, title, message, toast_type)
        toast.place(relx=0.99, rely=0.98, anchor="se")
        toast.lift()
        self.active_toast = toast
        self.after(4000, toast.destroy)
