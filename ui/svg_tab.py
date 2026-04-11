"""
Iconora Studio - SVG Converter Tab UI
Modernized with sidebar integration and tracing features.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from threading import Thread
import os
from PIL import Image
from core.svg_converter import SVGConverter
from core.svg_editor import SVGEditor
from i18n import tr, get_language
from config import EXPORT_SUBDIRS

class SVGConverterTab(ctk.CTkFrame):
    """UI for SVG conversion with tracing and embedding options"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.converter = None
        self.svg_editor = SVGEditor()
        self.input_path = None
        self.preview_image = None
        self.fill_color = (0, 0, 0)
        self._build_ui()

    def _build_ui(self):
        """Build the modernized SVG converter UI"""
        is_en = get_language() == "en"

        # Preview takes weight 1, Controls take weight 0
        if is_en:
            self.grid_columnconfigure(0, weight=0) # Controls
            self.grid_columnconfigure(1, weight=1) # Preview
        else:
            self.grid_columnconfigure(1, weight=0) # Controls
            self.grid_columnconfigure(0, weight=1) # Preview

        self.grid_rowconfigure(0, weight=1)

        # ── Left: Controls ───────────────────────────────────────────────────
        self.controls_frame = ctk.CTkScrollableFrame(self, width=320, corner_radius=0, fg_color=("gray95", "gray10"))
        self.controls_frame.grid(row=0, column=0 if is_en else 1, sticky="nsew")

        ctk.CTkLabel(self.controls_frame, text="✨ Vector Studio", font=("Segoe UI Variable Display", 26, "bold")).pack(pady=(30, 20))

        # 1. Source Selection
        select_card = ctk.CTkFrame(self.controls_frame, fg_color=("white", "gray14"), corner_radius=12)
        select_card.pack(fill="x", padx=15, pady=10)

        self.btn_select = ctk.CTkButton(
            select_card, text="📁 Select Image",
            command=self._select_image,
            height=45, corner_radius=10,
            font=("Segoe UI Variable Display", 14, "bold"),
            fg_color=("#3B82F6", "#6366F1"), hover_color=("#2563EB", "#4F46E5")
        )
        self.btn_select.pack(fill="x", padx=15, pady=(15, 5))

        self.lbl_path = ctk.CTkLabel(select_card, text=tr("no_image_selected"), font=("Segoe UI Variable Text", 10), text_color="gray")
        self.lbl_path.pack(pady=(0, 15))

        # 1.5 AI Smart Trace Presets
        ai_card = ctk.CTkFrame(self.controls_frame, fg_color=("#8B5CF6", "#7C3AED"), corner_radius=12)
        ai_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(ai_card, text="✨ AI Smart Trace", font=("Segoe UI Variable Text", 12, "bold"), text_color="white").pack(padx=15, pady=(15, 5), anchor="w")

        ai_btns = ctk.CTkFrame(ai_card, fg_color="transparent")
        ai_btns.pack(fill="x", padx=10, pady=(0, 15))

        presets = [("High Detail", "high"), ("Minimalist", "low"), ("Silhouette", "black")]
        for label, pid in presets:
            ctk.CTkButton(
                ai_btns, text=label, width=80, height=28, corner_radius=6,
                fg_color="white", text_color="#7C3AED", font=("Segoe UI Variable Text", 10),
                command=lambda p=pid: self._apply_ai_preset(p)
            ).pack(side="left", padx=3, expand=True)

        # 2. Vectorization Settings
        settings_card = ctk.CTkFrame(self.controls_frame, fg_color=("white", "gray14"), corner_radius=12)
        settings_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(settings_card, text="Tracing Engine", font=("Segoe UI Variable Text", 12, "bold")).pack(padx=15, pady=(15, 10), anchor="w")

        self.trace_var = tk.BooleanVar(value=True)
        self.check_trace = ctk.CTkCheckBox(settings_card, text="Enable Outline Tracing", variable=self.trace_var, command=self._toggle_trace)
        self.check_trace.pack(padx=15, pady=8, anchor="w")

        self.simplify_var = tk.BooleanVar(value=True)
        self.check_simplify = ctk.CTkCheckBox(settings_card, text="Simplify Vector Paths", variable=self.simplify_var, command=self._toggle_simplify)
        self.check_simplify.pack(padx=15, pady=8, anchor="w")

        self.embed_var = tk.BooleanVar(value=False)
        self.check_embed = ctk.CTkCheckBox(settings_card, text="Embed Bitmap Reference", variable=self.embed_var)
        self.check_embed.pack(padx=15, pady=8, anchor="w")

        self.bg_trans_var = tk.BooleanVar(value=True)
        self.check_bg_trans = ctk.CTkCheckBox(settings_card, text="Transparent Background", variable=self.bg_trans_var)
        self.check_bg_trans.pack(padx=15, pady=(8, 20), anchor="w")

        # 3. Dynamic Controls
        self.color_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        self.color_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(self.color_frame, text="Vector Path Color", font=("Segoe UI Variable Text", 11)).pack(anchor="w")
        self.btn_color = ctk.CTkButton(
            self.color_frame, text="", fg_color="black", height=30,
            command=self._pick_color, border_width=1, border_color="gray50"
        )
        self.btn_color.pack(fill="x", pady=5)
        self.threshold_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        self.threshold_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(self.threshold_frame, text="Intensity Threshold", font=("Segoe UI Variable Text", 11)).pack(anchor="w")
        self.threshold_slider = ctk.CTkSlider(self.threshold_frame, from_=0, to=255, height=18)
        self.threshold_slider.set(128)
        self.threshold_slider.pack(fill="x", pady=5)

        self.simplify_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        self.simplify_frame.pack(fill="x", padx=15, pady=(0, 20))

        ctk.CTkLabel(self.simplify_frame, text="Path Precision", font=("Segoe UI Variable Text", 11)).pack(anchor="w")
        self.simplify_slider = ctk.CTkSlider(self.simplify_frame, from_=0.1, to=5.0, height=18)
        self.simplify_slider.set(1.5)
        self.simplify_slider.pack(fill="x", pady=5)

        # 4. Action
        self.btn_convert = ctk.CTkButton(
            self.controls_frame,
            text="🚀 Export SVG Vector",
            command=self._convert,
            height=55, corner_radius=12,
            fg_color=("#10B981", "#059669"), hover_color=("#059669", "#047857"),
            font=("Segoe UI Variable Display", 16, "bold")
        )
        self.btn_convert.pack(fill="x", padx=20, pady=40)

        # ── Right: Preview Area ──────────────────────────────────────────────
        self.preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.preview_frame.grid(row=0, column=1 if is_en else 0, sticky="nsew", padx=20, pady=20)

        # Inner canvas with custom border
        canvas_bg = ("#E2E8F0", "#1E293B")
        self.canvas_container = ctk.CTkFrame(self.preview_frame, fg_color=canvas_bg, corner_radius=20, border_width=1, border_color=("gray80", "gray25"))
        self.canvas_container.pack(expand=True, fill="both", padx=20, pady=20)

        self.canvas_preview = tk.Canvas(self.canvas_container, bg="gray20", highlightthickness=0, borderwidth=0)
        self.canvas_preview.pack(expand=True, fill="both", padx=4, pady=4)
        self.canvas_preview.bind("<Configure>", lambda e: self._draw_checkerboard())

        self.preview_label = ctk.CTkLabel(self.canvas_preview, text=tr("msg_no_preview"), font=("Segoe UI Variable Display", 14), text_color="gray60")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

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


    def _pick_color(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(initialcolor=self._hex(self.fill_color))[0]
        if color:
            self.fill_color = tuple(map(int, color))
            self.btn_color.configure(fg_color=self._hex(self.fill_color))

    def _hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def _apply_ai_preset(self, preset_id):
        """Applies AI-powered tracing presets"""
        if preset_id == "high":
            self.threshold_slider.set(128)
            self.simplify_var.set(False)
            self.trace_var.set(True)
        elif preset_id == "low":
            self.threshold_slider.set(160)
            self.simplify_var.set(True)
            self.simplify_slider.set(2.5)
        elif preset_id == "black":
            self.threshold_slider.set(200)
            self.fill_color = (0, 0, 0)
            self.btn_color.configure(fg_color="black")

        self._toggle_trace()
        self._toggle_simplify()
        messagebox.showinfo("AI Vector", f"AI '{preset_id}' preset applied successfully!")

    def _select_image(self):
        path = filedialog.askopenfilename(
            title=tr("dlg_select_image"),
            filetypes=[(tr("lbl_image_files"), "*.png *.jpg *.jpeg *.bmp"), (tr("lbl_all_files"), "*.*")]
        )
        if path:
            self.input_path = path
            self.lbl_path.configure(text=os.path.basename(path))
            self._update_preview(path)

    def _update_preview(self, path):
        try:
            img = Image.open(path)
            # Make the preview much larger
            max_size = (1200, 1200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.preview_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=self.preview_image, text="")
        except Exception as e:
            self.preview_label.configure(text=f"Preview Error: {e}")

    def _toggle_trace(self):
        if self.trace_var.get():
            self.threshold_frame.pack(fill="x", padx=20, pady=(5, 5))
            self.check_simplify.configure(state="normal")
            self._toggle_simplify()
        else:
            self.threshold_frame.pack_forget()
            self.check_simplify.configure(state="disabled")
            self.simplify_frame.pack_forget()

    def _toggle_simplify(self):
        if self.simplify_var.get() and self.trace_var.get():
            self.simplify_frame.pack(fill="x", padx=20, pady=(0, 15))
        else:
            self.simplify_frame.pack_forget()

    def _convert(self):
        if not self.input_path:
            messagebox.showwarning(tr("msg_warning"), tr("msg_select_image_first"))
            return

        default_dir = EXPORT_SUBDIRS["SVGs"]
        path = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG Vector", "*.svg")],
            initialdir=str(default_dir),
            initialfile=os.path.splitext(os.path.basename(self.input_path))[0] + ".svg"
        )

        if not path: return

        def task():
            try:
                self.btn_convert.configure(state="disabled", text=tr("status_converting"))
                self.converter = SVGConverter(self.input_path)

                # Perform conversion
                self.converter.convert_to_svg(
                    path,
                    embed_image=self.embed_var.get(),
                    trace=self.trace_var.get(),
                    threshold=int(self.threshold_slider.get()),
                    simplify=self.simplify_var.get(),
                    tolerance=float(self.simplify_slider.get()),
                    fill_color=self._hex(self.fill_color),
                    bg_transparent=self.bg_trans_var.get()
                )

                messagebox.showinfo(tr("msg_success"), f"{tr('msg_saved_svg')}\n{path}")

            except Exception as e:
                messagebox.showerror(tr("lbl_error"), f"Conversion failed: {e}")
            finally:
                self.btn_convert.configure(state="normal", text=tr("btn_convert_svg"))

        Thread(target=task, daemon=True).start()

    def get_project_data(self):
        """Returns the current state for project saving"""
        return {
            "type": "svg_converter",
            "input_path": self.input_path,
            "embed_image": self.embed_var.get(),
            "enable_trace": self.trace_var.get(),
            "threshold": int(self.threshold_slider.get()),
            "simplify": self.simplify_var.get(),
            "tolerance": float(self.simplify_slider.get()),
            "fill_color": self._hex(self.fill_color),
            "bg_transparent": self.bg_trans_var.get()
        }

    def load_project_data(self, project_data):
        path = project_data.get("source_image") or project_data.get("input_path")
        if path and os.path.exists(path):
            self.input_path = path
            self.lbl_path.configure(text=os.path.basename(path))
            self._update_preview(path)

        self.embed_var.set(project_data.get("embed_image", False))
        self.trace_var.set(project_data.get("enable_trace", True))
        self.threshold_slider.set(project_data.get("threshold", 128))
        self.simplify_var.set(project_data.get("simplify", True))
        self.simplify_slider.set(project_data.get("tolerance", 1.5))
        self.bg_trans_var.set(project_data.get("bg_transparent", True))

        fill_color = project_data.get("fill_color")
        if isinstance(fill_color, str) and fill_color.startswith("#") and len(fill_color) == 7:
            try:
                self.fill_color = tuple(int(fill_color[i:i+2], 16) for i in (1, 3, 5))
                self.btn_color.configure(fg_color=fill_color)
            except Exception:
                pass

        self._toggle_trace()
        self._toggle_simplify()
