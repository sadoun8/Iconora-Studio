"""
Iconora Studio - Signature Tab (v2.0)
Decorative fonts, ornaments, opacity slider, color pickers, real-time preview.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from threading import Thread
import os
from PIL import Image
from core.signature_engine import SignatureEngine
from config import EXPORT_SUBDIRS
from i18n import tr

class SignatureTab(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.engine = SignatureEngine(900, 320)
        self._preview_img = None
        self.ink_color   = (20, 20, 80)
        self.title_color = (130, 130, 130)
        self._build_ui()

    # ─── UI Builder ───────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Controls ──
        ctrl = ctk.CTkScrollableFrame(self, width=420)
        ctrl.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        ctk.CTkLabel(ctrl, text="✍️ Signature Studio Pro", font=("Segoe UI Variable Display", 24, "bold")).pack(pady=(20, 10))

        # Name / Title
        ctk.CTkLabel(ctrl, text=tr("sig_name"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=16)
        self.entry_name = ctk.CTkEntry(ctrl, placeholder_text=tr("sig_name_ph"), height=45)
        self.entry_name.insert(0, "John Doe")
        self.entry_name.pack(fill="x", padx=16, pady=5)
        self.entry_name.bind("<KeyRelease>", lambda _: self._preview())

        ctk.CTkLabel(ctrl, text=tr("sig_title"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=16, pady=(10, 0))
        self.entry_title = ctk.CTkEntry(ctrl, placeholder_text=tr("sig_title_ph"), height=40)
        self.entry_title.pack(fill="x", padx=16, pady=5)
        self.entry_title.bind("<KeyRelease>", lambda _: self._preview())

        self._sep(ctrl)

        # Typography
        ctk.CTkLabel(ctrl, text=tr("sig_typography_settings"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=16, pady=(5, 5))
        fonts = self.engine.available_fonts()
        self._font_map = fonts
        
        self.font_var = ctk.StringVar(value=list(fonts.keys())[0])
        ctk.CTkOptionMenu(ctrl, values=list(fonts.keys()), variable=self.font_var, command=lambda _: self._preview()).pack(fill="x", padx=16, pady=3)

        self.title_font_var = ctk.StringVar(value=list(fonts.keys())[0])
        ctk.CTkOptionMenu(ctrl, values=list(fonts.keys()), variable=self.title_font_var, command=lambda _: self._preview()).pack(fill="x", padx=16, pady=3)

        self._create_slider_control(ctrl, tr("sig_size"), 30, 160, 90, "font_size_slider")
        self._create_slider_control(ctrl, tr("sig_line_spacing"), -20, 100, 15, "spacing_slider")

        self._sep(ctrl)

        # Artistic Adjustments
        ctk.CTkLabel(ctrl, text=tr("sig_artistic_adjust"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=16, pady=(5, 5))
        
        self._create_slider_control(ctrl, tr("sig_slant"), -1, 1, 0, "slant_slider", is_float=True)
        self._create_slider_control(ctrl, tr("sig_ink_thickness"), 0.1, 3.0, 1.0, "thickness_slider", is_float=True)
        self._create_slider_control(ctrl, tr("sig_rotation"), -45, 45, 0, "rotation_slider")

        self.style_var = ctk.StringVar(value=tr("opt_normal"))
        ctk.CTkOptionMenu(ctrl, values=[tr("opt_normal"), tr("opt_upward"), tr("opt_slanted")], variable=self.style_var, command=lambda _: self._preview()).pack(fill="x", padx=16, pady=10)

        self._sep(ctrl)

        # Ornament & Color
        ctk.CTkLabel(ctrl, text=tr("sig_ornament_color"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=16, pady=(5, 5))
        
        self.orn_var = ctk.StringVar(value=tr("opt_none"))
        # Fix: need to handle translated "None" in engine or map it
        orn_values = [tr("opt_none")] + [n for n in self.engine.ornament_names() if n != "None"]
        ctk.CTkOptionMenu(ctrl, values=orn_values, variable=self.orn_var, command=lambda _: self._preview()).pack(fill="x", padx=16, pady=5)

        self.btn_color = ctk.CTkButton(ctrl, text=tr("sig_pick_main_color"), fg_color=self._rgb_to_hex(self.ink_color), command=self._pick_color, height=35)
        self.btn_color.pack(fill="x", padx=16, pady=5)

        self.btn_title_color = ctk.CTkButton(ctrl, text=tr("sig_pick_title_color"), fg_color=self._rgb_to_hex(self.title_color), command=self._pick_title_color, height=35)
        self.btn_title_color.pack(fill="x", padx=16, pady=5)

        self._sep(ctrl)

        # Options & Export
        ctk.CTkLabel(ctrl, text=tr("sig_options"), font=("Segoe UI Variable Text", 12, "bold")).pack(anchor="w", padx=16, pady=(5, 5))
        
        self.var_transparent = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(ctrl, text=tr("sig_transparent"), variable=self.var_transparent, command=self._preview).pack(anchor="w", padx=20, pady=4)

        self.var_ink = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(ctrl, text=tr("sig_ink"), variable=self.var_ink, command=self._preview).pack(anchor="w", padx=20, pady=4)

        self._create_slider_control(ctrl, tr("sig_overall_opacity"), 0, 100, 100, "opacity_slider")

        # Hidden sliders for dragging offsets
        self.sig_x_slider = ctk.CTkSlider(self, from_=-800, to=800)
        self.sig_x_slider.set(0)
        self.sig_y_slider = ctk.CTkSlider(self, from_=-800, to=800)
        self.sig_y_slider.set(0)

        self.btn_save = ctk.CTkButton(
            ctrl, text=tr("sig_save_signature"), height=60, 
            font=("Segoe UI Variable Display", 16, "bold"), corner_radius=15, 
            command=self._save, fg_color=("#3B82F6", "#6366F1"), hover_color=("#2563EB", "#4F46E5")
        )
        self.btn_save.pack(fill="x", padx=16, pady=(30, 5))

        self.btn_gallery = ctk.CTkButton(
            ctrl, text="📚 " + tr("sig_open_gallery"), 
            height=40, font=("Segoe UI Variable Text", 13),
            command=self._open_gallery, fg_color="transparent", border_width=1
        )
        self.btn_gallery.pack(fill="x", padx=16, pady=5)

        self.btn_save_lib = ctk.CTkButton(
            ctrl, text="⭐ " + tr("sig_add_to_library"), 
            height=40, font=("Segoe UI Variable Text", 13),
            command=self._save_to_library, fg_color="transparent", border_width=1
        )
        self.btn_save_lib.pack(fill="x", padx=16, pady=5)

        # Additional formats
        format_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        format_row.pack(fill="x", padx=16, pady=(0, 30))

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

        # ── Preview ──
        prev = ctk.CTkFrame(self)
        prev.grid(row=0, column=1, sticky="nsew")
        
        self.preview_canvas_bg = tk.Canvas(prev, bg="gray20", highlightthickness=0)
        self.preview_canvas_bg.pack(expand=True, fill="both", padx=20, pady=20)
        self.preview_canvas_bg.bind("<Configure>", lambda e: self._draw_checkerboard())

        self.prev_canvas = ctk.CTkLabel(self.preview_canvas_bg, text="", bg_color="transparent")
        self.prev_canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Bind mouse events for dragging
        self.prev_canvas.bind("<Button-1>", self._on_drag_start)
        self.prev_canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.prev_canvas.bind("<ButtonRelease-1>", self._on_drag_end)

        # Help hint
        drag_hint = "🖱️ Drag to move signature | اسحب لتحريك التوقيع"
        ctk.CTkLabel(prev, text=drag_hint, font=("Segoe UI Variable Text", 10), text_color="gray").pack(pady=(0, 10))

    def _create_slider_control(self, parent, label, from_val, to_val, start_val, attr_name, is_float=False):
        lbl = ctk.CTkLabel(parent, text=label, font=("Segoe UI Variable Text", 11))
        lbl.pack(padx=16, pady=(8, 0), anchor="w")
        slider = ctk.CTkSlider(parent, from_=from_val, to=to_val, command=lambda v, l=lbl, n=label, f=is_float: self._on_slider_change(v, l, n, f))
        slider.set(start_val)
        slider.pack(fill="x", padx=16, pady=2)
        setattr(self, attr_name, slider)
        return slider

    def _on_slider_change(self, val, label_widget, name, is_float):
        v_str = f"{val:.2f}" if is_float else f"{int(val)}"
        label_widget.configure(text=f"{name}: {v_str}")
        self._preview()

    def _on_drag_start(self, event):
        self._drag_data = {"x": event.x, "y": event.y}
        self.prev_canvas.configure(cursor="fleur")

    def _on_drag_motion(self, event):
        if not hasattr(self, "_drag_data") or not self._drag_data: return
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        sensitivity = 1.5
        new_x = self.sig_x_slider.get() + (dx * sensitivity)
        new_y = self.sig_y_slider.get() + (dy * sensitivity)
        self.sig_x_slider.set(max(-800, min(800, new_x)))
        self.sig_y_slider.set(max(-800, min(800, new_y)))
        self._drag_data = {"x": event.x, "y": event.y}
        self._preview()

    def _on_drag_end(self, event):
        self._drag_data = None
        self.prev_canvas.configure(cursor="")

    def _draw_checkerboard(self):
        self.preview_canvas_bg.delete("checker")
        w = self.preview_canvas_bg.winfo_width()
        h = self.preview_canvas_bg.winfo_height()
        if w <= 1 or h <= 1: return
        size = 20
        for i in range(0, w, size):
            for j in range(0, h, size):
                if (i // size + j // size) % 2 == 0:
                    self.preview_canvas_bg.create_rectangle(i, j, i+size, j+size, fill="gray25", outline="", tags="checker")
        self.prev_canvas.lift()

    def _preview(self):
        name = self.entry_name.get().strip()
        if not name: return
        try:
            opacity = int(self.opacity_slider.get()) / 100

            # Internal mapping for ornament if translated
            orn_val = self.orn_var.get()
            if orn_val == tr("opt_none"): orn_val = "None"

            # Style mapping
            style_val = self.style_var.get()
            if style_val == tr("opt_normal"): style_val = "Normal"
            elif style_val == tr("opt_upward"): style_val = "Upward (صاعد)"
            elif style_val == tr("opt_slanted"): style_val = "Slanted (مائل)"

            img = self.engine.generate(
                name=name,
                title=self.entry_title.get().strip(),
                ornament=orn_val,
                font_path=self._current_font(),
                title_font_path=self._current_title_font(),
                font_size=int(self.font_size_slider.get()),
                color=self.ink_color,
                title_color=self.title_color,
                opacity=opacity,
                transparent=self.var_transparent.get(),
                ink_effect=self.var_ink.get(),
                style=style_val,
                spacing=int(self.spacing_slider.get()),
                slant=float(self.slant_slider.get()),
                thickness=float(self.thickness_slider.get()),
                rotation=int(self.rotation_slider.get()),
                offset_x=int(self.sig_x_slider.get()),
                offset_y=int(self.sig_y_slider.get())
            )
            
            # Show preview
            pw, ph = img.size
            ratio = min(800/pw, 280/ph)
            tw, th = max(1, int(pw * ratio)), max(1, int(ph * ratio))
            self._preview_img = ctk.CTkImage(light_image=img, dark_image=img, size=(tw, th))
            self.prev_canvas.configure(image=self._preview_img, text="")
        except Exception as e:
            self.prev_canvas.configure(text=f"⚠ {e}", image=None)

    # ─── Helpers ──────────────────────────────────────────────

    def _current_font(self):
        """Get the absolute path of the selected name font"""
        return self._font_map.get(self.font_var.get())

    def _current_title_font(self):
        """Get the absolute path of the selected title font"""
        return self._font_map.get(self.title_font_var.get())

    def _pick_color(self):
        color = colorchooser.askcolor(initialcolor=self._rgb_to_hex(self.ink_color), title=tr("sig_pick_sig_color"))
        if color[0]:
            self.ink_color = tuple(map(int, color[0]))
            self.btn_color.configure(fg_color=color[1])
            self._preview()

    def _pick_title_color(self):
        color = colorchooser.askcolor(initialcolor=self._rgb_to_hex(self.title_color), title=tr("sig_pick_title_color"))
        if color[0]:
            self.title_color = tuple(map(int, color[0]))
            self.btn_title_color.configure(fg_color=color[1])
            self._preview()

    def _sep(self, parent):
        """Visual divider helper"""
        f = ctk.CTkFrame(parent, height=2, fg_color=("gray90", "gray30"))
        f.pack(fill="x", padx=20, pady=15)

    def _rgb_to_hex(self, rgb):
        """Convert (R,G,B) to #RRGGBB"""
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    @staticmethod
    def _make_checker(size, box=20):
        """Create a grey/white checkerboard background for transparency visualization."""
        from PIL import Image as PI, ImageDraw
        img = PI.new("RGB", size, (200, 200, 200))
        draw = ImageDraw.Draw(img)
        for y in range(0, size[1], box):
            for x in range((y // box) % 2 * box, size[0], box * 2):
                draw.rectangle([x, y, x + box - 1, y + box - 1], fill=(240, 240, 240))
        return img.convert("RGBA")

    def _generate_signature_image(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning(tr("msg_warning"), tr("sig_enter_name"))
            return None

        opacity = int(self.opacity_slider.get()) / 100
        orn_val = self.orn_var.get()
        if orn_val == tr("opt_none"): orn_val = "None"

        style_val = self.style_var.get()
        if style_val == tr("opt_normal"): style_val = "Normal"
        elif style_val == tr("opt_upward"): style_val = "Upward (صاعد)"
        elif style_val == tr("opt_slanted"): style_val = "Slanted (مائل)"

        return self.engine.generate(
            name=name, title=self.entry_title.get().strip(),
            ornament=orn_val,
            font_path=self._current_font(),
            title_font_path=self._current_title_font(),
            font_size=int(self.font_size_slider.get()),
            color=self.ink_color,
            title_color=self.title_color,
            opacity=opacity,
            transparent=self.var_transparent.get(),
            ink_effect=self.var_ink.get(),
            style=style_val,
            spacing=int(self.spacing_slider.get()),
            slant=float(self.slant_slider.get()),
            thickness=float(self.thickness_slider.get()),
            rotation=int(self.rotation_slider.get()),
            offset_x=int(self.sig_x_slider.get()),
            offset_y=int(self.sig_y_slider.get())
        )

    def _export_webp(self):
        img = self._generate_signature_image()
        if not img: return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".webp",
            filetypes=[("WebP Image", "*.webp")],
            initialdir=str(EXPORT_SUBDIRS["Signatures"]),
            initialfile=f"{self.entry_name.get().lower().replace(' ','_')}_signature.webp")
        if path:
            self.engine.save(img, path)
            messagebox.showinfo(tr("msg_success"), f"{tr('msg_file_saved_at')}\n{path}")

    def _export_pdf(self):
        img = self._generate_signature_image()
        if not img: return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
            initialdir=str(EXPORT_SUBDIRS["Signatures"]),
            initialfile=f"{self.entry_name.get().lower().replace(' ','_')}_signature.pdf")
        if path:
            self.engine.save(img, path)
            messagebox.showinfo(tr("msg_success"), f"{tr('msg_file_saved_at')}\n{path}")

    def _save(self):
        img = self._generate_signature_image()
        if not img: return

        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")],
            initialdir=str(EXPORT_SUBDIRS["Signatures"]),
            initialfile=f"{self.entry_name.get().lower().replace(' ','_')}_signature.png")
        if not path: return

        try:
            self.engine.save(img, path)
            messagebox.showinfo(tr("msg_success"), f"{tr('msg_file_saved_at')}\n{path}")
        except Exception as e:
            messagebox.showerror(tr("msg_error"), str(e))

    def _open_gallery(self):
        """Open the signature gallery dialog"""
        from ui.signature_library import SignatureLibraryDialog
        dialog = SignatureLibraryDialog(self, callback=self.load_project_data)
        dialog.grab_set()

    def _save_to_library(self):
        """Save current signature to the gallery/library"""
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning(tr("msg_warning"), tr("sig_enter_name"))
            return

        try:
            from core.project_manager import ProjectManager
            import json
            import datetime
            
            lib_path = EXPORT_SUBDIRS["Signatures"] / "library.json"
            library = []
            if lib_path.exists():
                with open(lib_path, "r", encoding="utf-8") as f:
                    library = json.load(f)
            
            # Create metadata
            data = {
                "name": name,
                "title": self.entry_title.get().strip(),
                "font": self.font_var.get(),
                "title_font": self.title_font_var.get(),
                "font_size": int(self.font_size_slider.get()),
                "spacing": int(self.spacing_slider.get()),
                "slant": float(self.slant_slider.get()),
                "thickness": float(self.thickness_slider.get()),
                "rotation": int(self.rotation_slider.get()),
                "ornament": self.orn_var.get(),
                "ink_color": self._hex(self.ink_color),
                "title_color": self._hex(self.title_color),
                "transparent": self.var_transparent.get(),
                "ink_effect": self.var_ink.get(),
                "opacity": int(self.opacity_slider.get()),
                "offset_x": int(self.sig_x_slider.get()),
                "offset_y": int(self.sig_y_slider.get()),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Check if exists and update or add
            updated = False
            for i, item in enumerate(library):
                if item["name"] == name:
                    library[i] = data
                    updated = True
                    break
            
            if not updated:
                library.append(data)
                
            with open(lib_path, "w", encoding="utf-8") as f:
                json.dump(library, f, indent=4, ensure_ascii=False)
                
            # Also save a preview image
            img = self._generate_signature_image()
            preview_path = EXPORT_SUBDIRS["Signatures"] / f"lib_{name.lower().replace(' ', '_')}.png"
            self.engine.save(img, str(preview_path))
            
            messagebox.showinfo(tr("msg_success"), tr("sig_added_to_library"))
            
        except Exception as e:
            messagebox.showerror(tr("msg_error"), f"Failed to save to library: {e}")

    def get_project_data(self):
        """Returns the current state for project saving"""
        return {
            "type": "signature",
            "name": self.entry_name.get().strip(),
            "title": self.entry_title.get().strip(),
            "font": self.font_var.get(),
            "title_font": self.title_font_var.get(),
            "font_size": int(self.font_size_slider.get()),
            "spacing": int(self.spacing_slider.get()),
            "slant": float(self.slant_slider.get()),
            "thickness": float(self.thickness_slider.get()),
            "rotation": int(self.rotation_slider.get()),
            "ornament": self.orn_var.get(),
            "ink_color": self._rgb_to_hex(self.ink_color),
            "title_color": self._rgb_to_hex(self.title_color),
            "transparent": self.var_transparent.get(),
            "ink_effect": self.var_ink.get(),
            "opacity": int(self.opacity_slider.get()),
            "offset_x": int(self.sig_x_slider.get()),
            "offset_y": int(self.sig_y_slider.get())
        }

    def load_project_data(self, data):
        if "name"  in data: self.entry_name.delete(0,"end");  self.entry_name.insert(0, data["name"])
        if "title" in data: self.entry_title.delete(0,"end"); self.entry_title.insert(0, data["title"])
        if "font" in data: self.font_var.set(data["font"])
        if "title_font" in data: self.title_font_var.set(data["title_font"])
        if "font_size" in data: self.font_size_slider.set(data["font_size"])
        if "spacing" in data: self.spacing_slider.set(data["spacing"])
        if "slant" in data: self.slant_slider.set(data["slant"])
        if "thickness" in data: self.thickness_slider.set(data["thickness"])
        if "rotation" in data: self.rotation_slider.set(data["rotation"])
        if "ornament" in data: self.orn_var.set(data["ornament"])
        if "ink_color" in data and data["ink_color"].startswith("#"):
            c = data["ink_color"]
            self.ink_color = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
            self.btn_color.configure(fg_color=c)
        if "title_color" in data and data["title_color"].startswith("#"):
            c = data["title_color"]
            self.title_color = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
            self.btn_title_color.configure(fg_color=c)
        if "transparent" in data: self.var_transparent.set(data["transparent"])
        if "ink_effect" in data: self.var_ink.set(data["ink_effect"])
        if "opacity" in data: self.opacity_slider.set(data["opacity"])
        if "offset_x" in data: self.sig_x_slider.set(data["offset_x"])
        if "offset_y" in data: self.sig_y_slider.set(data["offset_y"])
        self._preview()
