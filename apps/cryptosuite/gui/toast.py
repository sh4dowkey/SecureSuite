import customtkinter


class ToastNotification(customtkinter.CTkFrame):
    """Enhanced toast notification with animations and better styling"""

    def __init__(self, master, title, message, toast_type="info"):
        super().__init__(master)

        # Enhanced styling based on message type
        self.styles = {
            "info": {
                "fg_color": ("#3498DB", "#2980B9"),
                "text_color": "white",
                "icon": "ℹ️",
                "border_color": ("#2980B9", "#1F6AA5")
            },
            "success": {
                "fg_color": ("#27AE60", "#229954"),
                "text_color": "white",
                "icon": "✅",
                "border_color": ("#229954", "#1E8449")
            },
            "warning": {
                "fg_color": ("#F39C12", "#E67E22"),
                "text_color": "white",
                "icon": "⚠️",
                "border_color": ("#E67E22", "#D35400")
            },
            "error": {
                "fg_color": ("#E74C3C", "#C0392B"),
                "text_color": "white",
                "icon": "❌",
                "border_color": ("#C0392B", "#A93226")
            }
        }

        self.style = self.styles.get(toast_type, self.styles["info"])
        self.toast_type = toast_type
        self.is_dismissing = False

        # Configure the frame
        self.configure(
            corner_radius=10,
            fg_color=self.style["fg_color"],
            border_width=2,
            border_color=self.style["border_color"]
        )

        # Set minimum width
        self.grid_columnconfigure(0, weight=1)
        self.configure(width=300, height=100)

        self._create_content(title, message)
        self._animate_in()

    def _create_content(self, title, message):
        """Create the toast content with enhanced layout"""
        # Main container
        content_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=12)
        content_frame.grid_columnconfigure(1, weight=1)

        # Icon
        icon_label = customtkinter.CTkLabel(
            content_frame,
            text=self.style["icon"],
            font=customtkinter.CTkFont(size=20),
            width=30
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 12), sticky="n")

        # Title
        title_label = customtkinter.CTkLabel(
            content_frame,
            text=title,
            text_color=self.style["text_color"],
            font=customtkinter.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="ew")

        # Message with word wrapping
        message_label = customtkinter.CTkLabel(
            content_frame,
            text=message,
            text_color=self.style["text_color"],
            font=customtkinter.CTkFont(size=12),
            anchor="w",
            justify="left",
            wraplength=400
        )
        message_label.grid(row=1, column=1, sticky="ew", pady=(2, 0))

        # Close button
        close_button = customtkinter.CTkButton(
            content_frame,
            text="×",
            width=25,
            height=25,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color=("white", "gray20"),
            text_color=self.style["text_color"],
            command=self.dismiss
        )
        close_button.grid(row=0, column=2, padx=(5, 0), sticky="ne")

        # Progress bar for auto-dismiss (optional)
        if self.toast_type in ["success", "info"]:
            self.progress_bar = customtkinter.CTkProgressBar(
                self,
                height=3,
                fg_color=("white", "gray30"),
                progress_color=self.style["text_color"]
            )
            self.progress_bar.grid(row=1, column=0, sticky="ew", padx=2, pady=(0, 2))
            self.progress_bar.set(1.0)

    def _animate_in(self):
        """Animate the toast sliding in from the right"""
        # Get the parent window dimensions
        parent = self.master
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Position off-screen initially
        self.place(x=parent_width, rely=0.98, anchor="se")

        # Animate sliding in
        self._slide_animation(start_x=parent_width, end_x=parent_width - 20, step=-15)

    def _slide_animation(self, start_x, end_x, step, current_step=0):
        """Smooth sliding animation"""
        if current_step <= 20:  # 20 steps for smooth animation
            # Calculate current position using easing
            progress = current_step / 20
            # Ease-out animation
            eased_progress = 1 - (1 - progress) ** 3
            current_x = start_x + (end_x - start_x) * eased_progress

            self.place(x=current_x, rely=0.98, anchor="se")

            # Schedule next frame
            self.after(16, lambda: self._slide_animation(start_x, end_x, step, current_step + 1))
        else:
            # Animation complete
            self.place(x=end_x, rely=0.98, anchor="se")

    def dismiss(self):
        """Dismiss the toast with animation"""
        if self.is_dismissing:
            return

        self.is_dismissing = True

        # Get current position
        current_x = self.winfo_x()
        parent_width = self.master.winfo_width()

        # Animate sliding out
        self._slide_out_animation(current_x, parent_width + 100)

    def _slide_out_animation(self, start_x, end_x, current_step=0):
        """Smooth slide-out animation"""
        if current_step <= 15 and self.winfo_exists():  # 15 steps for faster dismissal
            # Calculate current position with ease-in
            progress = current_step / 15
            eased_progress = progress ** 2
            current_x = start_x + (end_x - start_x) * eased_progress

            self.place(x=current_x, rely=0.98, anchor="se")

            # Schedule next frame
            self.after(16, lambda: self._slide_out_animation(start_x, end_x, current_step + 1))
        else:
            # Animation complete, destroy the toast
            if self.winfo_exists():
                self.destroy()

    def auto_dismiss(self, delay=4000):
        """Auto-dismiss the toast after specified delay with progress indication"""
        if self.toast_type in ["success", "info"] and hasattr(self, 'progress_bar'):
            # Animate progress bar
            self._animate_progress(delay)

        # Schedule dismissal
        self.after(delay, self.dismiss)

    def _animate_progress(self, total_time, current_time=0):
        """Animate the progress bar countdown"""
        if current_time >= total_time or not self.winfo_exists():
            return

        progress = 1 - (current_time / total_time)

        if hasattr(self, 'progress_bar'):
            self.progress_bar.set(progress)

        # Update every 50ms
        self.after(50, lambda: self._animate_progress(total_time, current_time + 50))

    def set_position(self, x=None, y=None, relx=None, rely=None, anchor="se"):
        """Set custom position for the toast"""
        if relx is not None and rely is not None:
            self.place(relx=relx, rely=rely, anchor=anchor)
        elif x is not None and y is not None:
            self.place(x=x, y=y, anchor=anchor)

    def update_content(self, title, message):
        """Update the toast content (useful for progress notifications)"""
        # Find and update the labels
        for child in self.winfo_children():
            if isinstance(child, customtkinter.CTkFrame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, customtkinter.CTkLabel):
                        if subchild.cget("font").cget("weight") == "bold":
                            subchild.configure(text=title)
                        else:
                            subchild.configure(text=message)
                        break
