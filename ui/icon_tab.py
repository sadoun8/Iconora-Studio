"""
Iconora Studio - Icon Converter Tab UI
Modernized with sidebar integration and reliable size selection.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from threading import Thread
import os
from PIL import Image
from core.icon_converter import IconConverter
from core.signature_engine import SignatureEngine
from i18n import tr, get_language
from config import EXPORT_SUBDIRS

class IconConverterTab(ctk.CTkFrame):
    """Modernized UI for icon conversion"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.converter = None
        self.input_path = None
        self.preview_image = None
        self.engine_fonts = SignatureEngine.available_fonts()
        self.bg_color = (255, 255, 255, 0)
        self.border_color = (255, 255, 255, 255)
        
        # Position offsets for text
        self.text_offset_x = 0
        self.text_offset_y = 0
        
        self._preview_timer = None
        self._build_ui()
        
        # Performance enhancements
        self._enable_performance_enhancements()

    def _enable_performance_enhancements(self):
        """تفعيل التحسينات - Enable performance features"""
        from core.enhancement_patches import patch_icon_tab_convert, patch_icon_tab_export_pngs
        patch_icon_tab_convert(self)
        patch_icon_tab_export_pngs(self)

    def _build_ui(self):
        """Build the modernized icon converter UI"""
        # Main horizontal container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        is_en = get_language() == "en"

        # Left Side: Controls
        self.controls_frame = ctk.CTkScrollableFrame(self.main_container, width=350)
        self.controls_frame.pack(side="left" if is_en else "right", fill="both", padx=10, pady=10)

        ctk.CTkLabel(self.controls_frame, text="📦 Icon Studio Pro", font=("Segoe UI Variable Display", 24, "bold")).pack(pady=20)

        # 1. File Selection
        self.selection_group = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.selection_group.pack(fill="x", padx=15, pady=10)

        self.btn_select = ctk.CTkButton(
            self.selection_group,
            text=tr("btn_select_image"),
            command=self._select_image,
            height=50,
            font=("Segoe UI Variable Display", 14, "bold"),
            corner_radius=15
        )
        self.btn_select.pack(fill="x", pady=5)

        self.btn_rembg = ctk.CTkButton(
            self.selection_group,
            text=tr("btn_remove_bg"),
            command=self._remove_bg,
            height=35,
            fg_color="transparent",
            border_width=1,
            text_color=("#3B82F6", "#6366F1"),
            font=("Segoe UI Variable Display", 12)
        )
        self.btn_rembg.pack(fill="x", pady=2)

        self.lbl_path = ctk.CTkLabel(self.selection_group, text=tr("no_image_selected"), font=("Segoe UI Variable Text", 10), text_color="gray")
        self.lbl_path.pack()

        # 1.5 AI Smart Suggestions
        ai_group = ctk.CTkFrame(self.controls_frame, fg_color=("#8B5CF6", "#7C3AED"), corner_radius=12)
        ai_group.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(ai_group, text="✨ AI Smart Styles", font=("Segoe UI Variable Text", 12, "bold"), text_color="white").pack(padx=15, pady=(15, 5), anchor="w")
        
        ai_btns = ctk.CTkFrame(ai_group, fg_color="transparent")
        ai_btns.pack(fill="x", padx=10, pady=(0, 15))
        
        styles = [("Modern Blue", "modern_blue"), ("Soft Glass", "glass"), ("Dark Neon", "neon")]
        for label, sid in styles:
            ctk.CTkButton(
                ai_btns, text=label, width=100, height=32, corner_radius=8,
                fg_color="white", text_color="#7C3AED", font=("Segoe UI Variable Text", 11),
                command=lambda s=sid: self._apply_ai_icon_style(s)
            ).pack(side="left", padx=5, expand=True)

        # 2. Mask & Shape
        shape_group = ctk.CTkFrame(self.controls_frame)
        shape_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(shape_group, text=tr("lbl_mask_shape"), font=("Segoe UI Variable Text", 12, "bold")).pack(pady=(10, 5), padx=10, anchor="w" if is_en else "e")

        self.mask_var = ctk.StringVar(value="None")
        self.mask_menu = ctk.CTkOptionMenu(shape_group, values=["None", tr("opt_circle"), tr("opt_squircle"), tr("opt_rounded")], variable=self.mask_var, command=lambda _: self._preview_delayed())
        self.mask_menu.pack(fill="x", padx=10, pady=5)

        self._create_slider_control(shape_group, tr("lbl_corner_radius"), 0, 50, 20, "corner_slider_attr")
        self._create_slider_control(shape_group, tr("lbl_internal_padding"), 0, 40, 0, "padding_slider_attr")

        # 3. Colors & Border
        color_group = ctk.CTkFrame(self.controls_frame)
        color_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(color_group, text=tr("lbl_bg_border"), font=("Segoe UI Variable Text", 12, "bold")).pack(pady=(10, 5), padx=10, anchor="w" if is_en else "e")

        self.btn_bg = ctk.CTkButton(color_group, text=tr("lbl_bg_color"), command=self._pick_bg, fg_color="gray30")
        self.btn_bg.pack(fill="x", padx=10, pady=5)
        
        self._create_slider_control(color_group, tr("lbl_border_width"), 0, 20, 0, "border_slider_attr")
        self.btn_border_col = ctk.CTkButton(color_group, text=tr("lbl_border_color"), command=self._pick_border_col, fg_color="white", text_color="black")
        self.btn_border_col.pack(fill="x", padx=10, pady=(5, 10))

        # 3.5 Image Adjustments
        adjust_group = ctk.CTkFrame(self.controls_frame)
        adjust_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(adjust_group, text=tr("lbl_image_adjust"), font=("Segoe UI Variable Text", 12, "bold")).pack(pady=(10, 5), padx=10, anchor="w" if is_en else "e")

        self._create_slider_control(adjust_group, tr("lbl_brightness"), 0, 200, 100, "bright_slider")
        self._create_slider_control(adjust_group, tr("lbl_contrast"), 0, 200, 100, "contrast_slider")
        self._create_slider_control(adjust_group, tr("lbl_saturation"), 0, 200, 100, "sat_slider")

        flip_frame = ctk.CTkFrame(adjust_group, fg_color="transparent")
        flip_frame.pack(fill="x", padx=10, pady=5)
        
        self.var_flip_h = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(flip_frame, text=tr("lbl_flip_h"), variable=self.var_flip_h, command=self._preview_delayed, font=("Segoe UI Variable Text", 10)).pack(side="left", padx=5)
        
        self.var_flip_v = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(flip_frame, text=tr("lbl_flip_v"), variable=self.var_flip_v, command=self._preview_delayed, font=("Segoe UI Variable Text", 10)).pack(side="left", padx=5)

        # 4. Text Overlay
        text_group = ctk.CTkFrame(self.controls_frame)
        text_group.pack(fill="x", padx=15, pady=10)

        self.var_text_enable = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(text_group, text=tr("opt_enable_text"), variable=self.var_text_enable, font=("Segoe UI Variable Text", 12, "bold"), command=self._preview_delayed).pack(pady=(10, 5), padx=10, anchor="w" if is_en else "e")

        self.entry_text = ctk.CTkEntry(text_group, placeholder_text=tr("lbl_text"))
        self.entry_text.pack(fill="x", padx=10, pady=5)
        self.entry_text.bind("<KeyRelease>", lambda _: self._preview_delayed())

        self.font_var = ctk.StringVar(value=list(self.engine_fonts.keys())[0] if self.engine_fonts else "")
        ctk.CTkOptionMenu(text_group, values=list(self.engine_fonts.keys()), variable=self.font_var, command=lambda _: self._preview_delayed()).pack(fill="x", padx=10, pady=5)

        self._create_slider_control(text_group, tr("lbl_font_size"), 10, 200, 40, "font_size_slider")

        self.pos_var = ctk.StringVar(value="bottom")
        ctk.CTkOptionMenu(text_group, values=[tr("pos_top"), tr("pos_center"), tr("pos_bottom")], variable=self.pos_var, command=lambda _: self._preview_delayed()).pack(fill="x", padx=10, pady=5)

        self.style_var = ctk.StringVar(value="Normal")
        ctk.CTkOptionMenu(text_group, values=["Normal", "Upward (صاعد)", "Slanted (مائل)"], variable=self.style_var, command=lambda _: self._preview_delayed()).pack(fill="x", padx=10, pady=(5, 15))

        # 5. Export Settings
        export_group = ctk.CTkFrame(self.controls_frame)
        export_group.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(export_group, text=tr("lbl_export_settings"), font=("Segoe UI Variable Text", 12, "bold")).pack(pady=(10, 5), padx=10, anchor="w" if is_en else "e")

        sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
        grid_frame = ctk.CTkFrame(export_group, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)
        self.size_vars = {}
        for i, s in enumerate(sizes):
            var = tk.BooleanVar(value=s >= 32)
            self.size_vars[s] = var
            chk = ctk.CTkCheckBox(grid_frame, text=f"{s}px", variable=var, font=("Segoe UI Variable Text", 10))
            chk.grid(row=i//3, column=i%3, padx=5, pady=3, sticky="w")

        self._create_slider_control(export_group, tr("lbl_ico_quality"), 50, 100, 95, "quality_slider_attr")

        # 6. Action Button
        self.btn_convert = ctk.CTkButton(
            self.controls_frame,
            text=tr("btn_save_ico"),
            command=self._convert,
            height=60,
            fg_color=("#3B82F6", "#6366F1"),
            hover_color=("#2563EB", "#4F46E5"),
            font=("Segoe UI Variable Display", 16, "bold"),
            corner_radius=15
        )
        self.btn_convert.pack(fill="x", padx=15, pady=20)

        self.btn_export_png = ctk.CTkButton(
            self.controls_frame,
            text=tr("btn_save_png"),
            command=self._export_pngs,
            height=40,
            fg_color="transparent",
            border_width=1,
            font=("Segoe UI Variable Display", 13)
        )
        self.btn_export_png.pack(fill="x", padx=15, pady=(0, 10))

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
        self.btn_save_pdf.pack(side="left", padx=(5, 0), expand=True, fill="x")

        # Right Side: Preview
        self.preview_frame = ctk.CTkFrame(self.main_container)
        self.preview_frame.pack(side="right" if is_en else "left", fill="both", expand=True, padx=10, pady=10)

        self.canvas_preview = tk.Canvas(self.preview_frame, bg="gray20", highlightthickness=0)
        self.canvas_preview.pack(expand=True, fill="both", padx=20, pady=20)
        self.canvas_preview.bind("<Configure>", lambda e: self._draw_checkerboard())

        self.preview_label = ctk.CTkLabel(self.canvas_preview, text=tr("msg_no_preview"), font=("Segoe UI Variable Display", 14))
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bind mouse events for dragging text
        self.preview_label.bind("<Button-1>", self._on_drag_start)
        self.preview_label.bind("<B1-Motion>", self._on_drag_motion)
        self.preview_label.bind("<ButtonRelease-1>", self._on_drag_end)
        
        # Add a tooltip/help label for dragging
        drag_hint = "🖱️ Drag text to move | اسحب النص للتحريك"
        ctk.CTkLabel(self.preview_frame, text=drag_hint, font=("Segoe UI Variable Text", 10), text_color="gray").pack(pady=(0, 10))

        # Hidden sliders for offsets (to be used by engine and project loading)
        self.text_x_slider = ctk.CTkSlider(self, from_=-800, to=800)
        self.text_x_slider.set(0)
        self.text_y_slider = ctk.CTkSlider(self, from_=-800, to=800)
        self.text_y_slider.set(0)

    def _on_drag_start(self, event):
        """Record starting mouse position"""
        if not self.var_text_enable.get(): return
        self._drag_data = {"x": event.x, "y": event.y}
        self.preview_label.configure(cursor="fleur")

    def _on_drag_motion(self, event):
        """Calculate delta and update offsets"""
        if not self.var_text_enable.get(): return
        if not hasattr(self, "_drag_data") or not self._drag_data: return
        
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        
        # Sensitivity factor to match preview scale
        sensitivity = 1.5 
        
        new_x = self.text_x_slider.get() + (dx * sensitivity)
        new_y = self.text_y_slider.get() + (dy * sensitivity)
        
        self.text_x_slider.set(max(-800, min(800, new_x)))
        self.text_y_slider.set(max(-800, min(800, new_y)))
        
        self._drag_data = {"x": event.x, "y": event.y}
        self._preview_delayed()

    def _on_drag_end(self, event):
        """Clear drag data"""
        self._drag_data = None
        self.preview_label.configure(cursor="")

    def _create_slider_control(self, parent, label, from_val, to_val, start_val, attr_name):
        lbl = ctk.CTkLabel(parent, text=label, font=("Segoe UI Variable Text", 11))
        lbl.pack(padx=10, pady=(5, 0), anchor="w")
        slider = ctk.CTkSlider(parent, from_=from_val, to=to_val, command=lambda v, l=lbl, n=label: self._on_slider_change(v, l, n))
        slider.set(start_val)
        slider.pack(fill="x", padx=10, pady=(2, 10))
        setattr(self, attr_name, slider)
        setattr(self, f"{attr_name}_lbl", lbl) # Store label reference
        setattr(self, f"{attr_name}_title", label) # Store original title
        return slider

    def _on_slider_change(self, val, label_widget, name):
        if label_widget:
            label_widget.configure(text=f"{name}: {int(val)}%")
        self._preview_delayed()

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

    def _pick_bg(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Pick Background Color")[0]
        if color:
            self.bg_color = (*[int(c) for c in color], 255)
            self.btn_bg.configure(fg_color=self._rgb_to_hex(self.bg_color))
            self._preview_delayed()
        else:
            self.bg_color = (255, 255, 255, 0) # Transparent
            self.btn_bg.configure(fg_color="gray30")
            self._preview_delayed()

    def _pick_border_col(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Pick Border Color")[0]
        if color:
            self.border_color = (*[int(c) for c in color], 255)
            self.btn_border_col.configure(fg_color=self._rgb_to_hex(self.border_color))
            self._preview_delayed()

    def _rgb_to_hex(self, rgba):
        return '#{:02x}{:02x}{:02x}'.format(*rgba[:3])

    def _select_image(self):
        path = filedialog.askopenfilename(
            title=tr("dlg_select_image"),
            filetypes=[(tr("lbl_image_files"), "*.png *.jpg *.jpeg *.bmp"), (tr("lbl_all_files"), "*.*")]
        )
        if path:
            self.input_path = path
            self.lbl_path.configure(text=os.path.basename(path))
            self.converter = IconConverter(path)
            self._update_preview(path)

    def _remove_bg(self):
        if not self.converter:
            messagebox.showwarning("Warning", tr("msg_select_image_first"))
            return
        
        def task():
            try:
                self.btn_rembg.configure(state="disabled", text=tr("status_loading"))
                self.converter.remove_background()
                self._update_preview()
                messagebox.showinfo(tr("msg_success"), tr("msg_rembg_success"))
            except Exception as e:
                messagebox.showerror(tr("msg_error"), f"{tr('msg_rembg_error')}: {e}")
            finally:
                self.btn_rembg.configure(state="normal", text=tr("btn_remove_bg"))

        Thread(target=task, daemon=True).start()

    def _update_preview(self, path=None):
        if not self.converter: return
        self.converter.reset_image()
        
        # Performance optimization: Resize working image to a manageable size for preview
        # if it's too large (e.g. > 1024px)
        w, h = self.converter.working_image.size
        if max(w, h) > 1024:
            ratio = 1024 / max(w, h)
            self.converter.working_image = self.converter.working_image.resize(
                (int(w * ratio), int(h * ratio)), Image.Resampling.BILINEAR)

        # Apply all transformations
        self._reapply_logic()

        try:
            img = self.converter.get_image_copy()
            max_size = (600, 600)
            img.thumbnail(max_size, Image.Resampling.BILINEAR) # Use faster resampling for live preview
            self.preview_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=self.preview_image, text="")
        except Exception as e:
            self.preview_label.configure(text=f"Preview Error: {e}")

    def _reapply_logic(self):
        """Internal helper to apply all current settings to self.converter.working_image"""
        if not self.converter: return

        # Apply adjustments
        if hasattr(self, "bright_slider") or hasattr(self, "contrast_slider") or hasattr(self, "sat_slider"):
            br = self.bright_slider.get() / 100.0 if hasattr(self, "bright_slider") else 1.0
            ct = self.contrast_slider.get() / 100.0 if hasattr(self, "contrast_slider") else 1.0
            sa = self.sat_slider.get() / 100.0 if hasattr(self, "sat_slider") else 1.0
            self.converter.adjust_image(br, ct, sa)

        if hasattr(self, "var_flip_h") and (self.var_flip_h.get() or self.var_flip_v.get()):
            self.converter.flip_image(self.var_flip_h.get(), self.var_flip_v.get())

        # Transformations
        if hasattr(self, "padding_slider_attr") and self.padding_slider_attr.get() > 0:
            self.converter.add_padding(self.padding_slider_attr.get())
        
        if hasattr(self, "bg_color") and self.bg_color[3] > 0:
            self.converter.add_background(self.bg_color)

        if hasattr(self, "mask_var"):
            m = self.mask_var.get()
            if m == tr("opt_circle"):
                self.converter.apply_circle_mask()
            elif m == tr("opt_squircle"):
                self.converter.apply_squircle_mask()
            elif m == tr("opt_rounded") and hasattr(self, "corner_slider_attr"):
                self.converter.apply_rounded_corners(self.corner_slider_attr.get())

        if hasattr(self, "border_slider_attr") and self.border_slider_attr.get() > 0:
            self.converter.add_border(self.border_slider_attr.get(), self.border_color)

        if self.var_text_enable.get():
            font_path = self.engine_fonts.get(self.font_var.get())
            self.converter.add_text_overlay(
                text=self.entry_text.get().strip(),
                font_path=font_path,
                position=self.pos_var.get(),
                style=self.style_var.get(),
                offset_x=int(self.text_x_slider.get()),
                offset_y=int(self.text_y_slider.get())
            )

    def _preview_delayed(self):
        if getattr(self, "_preview_timer", None):
            self.after_cancel(self._preview_timer)
        self._preview_timer = self.after(300, self._update_preview)

    def _apply_ai_icon_style(self, style_id):
        """Applies an AI-recommended style preset to the icon converter"""
        if style_id == "modern_blue":
            self.bg_color = (37, 99, 235, 255)
            self.mask_var.set(tr("opt_squircle"))
            self.corner_slider_attr.set(25)
            self.padding_slider_attr.set(10)
            self.btn_bg.configure(fg_color="#2563EB")
            self.bright_slider.set(105)
            self.contrast_slider.set(110)
            self.sat_slider.set(115)
        elif style_id == "glass":
            self.bg_color = (255, 255, 255, 80)
            self.mask_var.set(tr("opt_rounded"))
            self.corner_slider_attr.set(40)
            self.padding_slider_attr.set(15)
            self.border_slider_attr.set(3)
            self.btn_bg.configure(fg_color="gray80")
            self.btn_border_col.configure(fg_color="white")
            self.bright_slider.set(120)
            self.contrast_slider.set(90)
            self.sat_slider.set(110)
        elif style_id == "neon":
            self.bg_color = (15, 23, 42, 255)
            self.border_color = (96, 165, 250, 255)
            self.border_slider_attr.set(6)
            self.btn_bg.configure(fg_color="#0F172A")
            self.btn_border_col.configure(fg_color="#60A5FA")
            self.sat_slider.set(160)
            self.contrast_slider.set(140)
            self.bright_slider.set(110)
            
        # Manually trigger label updates for sliders
        for attr in ["corner_slider_attr", "padding_slider_attr", "border_slider_attr", 
                     "bright_slider", "contrast_slider", "sat_slider"]:
            if hasattr(self, attr):
                slider = getattr(self, attr)
                lbl = getattr(self, f"{attr}_lbl", None)
                title = getattr(self, f"{attr}_title", attr)
                self._on_slider_change(slider.get(), lbl, title)

        self._preview_delayed()
        messagebox.showinfo("✨ AI Smart Styles", f"AI Style '{style_id}' applied successfully!")

    def _convert(self):
        if not self.input_path:
            messagebox.showwarning("Warning", tr("msg_select_image_first"))
            return

        selected_sizes = [s for s, v in self.size_vars.items() if v.get()]
        if not selected_sizes:
            messagebox.showwarning("Warning", tr("msg_select_size"))
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".ico",
            filetypes=[("Icon", "*.ico")],
            initialfile=os.path.splitext(os.path.basename(self.input_path))[0] + ".ico"
        )

        if path:
            def task():
                try:
                    self.btn_convert.configure(state="disabled", text="Processing...")
                    quality = int(self.quality_slider_attr.get())
                    size_tuples = [(s, s) for s in selected_sizes]

                    # Re-apply all logic for export on FULL resolution
                    self.converter.reset_image()
                    self._reapply_logic()
                    self.converter.convert_to_ico(path, sizes=size_tuples, quality=quality)

                    messagebox.showinfo("Success", f"Icon saved at:\n{path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed: {e}")
                finally:
                    self.btn_convert.configure(state="normal", text="🚀 Generate ICO")

            Thread(target=task, daemon=True).start()

    def _export_pngs(self):
        if not self.input_path:
            messagebox.showwarning("Warning", tr("msg_select_image_first"))
            return

        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            def task():
                try:
                    self.btn_export_png.configure(state="disabled")
                    self.converter.reset_image()
                    self._reapply_logic()
                    self.converter.export_all_sizes(folder)
                    messagebox.showinfo("Success", f"PNGs saved in:\n{folder}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    self.btn_export_png.configure(state="normal")

            Thread(target=task, daemon=True).start()

    def _export_webp(self):
        if not self.input_path: return
        path = filedialog.asksaveasfilename(
            defaultextension=".webp", filetypes=[("WebP", "*.webp")],
            initialfile=os.path.splitext(os.path.basename(self.input_path))[0] + ".webp"
        )
        if path:
            try:
                self.converter.reset_image()
                self._reapply_logic()
                self.converter.convert_to_webp(path, quality=90)
                messagebox.showinfo("Success", f"WebP saved at:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _export_pdf(self):
        if not self.input_path: return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
            initialfile=os.path.splitext(os.path.basename(self.input_path))[0] + ".pdf"
        )
        if path:
            try:
                self.converter.reset_image()
                self._reapply_logic()
                self.converter.convert_to_pdf(path)
                messagebox.showinfo("Success", f"PDF saved at:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def get_project_data(self):
        """Returns the current state for project saving"""
        return {
            "type": "icon_converter",
            "input_path": self.input_path,
            "mask": self.mask_var.get(),
            "corner_radius": int(self.corner_slider_attr.get()),
            "padding": int(self.padding_slider_attr.get()),
            "bg_color": self.bg_color,
            "border_width": int(self.border_slider_attr.get()),
            "border_color": self.border_color,
            "brightness": int(self.bright_slider.get()),
            "contrast": int(self.contrast_slider.get()),
            "saturation": int(self.sat_slider.get()),
            "flip_h": self.var_flip_h.get(),
            "flip_v": self.var_flip_v.get(),
            "text_enabled": self.var_text_enable.get(),
            "text": self.entry_text.get().strip(),
            "font": self.font_var.get(),
            "position": self.pos_var.get(),
            "style": self.style_var.get(),
            "quality": int(self.quality_slider_attr.get()),
            "sizes": [s for s, v in self.size_vars.items() if v.get()],
            "text_offset_x": int(self.text_x_slider.get()),
            "text_offset_y": int(self.text_y_slider.get())
        }

    def load_project_data(self, data):
        """Load data from project"""
        path = data.get("source_image") or data.get("input_path")
        if path and os.path.exists(path):
            self.input_path = path
            self.lbl_path.configure(text=os.path.basename(path))
            self.converter = IconConverter(path)
            self._update_preview(path)

        if "sizes" in data:
            target_sizes = data["sizes"]
            for s, v in self.size_vars.items():
                v.set(s in target_sizes)

        if "quality" in data and hasattr(self, "quality_slider_attr"):
            self.quality_slider_attr.set(data["quality"])
        
        if "mask" in data: self.mask_var.set(data["mask"])
        if "corner_radius" in data and hasattr(self, "corner_slider_attr"): self.corner_slider_attr.set(data["corner_radius"])
        if "padding" in data and hasattr(self, "padding_slider_attr"): self.padding_slider_attr.set(data["padding"])
        if "brightness" in data and hasattr(self, "bright_slider"): self.bright_slider.set(data["brightness"])
        if "contrast" in data and hasattr(self, "contrast_slider"): self.contrast_slider.set(data["contrast"])
        if "saturation" in data and hasattr(self, "sat_slider"): self.sat_slider.set(data["saturation"])
        if "flip_h" in data: self.var_flip_h.set(data["flip_h"])
        if "flip_v" in data: self.var_flip_v.set(data["flip_v"])
        if "text_enabled" in data: self.var_text_enable.set(data["text_enabled"])
        if "text" in data: self.entry_text.delete(0, "end"); self.entry_text.insert(0, data["text"])
        if "font" in data: self.font_var.set(data["font"])
        if "position" in data: self.pos_var.set(data["position"])

        self._preview_delayed()
