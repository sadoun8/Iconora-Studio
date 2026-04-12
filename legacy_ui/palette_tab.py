"""
Iconora Studio - Palette Generator Tab UI
Modernized with sidebar integration and document exports.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import pyperclip
from pathlib import Path
from threading import Thread
import os
from core.palette_engine import PaletteEngine
from core.ai_assistant import AIAssistant
from i18n import tr, get_language
from config import EXPORT_SUBDIRS

class PaletteTab(ctk.CTkFrame):
    """Modernized UI for smart color palettes"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.palette_engine = PaletteEngine()
        self.ai_assistant = AIAssistant()
        self.selected_palette = None
        self.custom_colors = None
        self._build_ui()

    def _build_ui(self):
        """Build the modernized palette UI"""
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        is_en = get_language() == "en"

        # ── Left Side: Controls ──────────────────────────────────────────────
        self.controls_frame = ctk.CTkScrollableFrame(self, width=380, corner_radius=0, fg_color=("gray95", "gray10"))
        self.controls_frame.grid(row=0, column=0 if is_en else 1, sticky="nsew")

        ctk.CTkLabel(self.controls_frame, text="🎨 Palette Studio", font=("Segoe UI Variable Display", 26, "bold")).pack(pady=(30, 20))

        # 1. Algorithmic Generation
        algo_card = ctk.CTkFrame(self.controls_frame, fg_color=("white", "gray14"), corner_radius=12)
        algo_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(algo_card, text="Smart Generation", font=("Segoe UI Variable Text", 12, "bold")).pack(padx=15, pady=(15, 5), anchor="w")

        self.algo_base_color = "#6366F1"
        self.btn_algo_base = ctk.CTkButton(
            algo_card, text="Pick Base Color",
            fg_color=self.algo_base_color,
            height=38, corner_radius=8,
            command=self._pick_algo_color
        )
        self.btn_algo_base.pack(fill="x", padx=15, pady=8)

        self.algo_mode_var = ctk.StringVar(value="Analogous")
        self.algo_mode_menu = ctk.CTkOptionMenu(
            algo_card, values=["Monochromatic", "Analogous", "Complementary", "Triadic"],
            variable=self.algo_mode_var, height=38, corner_radius=8
        )
        self.algo_mode_menu.pack(fill="x", padx=15, pady=8)

        ctk.CTkButton(
            algo_card, text="✨ Generate Palette",
            command=self._generate_algorithmic,
            height=45, corner_radius=8,
            fg_color=("#3B82F6", "#6366F1"), hover_color=("#2563EB", "#4F46E5")
        ).pack(fill="x", padx=15, pady=(8, 15))

        # 1.5 AI Palette Generator
        ai_card = ctk.CTkFrame(self.controls_frame, fg_color=("#8B5CF6", "#7C3AED"), corner_radius=12)
        ai_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(ai_card, text="✨ AI Palette Generator", font=("Segoe UI Variable Text", 12, "bold"), text_color="white").pack(padx=15, pady=(15, 5), anchor="w")

        self.entry_ai_palette = ctk.CTkEntry(ai_card, placeholder_text="e.g. Modern Tech, Warm Sunset...", height=38, border_width=0)
        self.entry_ai_palette.pack(fill="x", padx=15, pady=5)

        self.btn_ai_palette = ctk.CTkButton(
            ai_card, text="Generate with AI",
            fg_color="white", text_color="#7C3AED", hover_color="#F3E8FF",
            height=38, corner_radius=8, font=("Segoe UI Variable Display", 12, "bold"),
            command=self._generate_ai_palette
        )
        self.btn_ai_palette.pack(fill="x", padx=15, pady=(5, 15))

        # 2. Preset Style Selection
        style_card = ctk.CTkFrame(self.controls_frame, fg_color=("white", "gray14"), corner_radius=12)
        style_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(style_card, text="Premium Presets", font=("Segoe UI Variable Text", 12, "bold")).pack(padx=15, pady=(15, 5), anchor="w")
        self.style_var = ctk.StringVar(value="Modern")
        self.style_menu = ctk.CTkOptionMenu(
            style_card, values=["Modern", "Luxury", "Pastel", "Vibrant"],
            variable=self.style_var, command=self._refresh_palette_list,
            height=38, corner_radius=8
        )
        self.style_menu.pack(fill="x", padx=15, pady=(8, 15))

        # 3. Palette List
        self.list_frame = ctk.CTkScrollableFrame(self.controls_frame, height=200, fg_color="transparent")
        self.list_frame.pack(fill="x", padx=15, pady=5)

        # 4. Action Button
        self.btn_save = ctk.CTkButton(
            self.controls_frame,
            text="💾 Export Collection",
            command=self._save_palette,
            height=55,
            fg_color=("#10B981", "#059669"),
            hover_color=("#059669", "#047857"),
            font=("Segoe UI Variable Display", 15, "bold"),
            corner_radius=12
        )
        self.btn_save.pack(fill="x", padx=20, pady=30)

        # ── Right Side: Preview ──────────────────────────────────────────────
        self.preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.preview_frame.grid(row=0, column=1 if is_en else 0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.preview_frame, text="Colors Preview", font=("Segoe UI Variable Display", 22, "bold")).pack(pady=(20, 10))
        self.lbl_desc = ctk.CTkLabel(self.preview_frame, text="Choose a theme or generate one to see colors", font=("Segoe UI Variable Text", 13), text_color="gray")
        self.lbl_desc.pack(pady=(0, 30))

        # Swatch Grid
        self.colors_container = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.colors_container.pack(expand=True, fill="both", padx=40, pady=20)

        self._refresh_palette_list()


    def _refresh_palette_list(self, style=None):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        style = self.style_var.get()
        palettes = self.palette_engine.PALETTES.get(style, self.palette_engine.PALETTES.get("Modern"))

        for p_name in palettes:
            btn = ctk.CTkButton(
                self.list_frame, text=f"  {p_name}",
                fg_color="transparent", text_color=("gray20", "gray85"),
                font=("Segoe UI Variable Text", 13),
                anchor="w", height=35,
                hover_color=("gray85", "gray20"),
                command=lambda n=p_name: self._select_palette(n)
            )
            btn.pack(fill="x", pady=2)

    def _update_swatches(self, colors):
        """Update the visual swatch grid with hex copy functionality"""
        for widget in self.colors_container.winfo_children():
            widget.destroy()

        for hex_code in colors:
            card = ctk.CTkFrame(self.colors_container, fg_color="transparent")
            card.pack(side="left", expand=True, fill="both", padx=10)

            swatch = ctk.CTkFrame(card, height=300, fg_color=hex_code, corner_radius=16, border_width=1, border_color=("gray80", "gray30"))
            swatch.pack(fill="both", expand=True)

            ctk.CTkLabel(card, text=hex_code.upper(), font=("Segoe UI Variable Display", 14, "bold")).pack(pady=(15, 2))

            copy_btn = ctk.CTkButton(
                card, text="Copy Hex", height=28, width=80,
                font=("Segoe UI Variable Text", 11),
                fg_color="transparent", border_width=1,
                command=lambda h=hex_code: self._copy_hex(h)
            )
            copy_btn.pack(pady=(0, 10))

    def _copy_hex(self, hx):
        pyperclip.copy(hx)

    def _generate_algorithmic(self):
        """Generate a palette dynamically using the palette engine algorithm"""
        try:
            mode = self.algo_mode_var.get()
            colors = self.palette_engine.generate_algorithmic_palette(self.algo_base_color, mode=mode)
            self.selected_palette = f"AI_{mode}"
            self.custom_colors = colors
            self._update_swatches(colors)
            self.lbl_desc.configure(text=f"Dynamically calculated {mode} harmony", text_color=("#3B82F6", "#6366F1"))
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate: {e}")

    def _pick_algo_color(self):
        rgb, hx = colorchooser.askcolor(self.algo_base_color)
        if hx:
            self.algo_base_color = hx
            self.btn_algo_base.configure(fg_color=hx, text_color="white" if self._is_dark(hx) else "black")

    def _select_palette(self, name):
        self.selected_palette = name
        self.custom_colors = None
        style = self.style_var.get()
        data = self.palette_engine.get_palette_colors(style, name)
        colors = data.get("colors", [])
        self._update_swatches(colors)
        self.lbl_desc.configure(text=data.get("description", "Premium color collection"), text_color=("#3B82F6", "#6366F1"))

    def _is_dark(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 128

    def _save_palette(self):
        if not self.selected_palette:
            messagebox.showwarning("Warning", "Please select a palette first")
            return

        default_dir = EXPORT_SUBDIRS["Palettes"]
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialdir=str(default_dir),
            initialfile=f"{self.selected_palette.lower().replace(' ', '_')}_palette.png"
        )
        if path:
            if hasattr(self, 'custom_colors') and self.custom_colors:
                data = self.palette_engine.generate_palette(custom_colors=self.custom_colors, palette_name=f"Custom_{self.algo_mode_var.get()}")
            else:
                style = self.style_var.get()
                data = self.palette_engine.generate_palette(style, self.selected_palette)

            self.palette_engine.save_palette(data, path)
            messagebox.showinfo("Success", f"Palette image saved to:\n{path}")

    def get_project_data(self):
        """Returns the current state for project saving"""
        return {
            "type": "palette",
            "style": self.style_var.get(),
            "palette": self.selected_palette or ""
        }

    def load_project_data(self, data):
        if "style" in data: self.style_var.set(data["style"]); self._refresh_palette_list()
        if "palette" in data: self._select_palette(data["palette"])

    def _generate_ai_palette(self):
        """Generates a palette using AI logic from text description"""
        desc = self.entry_ai_palette.get().strip()
        if not desc:
            messagebox.showwarning("AI Palette", "Please enter a description (e.g., 'Modern Tech')")
            return

        self.btn_ai_palette.configure(state="disabled", text="⏳ AI Thinking...")

        def _task():
            return self.ai_assistant.suggest_palette(desc)

        def _on_done(result):
            self.btn_ai_palette.configure(state="normal", text="Generate with AI")

            # Display results
            self.selected_palette = result.get("name", desc)
            self.custom_colors = result.get("colors", [])  # For export
            self._update_swatches(self.custom_colors)
            self.lbl_desc.configure(
                text=result.get("description", f"AI Generated for: {desc}"),
                text_color=("#3B82F6", "#6366F1")
            )
            messagebox.showinfo("AI Palette", f"AI successfully generated a palette for '{desc}'!")

        parent = self.master
        while parent and not hasattr(parent, 'task_executor'):
            parent = parent.master

        if parent and hasattr(parent, 'task_executor'):
            parent.task_executor.submit_task(_task, on_complete=lambda r: self.after(0, _on_done, r.result))
        else:
            Thread(target=lambda: self.after(0, _on_done, _task()), daemon=True).start()
