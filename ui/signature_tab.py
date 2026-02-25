import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from pathlib import Path
from core.signature_engine import SignatureEngine


class SignatureTab(ctk.CTkFrame):
    """Professional Signature Tab - Phase 5 Enhanced."""

    def __init__(self, master):
        super().__init__(master)
        self.engine = SignatureEngine()
        self._current_image = None
        self._last_path = None
        self._build_ui()

    def _build_ui(self):
        """Build professional dual-panel layout."""
        # LEFT PANEL: Controls
        left_panel = ctk.CTkScrollableFrame(self, width=300)
        left_panel.pack(side="left", fill="y", padx=15, pady=15)
        left_panel.pack_propagate(False)

        # Title
        title = ctk.CTkLabel(left_panel, text="✍️ Signature Designer", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))

        # === Name Input ===
        ctk.CTkLabel(left_panel, text="📝 Name:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(left_panel, placeholder_text="Enter name", font=("Arial", 11))
        self.name_entry.pack(fill="x", pady=(5, 12))

        # === Title Input ===
        ctk.CTkLabel(left_panel, text="💼 Title (Optional):", font=("Arial", 12, "bold")).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(left_panel, placeholder_text="Job Title", font=("Arial", 11))
        self.title_entry.pack(fill="x", pady=(5, 12))

        # === Font Size ===
        ctk.CTkLabel(left_panel, text="🔤 Font Size:", font=("Arial", 12, "bold")).pack(anchor="w")
        size_frame = ctk.CTkFrame(left_panel)
        size_frame.pack(fill="x", pady=(5, 12))

        self.size_slider = ctk.CTkSlider(size_frame, from_=40, to=140, number_of_steps=20,
                                         command=lambda v: self.size_value.configure(text=str(int(float(v)))))
        self.size_slider.set(80)
        self.size_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.size_value = ctk.CTkLabel(size_frame, text="80", width=40)
        self.size_value.pack(side="right")

        # === Text Color ===
        ctk.CTkLabel(left_panel, text="🎨 Text Color:", font=("Arial", 12, "bold")).pack(anchor="w")
        color_frame = ctk.CTkFrame(left_panel)
        color_frame.pack(fill="x", pady=(5, 12))

        self.text_color = "#000000"
        self.text_color_btn = ctk.CTkButton(color_frame, text="  ", width=50, height=35,
                                           fg_color=self.text_color, command=self.choose_text_color)
        self.text_color_btn.pack(side="left", padx=(0, 10))

        color_label = ctk.CTkLabel(color_frame, text=self.text_color)
        color_label.pack(side="left")

        def update_color_label():
            color_label.configure(text=self.text_color)

        self.choose_text_color_original = self.choose_text_color
        def choose_text_color_wrapper():
            self.choose_text_color_original()
            update_color_label()
        self.choose_text_color = choose_text_color_wrapper

        # === Ink Effect ===
        ctk.CTkLabel(left_panel, text="✨ Ink Effect:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.ink_effect_var = ctk.BooleanVar(value=True)
        ink_check = ctk.CTkCheckBox(left_panel, text="Apply shadow & blur", variable=self.ink_effect_var)
        ink_check.pack(anchor="w", pady=(5, 12))

        # === Canvas Size ===
        ctk.CTkLabel(left_panel, text="📐 Canvas Size:", font=("Arial", 12, "bold")).pack(anchor="w")
        size_preset_frame = ctk.CTkFrame(left_panel)
        size_preset_frame.pack(fill="x", pady=(5, 12))

        self.canvas_width = 800
        self.canvas_height = 250

        preset_options = [("Standard (800x250)", (800, 250)),
                         ("Large (1000x300)", (1000, 300)),
                         ("Square (500x500)", (500, 500))]

        self.size_preset = ctk.CTkOptionMenu(size_preset_frame,
                                            values=[x[0] for x in preset_options],
                                            command=lambda v: self._set_canvas_size(preset_options, v),
                                            font=("Arial", 10))
        self.size_preset.set("Standard (800x250)")
        self.size_preset.pack(fill="x")

        # === Separator ===
        sep = ctk.CTkFrame(left_panel, height=2, fg_color="#444444")
        sep.pack(fill="x", pady=15)

        # === Action Buttons ===
        generate_btn = ctk.CTkButton(left_panel, text="✨ Create Signature",
                                    command=self.generate_signature,
                                    height=40, font=("Arial", 12, "bold"))
        generate_btn.pack(fill="x", pady=(0, 10))

        save_btn = ctk.CTkButton(left_panel, text="💾 Save As PNG",
                                command=self.save_signature,
                                height=35, font=("Arial", 11))
        save_btn.pack(fill="x", pady=(0, 15))

        # === Status ===
        self.status = ctk.CTkLabel(left_panel, text="Ready to generate", text_color="#888888", font=("Arial", 10))
        self.status.pack(fill="x", pady=(0, 10))

        # RIGHT PANEL: Preview
        right_panel = ctk.CTkFrame(self)
        right_panel.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        preview_title = ctk.CTkLabel(right_panel, text="👁️ Preview", font=("Arial", 14, "bold"))
        preview_title.pack(pady=(0, 10))

        # Preview canvas
        self.preview_canvas = ctk.CTkLabel(right_panel, width=600, height=300,
                                          fg_color="#1a1a1a", text="No preview yet")
        self.preview_canvas.pack(expand=True, fill="both", padx=10, pady=10)

    def _set_canvas_size(self, options, selection):
        """Set canvas size from preset."""
        for label, size in options:
            if label == selection:
                self.canvas_width, self.canvas_height = size
                break

    def choose_text_color_original(self):
        """Choose text color with dialog."""
        color = colorchooser.askcolor(initialcolor=self.text_color, title="Choose Text Color")
        if color and color[1]:
            self.text_color = color[1]
            self.text_color_btn.configure(fg_color=self.text_color)

    def choose_text_color(self):
        """Wrapper for color selection."""
        self.choose_text_color_original()

    def generate_signature(self):
        """Generate signature with threading."""
        name = self.name_entry.get().strip()
        title = self.title_entry.get().strip()
        font_size = int(self.size_slider.get())
        ink_effect = self.ink_effect_var.get()

        if not name:
            self.status.configure(text="❌ Name is required", text_color="#FF4444")
            return

        self.status.configure(text="⏳ Generating...", text_color="#FFA500")
        self.preview_canvas.configure(text="")

        # Run in thread to prevent UI freeze
        thread = threading.Thread(target=self._generate_thread,
                                 args=(name, title, font_size, ink_effect))
        thread.daemon = True
        thread.start()

    def _generate_thread(self, name, title, font_size, ink_effect):
        """Background signature generation."""
        try:
            # Get system font path
            font_path = self._get_font_path()

            if title:
                # Generate with title
                output_path = self.engine.generate_signature_with_title(
                    name=name,
                    title=title,
                    font_path=font_path,
                    font_size=font_size,
                    color=self.text_color,
                    ink_effect=ink_effect
                )
            else:
                # Generate name only
                output_path = self.engine.generate_signature(
                    text=name,
                    font_path=font_path,
                    font_size=font_size,
                    color=self.text_color,
                    ink_effect=ink_effect,
                    width=self.canvas_width,
                    height=self.canvas_height
                )

            self._last_path = output_path
            self._load_preview(output_path)
            self.status.configure(text="✅ Signature created", text_color="#00CC66")

        except Exception as e:
            self.status.configure(text=f"❌ Error: {e}", text_color="#FF4444")

    def _load_preview(self, image_path):
        """Load and display signature preview."""
        try:
            img = Image.open(image_path)
            img.thumbnail((600, 280), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.preview_canvas.configure(image=photo, text="")
            self.preview_canvas.image = photo  # Keep reference
        except Exception as e:
            self.status.configure(text=f"❌ Preview error: {e}", text_color="#FF4444")

    def _get_font_path(self):
        """Get system default font path."""
        try:
            from pathlib import Path
            import sys

            if sys.platform == "win32":
                font_path = Path("C:\\Windows\\Fonts\\arial.ttf")
            elif sys.platform == "darwin":
                font_path = Path("/Library/Fonts/Arial.ttf")
            else:
                font_path = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")

            if font_path.exists():
                return str(font_path)
            else:
                return None  # PIL will use default
        except:
            return None

    def save_signature(self):
        """Save signature with file dialog."""
        if not self._last_path:
            self.status.configure(text="❌ No signature to save", text_color="#FF4444")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
                initialdir=str(Path("exports/signatures"))
            )

            if file_path:
                img = Image.open(self._last_path)
                img.save(file_path, format="PNG")
                self.status.configure(text=f"✅ Saved to {Path(file_path).name}", text_color="#00CC66")

        except Exception as e:
            self.status.configure(text=f"❌ Save error: {e}", text_color="#FF4444")
