"""
Logo Designer Tab
تبويب تصميم الشعارات

Professional logo design interface with gradient, shadow, and multiple styles.
"""

import customtkinter as ctk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
from core.logo_engine import LogoEngine


class LogoTab(ctk.CTkFrame):
    """Professional logo designer with styles: Minimal, Luxury, 3D."""

    def __init__(self, parent):
        super().__init__(parent)

        self.engine = LogoEngine()
        self.selected_font = None
        self.color1 = "#ffffff"
        self.color2 = "#888888"
        self.style = "Minimal"
        self.last_logo_path = None

        self.create_widgets()

    def create_widgets(self):
        """Build the UI layout."""
        # Left panel - Controls
        controls = ctk.CTkFrame(self)
        controls.pack(side="left", fill="y", padx=12, pady=12, anchor="n")

        # Title
        title = ctk.CTkLabel(controls, text="Logo Designer", font=("Arial", 14, "bold"))
        title.pack(pady=(0, 12))

        # Text input
        ctk.CTkLabel(controls, text="Company Name:").pack(anchor="w", pady=(8, 0))
        self.entry = ctk.CTkEntry(controls, placeholder_text="Enter text...", width=280)
        self.entry.pack(pady=8)

        # Font selection
        ctk.CTkLabel(controls, text="Font:").pack(anchor="w", pady=(8, 0))
        self.font_btn = ctk.CTkButton(controls, text="Choose Font", command=self.choose_font)
        self.font_btn.pack(pady=6)

        # Font size
        ctk.CTkLabel(controls, text="Font Size:").pack(anchor="w", pady=(8, 0))
        self.font_size = ctk.CTkSlider(controls, from_=30, to=150, width=280)
        self.font_size.set(96)
        self.font_size.pack(pady=6)

        # Style selection
        ctk.CTkLabel(controls, text="Style:").pack(anchor="w", pady=(8, 0))
        self.style_menu = ctk.CTkOptionMenu(
            controls,
            values=["Minimal", "Luxury", "3D"],
            command=self.set_style,
            width=280
        )
        self.style_menu.set("Minimal")
        self.style_menu.pack(pady=6)

        # Color 1
        ctk.CTkLabel(controls, text="Primary Color:").pack(anchor="w", pady=(8, 0))
        self.color1_btn = ctk.CTkButton(
            controls, text="   ", width=280, height=28, command=self.choose_color1
        )
        self.color1_btn.configure(fg_color=self.color1)
        self.color1_btn.pack(pady=6)

        # Color 2
        ctk.CTkLabel(controls, text="Secondary Color:").pack(anchor="w", pady=(8, 0))
        self.color2_btn = ctk.CTkButton(
            controls, text="   ", width=280, height=28, command=self.choose_color2
        )
        self.color2_btn.configure(fg_color=self.color2)
        self.color2_btn.pack(pady=6)

        # Effects
        ctk.CTkLabel(controls, text="Effects:").pack(anchor="w", pady=(12, 0))
        self.shadow_var = ctk.BooleanVar(value=True)
        shadow_check = ctk.CTkCheckBox(controls, text="Add Shadow", variable=self.shadow_var)
        shadow_check.pack(anchor="w", pady=4)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(controls, width=280)
        self.progress_bar.pack(pady=(12, 0))
        self.progress_bar.set(0)

        # Generate button
        self.generate_btn = ctk.CTkButton(
            controls, text="✨ Generate Logo", command=self.generate_logo
        )
        self.generate_btn.pack(pady=12)

        # Save button
        self.save_btn = ctk.CTkButton(
            controls, text="💾 Save Logo", command=self.save_logo, state="disabled"
        )
        self.save_btn.pack(pady=6)

        # Right panel - Preview
        preview_frame = ctk.CTkFrame(self)
        preview_frame.pack(side="right", fill="both", expand=True, padx=12, pady=12)

        preview_title = ctk.CTkLabel(preview_frame, text="Preview", font=("Arial", 12, "bold"))
        preview_title.pack(anchor="w", pady=(0, 8))

        self.canvas = ctk.CTkLabel(
            preview_frame, width=600, height=300, fg_color="#222222", text="No preview yet"
        )
        self.canvas.pack(fill="both", expand=True)

    def choose_font(self):
        """Select a font file from the system."""
        fonts = self.engine.get_system_fonts()
        if not fonts:
            messagebox.showerror("Error", "No fonts found")
            return

        path = filedialog.askopenfilename(
            initialdir="C:/Windows/Fonts",
            filetypes=[("Font Files", "*.ttf;*.otf")]
        )
        if path:
            self.selected_font = path
            self.font_btn.configure(text=f"✓ Font selected")

    def choose_color1(self):
        """Choose primary (text) color."""
        color = colorchooser.askcolor(color=self.color1)
        if color[1]:
            self.color1 = color[1]
            self.color1_btn.configure(fg_color=self.color1)

    def choose_color2(self):
        """Choose secondary color."""
        color = colorchooser.askcolor(color=self.color2)
        if color[1]:
            self.color2 = color[1]
            self.color2_btn.configure(fg_color=self.color2)

    def set_style(self, choice):
        """Set the logo style."""
        self.style = choice

    def generate_logo(self):
        """Generate the logo with current settings."""
        text = self.entry.get().strip()
        if not text:
            messagebox.showerror("Error", "Enter company name")
            return

        if not self.selected_font:
            messagebox.showerror("Error", "Select a font first")
            return

        self.progress_bar.set(0.3)
        self.generate_btn.configure(state="disabled")

        try:
            font_size = int(self.font_size.get())

            output = self.engine.generate_logo(
                text=text,
                font_path=self.selected_font,
                font_size=font_size,
                style=self.style,
                color1=self.color1,
                color2=self.color2,
                shadow=self.shadow_var.get()
            )

            self.progress_bar.set(0.7)
            self._show_preview(output)
            self.progress_bar.set(1.0)
            self.last_logo_path = output
            self.save_btn.configure(state="normal")
            messagebox.showinfo("Success", f"Logo saved:\n{output}")

        except Exception as e:
            messagebox.showerror("Error", f"Generation failed: {e}")
        finally:
            self.progress_bar.set(0)
            self.generate_btn.configure(state="normal")

    def _show_preview(self, logo_path):
        """Display the generated logo in preview canvas."""
        try:
            img = Image.open(logo_path)
            img.thumbnail((600, 300), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.configure(image=self.tk_image, text="")
        except Exception as e:
            messagebox.showerror("Preview Error", str(e))

    def save_logo(self):
        """Save the generated logo to a custom path."""
        if not self.last_logo_path:
            messagebox.showerror("Error", "Generate a logo first")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if path:
            try:
                img = Image.open(self.last_logo_path)
                img.save(path)
                messagebox.showinfo("Success", f"Saved to:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {e}")
