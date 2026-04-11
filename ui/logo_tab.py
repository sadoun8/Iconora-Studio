"""
Iconora Studio - Logo Designer Tab UI
Modernized with sidebar integration and icon support.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from pathlib import Path
from threading import Thread
import os, traceback
from PIL import Image
from core.logo_engine import LogoEngine
from core.ai_logo_engine import AILogoEngine
from i18n import tr, get_language

class LogoDesignerTab(ctk.CTkFrame):
    """Modernized UI for professional logo design"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.logo_engine = LogoEngine(600, 600)
        self.ai_engine = AILogoEngine()
        self.preview_image = None
        self.color1 = (99, 102, 241) # Modern Indigo
        self.color2 = (255, 255, 255)
        self.glow_color = (255, 255, 255)
        self.icon_path = None
        self._build_ui()

    def _build_ui(self):
        """Build the modernized logo designer UI"""
        # Main horizontal container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # Left Side: Controls
        self.controls_frame = ctk.CTkScrollableFrame(self.main_container, width=420)
        self.controls_frame.pack(side="left" if get_language() == "en" else "right", fill="both", padx=10, pady=10)

        ctk.CTkLabel(self.controls_frame, text=tr("logo_designer_title"), font=("Segoe UI Variable Display", 24, "bold")).pack(pady=20)

        # 1. Text Input
        ctk.CTkLabel(self.controls_frame, text=tr("lbl_logo_text"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=15)
        self.entry_text = ctk.CTkEntry(self.controls_frame, placeholder_text=tr("placeholder_company_name"), height=45)
        self.entry_text.insert(0, "Iconora")
        self.entry_text.pack(fill="x", padx=15, pady=(5, 15))
        self.entry_text.bind("<KeyRelease>", lambda e: self._preview())

        self.btn_ai_gen = ctk.CTkButton(
            self.controls_frame, text="✨ " + tr("logo_ai_generate"),
            command=self._generate_ai_logo,
            height=40, fg_color=("#8B5CF6", "#7C3AED"), hover_color=("#7C3AED", "#6D28D9"),
            font=("Segoe UI Variable Display", 13, "bold")
        )
        self.btn_ai_gen.pack(fill="x", padx=15, pady=(0, 15))

        # 2. Style & Layout
        style_group = ctk.CTkFrame(self.controls_frame)
        style_group.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(style_group, text=tr("logo_general_settings"), font=("Segoe UI Variable Text", 12, "bold")).pack(padx=10, pady=(10, 5), anchor="w")

        # Row 1: Style & Layout
        r1 = ctk.CTkFrame(style_group, fg_color="transparent")
        r1.pack(fill="x", padx=10, pady=5)

        self.style_var = ctk.StringVar(value="Minimal")
        self.style_menu = ctk.CTkOptionMenu(r1, values=LogoEngine.STYLES, variable=self.style_var, command=lambda v: self._preview())
        self.style_menu.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.layout_var = ctk.StringVar(value="side")
        self.layout_menu = ctk.CTkOptionMenu(r1, values=["side", "top", "bottom"], variable=self.layout_var, command=lambda v: self._preview())
        self.layout_menu.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Row 2: Template & Canvas
        r2 = ctk.CTkFrame(style_group, fg_color="transparent")
        r2.pack(fill="x", padx=10, pady=5)

        self.template_var = ctk.StringVar(value="None")
        self.template_menu = ctk.CTkOptionMenu(r2, values=["None"] + self.logo_engine.template_names(), variable=self.template_var, command=lambda v: self._preview())
        self.template_menu.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.canvas_size_var = ctk.StringVar(value="Square (800x800)")
        self.canvas_size_menu = ctk.CTkOptionMenu(r2, values=["Square (800x800)", "Landscape (1200x800)", "Wide Banner (1600x500)", "Cover / Social (1920x1080)", "Avatar (500x500)"], variable=self.canvas_size_var, command=lambda v: self._preview())
        self.canvas_size_menu.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.overlay_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(style_group, text=tr("logo_overlay"), variable=self.overlay_var, command=self._preview).pack(padx=10, pady=(5, 10), anchor="w")

        # 3. Typography & Positioning
        type_group = ctk.CTkFrame(self.controls_frame)
        type_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(type_group, text=tr("logo_typography_pos"), font=("Segoe UI Variable Text", 12, "bold")).pack(padx=10, pady=(10, 5), anchor="w")

        self.engine_fonts = self.logo_engine.available_fonts()
        self.font_var = ctk.StringVar(value=list(self.engine_fonts.keys())[0] if self.engine_fonts else "")
        ctk.CTkOptionMenu(type_group, values=list(self.engine_fonts.keys()), variable=self.font_var, command=lambda _: self._preview()).pack(fill="x", padx=10, pady=(0, 10))

        self._create_slider_control(type_group, tr("logo_font_size"), 20, 400, 80, "size_slider")
        self._create_slider_control(type_group, tr("logo_offset_x"), -800, 800, 0, "x_slider")
        self._create_slider_control(type_group, tr("logo_offset_y"), -800, 800, 0, "y_slider")

        # 4. Effects (Shadow & Glow)
        fx_group = ctk.CTkFrame(self.controls_frame)
        fx_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(fx_group, text=tr("logo_effects"), font=("Segoe UI Variable Text", 12, "bold")).pack(padx=10, pady=(10, 5), anchor="w")

        self._create_slider_control(fx_group, tr("logo_shadow_blur"), 0, 50, 5, "shadow_blur_slider")
        self._create_slider_control(fx_group, tr("logo_shadow_offset"), 0, 30, 4, "shadow_offset_slider")
        self._create_slider_control(fx_group, tr("logo_shadow_opacity"), 0, 255, 100, "shadow_opacity_slider")

        fx_row = ctk.CTkFrame(fx_group, fg_color="transparent")
        fx_row.pack(fill="x", padx=10, pady=(5, 10))

        self.btn_shadow_color = ctk.CTkButton(fx_row, text=tr("logo_shadow_color"), fg_color="black", text_color="white", command=self._pick_shadow_color, width=150)
        self.btn_shadow_color.pack(side="left", padx=(0, 5))
        self.shadow_color = (0, 0, 0)

        self.btn_glow_color = ctk.CTkButton(fx_row, text=tr("logo_glow_color"), fg_color=self._rgb_to_hex(self.glow_color), text_color="black", command=self._pick_glow_color, width=150)
        self.btn_glow_color.pack(side="left", padx=(5, 0))

        self._create_slider_control(fx_group, tr("logo_glow_radius"), 0, 50, 0, "glow_radius_slider")

        # 5. Colors
        color_group = ctk.CTkFrame(self.controls_frame)
        color_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(color_group, text="Colors", font=("Segoe UI Variable Text", 12, "bold")).pack(padx=10, pady=(10, 5), anchor="w")

        self.btn_color1 = ctk.CTkButton(color_group, text=tr("logo_primary_color"), fg_color=self._rgb_to_hex(self.color1), command=self._pick_color1)
        self.btn_color1.pack(fill="x", padx=10, pady=(5, 5))

        self.btn_color2 = ctk.CTkButton(color_group, text=tr("logo_secondary_color"), fg_color=self._rgb_to_hex(self.color2), text_color="black", command=self._pick_color2)
        self.btn_color2.pack(fill="x", padx=10, pady=(5, 15))

        # 6. Icon Integration & Customization
        icon_group = ctk.CTkFrame(self.controls_frame)
        icon_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(icon_group, text=tr("logo_icon_custom"), font=("Segoe UI Variable Text", 12, "bold")).pack(padx=10, pady=(10, 5), anchor="w")

        self.btn_load_icon = ctk.CTkButton(icon_group, text=tr("logo_load_icon"), command=self._load_icon)
        self.btn_load_icon.pack(fill="x", padx=10, pady=5)

        self.btn_rembg = ctk.CTkButton(
            icon_group,
            text=tr("btn_remove_bg"),
            command=self._remove_icon_bg,
            height=30,
            fg_color="transparent",
            border_width=1,
            text_color=("#3B82F6", "#6366F1"),
            font=("Segoe UI Variable Display", 11)
        )
        self.btn_rembg.pack(fill="x", padx=10, pady=2)

        self.lbl_icon_name = ctk.CTkLabel(icon_group, text=tr("logo_no_icon"), font=("Segoe UI Variable Text", 10), text_color="gray")
        self.lbl_icon_name.pack(pady=(0, 5))

        self._create_slider_control(icon_group, tr("logo_icon_scale"), 10, 400, 100, "icon_scale")
        self._create_slider_control(icon_group, tr("logo_icon_rotation"), 0, 360, 0, "icon_rotation")
        self._create_slider_control(icon_group, tr("logo_icon_opacity"), 0, 100, 100, "icon_opacity")
        self._create_slider_control(icon_group, tr("logo_icon_saturation"), 0, 200, 100, "icon_saturation")
        self._create_slider_control(icon_group, tr("logo_icon_offset_x"), -800, 800, 0, "icon_x_slider")
        self._create_slider_control(icon_group, tr("logo_icon_offset_y"), -800, 800, 0, "icon_y_slider")

        # 7. Action Button
        self.btn_save = ctk.CTkButton(
            self.controls_frame,
            text=tr("logo_generate_save"),
            command=self._save_logo,
            height=60,
            fg_color=("#3B82F6", "#6366F1"),
            hover_color=("#2563EB", "#4F46E5"),
            font=("Segoe UI Variable Display", 16, "bold"),
            corner_radius=15
        )
        self.btn_save.pack(fill="x", padx=15, pady=20)

        # Additional formats
        format_row = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        format_row.pack(fill="x", padx=15, pady=(0, 30))

        self.btn_save_webp = ctk.CTkButton(
            format_row, text="WebP", command=self._export_webp,
            height=32, fg_color="transparent", border_width=1, width=100
        )
        self.btn_save_webp.pack(side="left", padx=(0, 5), expand=True, fill="x")

        self.btn_save_pdf = ctk.CTkButton(
            format_row, text="PDF", command=self._export_pdf,
            height=32, fg_color="transparent", border_width=1, width=100
        )
        self.btn_save_pdf.pack(side="left", padx=(5, 5), expand=True, fill="x")

        self.btn_watermark = ctk.CTkButton(
            format_row, text=tr("btn_apply_watermark"), command=self._apply_watermark,
            height=32, fg_color="transparent", border_width=1, width=120
        )
        self.btn_watermark.pack(side="left", padx=(0, 0), expand=True, fill="x")

        # Right Side: Preview
        self.preview_frame = ctk.CTkFrame(self.main_container)
        self.preview_frame.pack(side="right" if get_language() == "en" else "left", fill="both", expand=True, padx=10, pady=10)

        # Add a checkerboard pattern for transparency preview
        self.canvas_preview = tk.Canvas(self.preview_frame, bg="gray20", highlightthickness=0)
        self.canvas_preview.pack(expand=True, fill="both", padx=20, pady=20)
        self.canvas_preview.bind("<Configure>", lambda e: self._draw_checkerboard())

        self.preview_label = ctk.CTkLabel(self.canvas_preview, text="", bg_color="transparent")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bind mouse events for dragging elements
        self.preview_label.bind("<Button-1>", self._on_drag_start)
        self.preview_label.bind("<B1-Motion>", self._on_drag_motion)
        self.preview_label.bind("<ButtonRelease-1>", self._on_drag_end)

        # Add a tooltip/help label for dragging
        drag_hint = "🖱️ Drag text/icon to move | اسحب النص/الأيقونة للتحريك"
        ctk.CTkLabel(self.preview_frame, text=drag_hint, font=("Segoe UI Variable Text", 10), text_color="gray").pack(pady=(0, 5))

        self.target_var = ctk.StringVar(value="Text")
        target_switch = ctk.CTkSegmentedButton(self.preview_frame, values=[tr("logo_target_text"), tr("logo_target_icon")],
                                               command=lambda v: self.target_var.set("Text" if v == tr("logo_target_text") else "Icon"))
        target_switch.set(tr("logo_target_text"))
        target_switch.pack(pady=(0, 10))

        self._preview()

    def _on_drag_start(self, event):
        """Record starting mouse position"""
        self._drag_data = {"x": event.x, "y": event.y}
        self.preview_label.configure(cursor="fleur")

    def _on_drag_motion(self, event):
        """Calculate delta and update sliders"""
        if not hasattr(self, "_drag_data") or not self._drag_data: return

        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]

        # Sensitivity factor to match preview scale
        sensitivity = 1.5

        # Get actual target based on variable or segmented button state
        target = self.target_var.get()

        if target == "Text":
            new_x = self.x_slider.get() + (dx * sensitivity)
            new_y = self.y_slider.get() + (dy * sensitivity)
            self.x_slider.set(max(-800, min(800, new_x)))
            self.y_slider.set(max(-800, min(800, new_y)))
        else:
            new_x = self.icon_x_slider.get() + (dx * sensitivity)
            new_y = self.icon_y_slider.get() + (dy * sensitivity)
            self.icon_x_slider.set(max(-800, min(800, new_x)))
            self.icon_y_slider.set(max(-800, min(800, new_y)))

        self._drag_data = {"x": event.x, "y": event.y}
        self._preview_delayed()

    def _preview_delayed(self):
        if hasattr(self, "_preview_timer") and self._preview_timer:
            self.after_cancel(self._preview_timer)
        self._preview_timer = self.after(50, self._preview)

    def _on_drag_end(self, event):
        """Clear drag data"""
        self._drag_data = None
        self.preview_label.configure(cursor="")

    def _create_slider_control(self, parent, label, from_val, to_val, start_val, attr_name):
        ctk.CTkLabel(parent, text=label, font=("Segoe UI Variable Text", 11)).pack(padx=10, pady=(5, 0), anchor="w")
        slider = ctk.CTkSlider(parent, from_=from_val, to=to_val, command=lambda v: self._preview_delayed())
        slider.set(start_val)
        slider.pack(fill="x", padx=10, pady=(2, 10))
        setattr(self, attr_name, slider)

    def _draw_checkerboard(self):
        self.canvas_preview.delete("checker")
        w = self.canvas_preview.winfo_width()
        h = self.canvas_preview.winfo_height()
        if w <= 1 or h <= 1: return
        size = 20
        for i in range(0, w, size):
            for j in range(0, h, size):
                if (i // size + j // size) % 2 == 0:
                    self.canvas_preview.create_rectangle(i, j, i+size, j+size, fill="gray25", outline="", tags="checker")
        self.preview_label.lift()

    def _pick_glow_color(self):
        color = colorchooser.askcolor(self._rgb_to_hex(self.glow_color))[0]
        if color:
            self.glow_color = tuple(int(c) for c in color)
            self.btn_glow_color.configure(fg_color=self._rgb_to_hex(self.glow_color))
            self._preview_delayed()

    def _pick_shadow_color(self):
        color = colorchooser.askcolor(self._rgb_to_hex(self.shadow_color))[0]
        if color:
            self.shadow_color = tuple(int(c) for c in color)
            self.btn_shadow_color.configure(fg_color=self._rgb_to_hex(self.shadow_color),
                                            text_color="white" if sum(self.shadow_color)/3 < 128 else "black")
            self._preview_delayed()

    def _pick_color1(self):
        color = colorchooser.askcolor(self._rgb_to_hex(self.color1))[0]
        if color:
            self.color1 = tuple(int(c) for c in color)
            self.btn_color1.configure(fg_color=self._rgb_to_hex(self.color1))
            self._preview_delayed()

    def _pick_color2(self):
        color = colorchooser.askcolor(self._rgb_to_hex(self.color2))[0]
        if color:
            self.color2 = tuple(int(c) for c in color)
            self.btn_color2.configure(fg_color=self._rgb_to_hex(self.color2))
            self._preview_delayed()

    def _generate_ai_logo(self):
        """Generates a logo using AI Engine and updates UI"""
        text = self.entry_text.get().strip() or "Iconora"
        style = self.style_var.get().lower() if hasattr(self, "style_var") else "modern"

        def _task():
            try:
                # Generate data
                return self.ai_engine.generate(
                    text,
                    style,
                    candidate_fonts=list(self.engine_fonts.keys()) if hasattr(self, "engine_fonts") else None
                )
            except Exception as e:
                return e

        def _on_done(result):
            self.btn_ai_gen.configure(state="normal", text="✨ " + tr("logo_ai_generate"))
            if isinstance(result, Exception):
                messagebox.showerror("Error", f"AI Generation failed: {result}")
                return

            data = result
            # 1. Typography
            if "font" in data: self.font_var.set(data["font"])

            # 2. Colors (convert hex to RGB for UI)
            if "colors" in data:
                c1_hex, c2_hex = data["colors"]
                def hex_to_rgb(h): return tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

                self.color1 = hex_to_rgb(c1_hex)
                self.color2 = hex_to_rgb(c2_hex)
                self.btn_color1.configure(fg_color=c1_hex)
                self.btn_color2.configure(fg_color=c2_hex)

            # 3. Layout mapping
            if "layout" in data:
                l = data["layout"]
                if l == "vertical": self.layout_var.set("top")
                elif l == "horizontal": self.layout_var.set("side")
                else: self.layout_var.set("side")

            # 4. Impactful AI Adjustments
            if style == "minimalist":
                self.size_slider.set(85)
                self.shadow_blur_slider.set(0)
                self.shadow_offset_slider.set(0)
                self.icon_scale.set(100)
            elif style == "modern":
                self.size_slider.set(125)
                self.shadow_blur_slider.set(20)
                self.shadow_offset_slider.set(8)
                self.icon_scale.set(120)
            elif style == "tech":
                self.size_slider.set(110)
                self.glow_radius_slider.set(25)
                self.color1 = (37, 99, 235)
                self.btn_color1.configure(fg_color="#2563EB")

            self.icon_path = None
            self.lbl_icon_name.configure(text=tr("logo_no_icon"))
            self._preview()
            messagebox.showinfo("✨ AI Logo Designer", f"AI Generated a professional '{style}' style for '{text}'!")

        self.btn_ai_gen.configure(state="disabled", text="⏳ AI Thinking...")

        # Access task_executor from MainWindow
        parent = self.master
        while parent and not hasattr(parent, 'task_executor'):
            parent = parent.master

        if parent and hasattr(parent, 'task_executor'):
            parent.task_executor.submit_task(_task, on_complete=lambda r: self.after(0, _on_done, r.result))
        else:
            Thread(target=lambda: self.after(0, _on_done, _task()), daemon=True).start()

    def _preview(self):
        text = self.entry_text.get()
        if not text: return

        try:
            import re
            m = re.search(r'\((\d+)x(\d+)\)', self.canvas_size_var.get())
            cw, ch = (int(m.group(1)), int(m.group(2))) if m else (800, 800)

            image = self.logo_engine.generate_logo(
                text=text,
                style=self.style_var.get(),
                color1=self.color1,
                color2=self.color2,
                font_size=int(self.size_slider.get()),
                font_path=self.engine_fonts.get(self.font_var.get()),
                layout=self.layout_var.get(),
                template_name=self.template_var.get() if self.template_var.get() != "None" else None,
                icon_size_factor=self.icon_scale.get() / 100.0,
                icon_rotation=self.icon_rotation.get(),
                icon_opacity=self.icon_opacity.get() / 100.0,
                icon_saturation=self.icon_saturation.get() / 100.0,
                text_overlay=self.overlay_var.get(),
                canvas_size=(cw, ch),
                text_offset_x=int(self.x_slider.get()),
                text_offset_y=int(self.y_slider.get()),
                icon_offset_x=int(self.icon_x_slider.get()),
                icon_offset_y=int(self.icon_y_slider.get()),
                shadow_color=self.shadow_color,
                shadow_opacity=int(self.shadow_opacity_slider.get()),
                shadow_blur=int(self.shadow_blur_slider.get()),
                shadow_offset=(int(self.shadow_offset_slider.get()), int(self.shadow_offset_slider.get())),
                glow_color=(*self.glow_color, 255) if self.glow_radius_slider.get() > 0 else None,
                glow_radius=int(self.glow_radius_slider.get())
            )

            # Show preview
            ratio = min(600/cw, 600/ch)
            pw, ph = max(1, int(cw * ratio)), max(1, int(ch * ratio))
            self.preview_image = ctk.CTkImage(light_image=image, dark_image=image, size=(pw, ph))
            self.preview_label.configure(image=self.preview_image)
        except Exception as e:
            print(f"Preview error: {e}")

    def _generate_logo_image(self):
        text = self.entry_text.get()
        if not text:
            messagebox.showwarning(tr("msg_warning"), tr("msg_enter_text"))
            return None

        import re
        m = re.search(r'\((\d+)x(\d+)\)', self.canvas_size_var.get())
        cw, ch = (int(m.group(1)), int(m.group(2))) if m else (800, 800)

        return self.logo_engine.generate_logo(
            text=text,
            style=self.style_var.get(),
            color1=self.color1,
            color2=self.color2,
            font_size=int(self.size_slider.get()),
            font_path=self.engine_fonts.get(self.font_var.get()),
            layout=self.layout_var.get(),
            template_name=self.template_var.get() if self.template_var.get() != "None" else None,
            icon_size_factor=self.icon_scale.get() / 100.0,
            icon_rotation=self.icon_rotation.get(),
            icon_opacity=self.icon_opacity.get() / 100.0,
            icon_saturation=self.icon_saturation.get() / 100.0,
            text_overlay=self.overlay_var.get(),
            canvas_size=(cw, ch),
            text_offset_x=int(self.x_slider.get()),
            text_offset_y=int(self.y_slider.get()),
            icon_offset_x=int(self.icon_x_slider.get()),
            icon_offset_y=int(self.icon_y_slider.get()),
            shadow_color=self.shadow_color,
            shadow_opacity=int(self.shadow_opacity_slider.get()),
            shadow_blur=int(self.shadow_blur_slider.get()),
            shadow_offset=(int(self.shadow_offset_slider.get()), int(self.shadow_offset_slider.get())),
            glow_color=(*self.glow_color, 255) if self.glow_radius_slider.get() > 0 else None,
            glow_radius=int(self.glow_radius_slider.get())
        )

    def _export_webp(self):
        image = self._generate_logo_image()
        if not image: return

        path = filedialog.asksaveasfilename(
            defaultextension=".webp",
            filetypes=[("WebP Image", "*.webp")],
            initialfile=f"{self.entry_text.get().lower()}_logo.webp"
        )
        if path:
            self.logo_engine.save_logo(image, path)
            messagebox.showinfo(tr("msg_success"), f"{tr('msg_save_success')}\n{path}")

    def _export_pdf(self):
        image = self._generate_logo_image()
        if not image: return

        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
            initialfile=f"{self.entry_text.get().lower()}_logo.pdf"
        )
        if path:
            self.logo_engine.save_logo(image, path)
            messagebox.showinfo(tr("msg_success"), f"{tr('msg_save_success')}\n{path}")

    def _save_logo(self):
        image = self._generate_logo_image()
        if not image: return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=f"{self.entry_text.get().lower()}_logo.png"
        )

        if path:
            try:
                self.logo_engine.save_logo(image, path)
                messagebox.showinfo(tr("msg_success"), f"{tr('msg_save_success')}\n{path}")
            except Exception as e:
                messagebox.showerror(tr("msg_error"), f"{tr('msg_save_error')}: {e}")

    def _apply_watermark(self):
        """Logic to apply current logo as a watermark on another image"""
        logo_img = self._generate_logo_image()
        if not logo_img: return

        base_path = filedialog.askopenfilename(
            title=tr("msg_select_base_image"),
            filetypes=[(tr("lbl_image_files"), "*.png *.jpg *.jpeg *.bmp"), (tr("lbl_all_files"), "*.*")]
        )
        if not base_path: return

        # Quick settings dialog (simplified for now, can be improved with a custom Toplevel)
        from tkinter import simpledialog

        # Define positions mapping
        pos_options = ["bottom-right", "bottom-left", "top-right", "top-left", "center"]

        # For simplicity, we use default settings for now or a basic choice
        try:
            # We'll use a standard result path
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png")],
                initialfile="watermarked_" + os.path.basename(base_path)
            )

            if save_path:
                # Apply with defaults: bottom-right, scale 0.2, opacity 0.7
                result = self.logo_engine.apply_watermark(base_path, logo_img)
                result.save(save_path, "PNG")
                messagebox.showinfo(tr("msg_success"), tr("msg_watermark_success"))
        except Exception as e:
            messagebox.showerror(tr("msg_error"), f"Watermarking failed: {e}")

    def get_project_data(self):
        """Returns the current state for project saving"""
        return {
            "type": "logo_designer",
            "text": self.entry_text.get().strip(),
            "style": self.style_var.get(),
            "layout": self.layout_var.get(),
            "template": self.template_var.get(),
            "canvas_size": self.canvas_size_var.get(),
            "overlay": self.overlay_var.get(),
            "font": self.font_var.get(),
            "font_size": int(self.size_slider.get()),
            "offset_x": int(self.x_slider.get()),
            "offset_y": int(self.y_slider.get()),
            "shadow_blur": int(self.shadow_blur_slider.get()),
            "shadow_offset": int(self.shadow_offset_slider.get()),
            "glow_radius": int(self.glow_radius_slider.get()),
            "color1": self._rgb_to_hex(self.color1),
            "color2": self._rgb_to_hex(self.color2),
            "glow_color": self._rgb_to_hex(self.glow_color),
            "icon_scale": self.icon_scale.get(),
            "icon_rotation": self.icon_rotation.get(),
            "icon_opacity": self.icon_opacity.get(),
            "icon_saturation": self.icon_saturation.get(),
            "icon_offset_x": int(self.icon_x_slider.get()),
            "icon_offset_y": int(self.icon_y_slider.get()),
            "icon_path": self.icon_path or ""
        }

    def load_project_data(self, data):
        """Load data from project"""
        if "text" in data: self.entry_text.delete(0, "end"); self.entry_text.insert(0, data["text"])
        if "style" in data: self.style_var.set(data["style"])
        if "layout" in data: self.layout_var.set(data["layout"])
        if "template" in data: self.template_var.set(data["template"])
        if "canvas_size" in data: self.canvas_size_var.set(data["canvas_size"])
        if "overlay" in data: self.overlay_var.set(data["overlay"])
        if "font" in data: self.font_var.set(data["font"])
        if "font_size" in data: self.size_slider.set(data["font_size"])
        if "offset_x" in data: self.x_slider.set(data["offset_x"])
        if "offset_y" in data: self.y_slider.set(data["offset_y"])
        if "shadow_blur" in data: self.shadow_blur_slider.set(data["shadow_blur"])
        if "shadow_offset" in data: self.shadow_offset_slider.set(data["shadow_offset"])
        if "glow_radius" in data: self.glow_radius_slider.set(data["glow_radius"])
        if "color1" in data and data["color1"].startswith("#"):
            c = data["color1"]
            self.color1 = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
            self.btn_color1.configure(fg_color=c)
        if "color2" in data and data["color2"].startswith("#"):
            c = data["color2"]
            self.color2 = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
            self.btn_color2.configure(fg_color=c)
        if "glow_color" in data and data["glow_color"].startswith("#"):
            c = data["glow_color"]
            self.glow_color = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
            self.btn_glow_color.configure(fg_color=c)
        if "icon_scale" in data: self.icon_scale.set(data["icon_scale"])
        if "icon_rotation" in data: self.icon_rotation.set(data["icon_rotation"])
        if "icon_opacity" in data: self.icon_opacity.set(data["icon_opacity"])
        if "icon_saturation" in data: self.icon_saturation.set(data["icon_saturation"])
        if "icon_offset_x" in data: self.icon_x_slider.set(data["icon_offset_x"])
        if "icon_offset_y" in data: self.icon_y_slider.set(data["icon_offset_y"])
        if "icon_path" in data and os.path.exists(data["icon_path"]):
            self._load_icon_from_path(data["icon_path"])
        self._preview()

    def _load_icon_from_path(self, path):
        if self.logo_engine.load_icon(path):
            self.icon_path = path
            self.lbl_icon_name.configure(text=os.path.basename(path))

    def _load_icon(self):
        path = filedialog.askopenfilename(
            title=tr("dlg_select_icon"),
            filetypes=[(tr("lbl_image_files"), "*.png *.jpg *.jpeg *.bmp"), (tr("lbl_all_files"), "*.*")]
        )
        if path:
            self._load_icon_from_path(path)

    def _remove_icon_bg(self):
        if not self.logo_engine.icon:
            messagebox.showwarning(tr("msg_warning"), tr("msg_select_icon_first"))
            return

        def task():
            try:
                self.btn_rembg.configure(state="disabled", text=tr("status_loading"))
                if self.logo_engine.remove_icon_bg():
                    self._preview()
                    messagebox.showinfo(tr("msg_success"), tr("msg_rembg_success"))
                else:
                    messagebox.showwarning(tr("msg_warning"), tr("msg_rembg_error"))
            except Exception as e:
                messagebox.showerror(tr("msg_error"), f"{tr('msg_rembg_error')}: {e}")
            finally:
                self.btn_rembg.configure(state="normal", text=tr("btn_remove_bg"))

        Thread(target=task, daemon=True).start()

    def _rgb_to_hex(self, rgba):
        return '#{:02x}{:02x}{:02x}'.format(*rgba[:3])
