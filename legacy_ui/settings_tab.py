"""
Iconora Studio - Settings Tab
App preferences: theme, language, export paths, quality defaults.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os, json
from pathlib import Path
from config import ICONORA_DOCS, EXPORT_SUBDIRS, PROJECTS_DIR
from core.ai_assistant import AIAssistant

SETTINGS_FILE = ICONORA_DOCS / "settings.json"

_DEFAULTS = {
    "theme": "dark",
    "language": "en",
    "default_quality": 95,
    "auto_open_folder": False,
    "export_dir_icons":      str(EXPORT_SUBDIRS["Icons"]),
    "export_dir_svgs":       str(EXPORT_SUBDIRS["SVGs"]),
    "export_dir_logos":      str(EXPORT_SUBDIRS["Logos"]),
    "export_dir_signatures": str(EXPORT_SUBDIRS["Signatures"]),
    "export_dir_palettes":   str(EXPORT_SUBDIRS["Palettes"]),
    "projects_dir":          str(PROJECTS_DIR),
    "ai_enabled":           True,
    "ai_endpoint":          "http://127.0.0.1:11434",
    "ai_model":             "qwen2.5:7b-instruct",
    "ai_timeout":           30,
}


def load_settings() -> dict:
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {**_DEFAULTS, **data}
    except Exception:
        pass
    return dict(_DEFAULTS)


def save_settings(data: dict):
    ICONORA_DOCS.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


from i18n import tr, get_language

class SettingsTab(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.settings = load_settings()
        self._dir_map: dict = {}
        self._build_ui()

    # ------------------------------------------------------------------ build
    def _build_ui(self):
        is_rtl = get_language() == "ar"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Left column: Appearance ──────────────────────────────────────────
        left = ctk.CTkScrollableFrame(self)
        left.grid(row=0, column=0 if not is_rtl else 1, sticky="nsew", padx=6, pady=0)

        ctk.CTkLabel(left, text=tr("tab_settings"), font=("Segoe UI Variable Display", 24, "bold")).pack(pady=(20, 10))

        self._section(left, tr("settings_appearance_mode"))
        self.theme_var = ctk.StringVar(value=self.settings.get("theme", "dark"))
        ctk.CTkSegmentedButton(left, values=["dark", "light", "system"],
                               variable=self.theme_var, height=40).pack(fill="x", padx=16, pady=4)

        self._sep(left)

        self._section(left, tr("settings_app_language"))
        self.lang_var = ctk.StringVar(value=self.settings.get("language", "en"))
        ctk.CTkSegmentedButton(left, values=["en", "ar"],
                               variable=self.lang_var, height=40).pack(fill="x", padx=16, pady=4)

        self._sep(left)

        self._section(left, tr("settings_export_quality"))
        self.lbl_q = ctk.CTkLabel(left, text=f"{self.settings['default_quality']} %", font=("Segoe UI Variable Text", 11, "bold"))
        self.lbl_q.pack(anchor="w" if not is_rtl else "e", padx=16)
        self.q_slider = ctk.CTkSlider(left, from_=50, to=100,
                                      command=lambda v: self.lbl_q.configure(text=f"{int(v)} %"))
        self.q_slider.set(self.settings["default_quality"])
        self.q_slider.pack(fill="x", padx=16, pady=4)

        self._sep(left)

        self.auto_open_var = tk.BooleanVar(value=self.settings.get("auto_open_folder", False))
        ctk.CTkCheckBox(left, text=tr("settings_auto_open"),
                        variable=self.auto_open_var, font=("Segoe UI Variable Text", 12)).pack(anchor="w" if not is_rtl else "e", padx=20, pady=10)

        self._sep(left)

        self._section(left, tr("settings_ai_section"))
        self.ai_enabled_var = tk.BooleanVar(value=bool(self.settings.get("ai_enabled", True)))
        ctk.CTkCheckBox(
            left,
            text=tr("settings_ai_enable"),
            variable=self.ai_enabled_var,
            font=("Segoe UI Variable Text", 12)
        ).pack(anchor="w" if not is_rtl else "e", padx=20, pady=(4, 8))

        ctk.CTkLabel(left, text=tr("settings_ai_endpoint"), font=("Segoe UI Variable Text", 11)).pack(anchor="w" if not is_rtl else "e", padx=16)
        self.ai_endpoint_entry = ctk.CTkEntry(left, height=34)
        self.ai_endpoint_entry.insert(0, self.settings.get("ai_endpoint", "http://127.0.0.1:11434"))
        self.ai_endpoint_entry.pack(fill="x", padx=16, pady=(2, 8))

        ctk.CTkLabel(left, text=tr("settings_ai_model"), font=("Segoe UI Variable Text", 11)).pack(anchor="w" if not is_rtl else "e", padx=16)
        self.ai_model_entry = ctk.CTkEntry(left, height=34)
        self.ai_model_entry.insert(0, self.settings.get("ai_model", "qwen2.5:7b-instruct"))
        self.ai_model_entry.pack(fill="x", padx=16, pady=(2, 8))

        ctk.CTkLabel(left, text=tr("settings_ai_timeout"), font=("Segoe UI Variable Text", 11)).pack(anchor="w" if not is_rtl else "e", padx=16)
        self.ai_timeout_entry = ctk.CTkEntry(left, height=34)
        self.ai_timeout_entry.insert(0, str(self.settings.get("ai_timeout", 30)))
        self.ai_timeout_entry.pack(fill="x", padx=16, pady=(2, 8))

        ctk.CTkButton(
            left,
            text="🔎 " + tr("settings_ai_test"),
            fg_color="transparent",
            border_width=1,
            height=36,
            command=self._test_ai_backend,
        ).pack(fill="x", padx=16, pady=(4, 8))

        self._sep(left)

        self._section(left, tr("settings_resources"))
        ctk.CTkButton(
            left, text="📥 " + tr("settings_get_fonts"),
            fg_color="transparent", border_width=1,
            height=36, font=("Segoe UI Variable Text", 12),
            command=lambda: os.startfile("https://fonts.google.com/?subset=arabic")
        ).pack(fill="x", padx=16, pady=5)

        self._sep(left)

        self._section(left, tr("settings_about"))
        from config import APP_VERSION, APP_PHASE
        ctk.CTkLabel(
            left, justify="left" if not is_rtl else "right", text_color="gray",
            font=("Segoe UI Variable Text", 11),
            text=(
                f"Version {APP_VERSION} ({APP_PHASE})\n"
                f"{tr('app_description_brief')}\n"
                "Built with Python & CustomTkinter."
            )
        ).pack(anchor="w" if not is_rtl else "e", padx=16, pady=4)

        # ── Right column: Export Folders ─────────────────────────────────────
        right = ctk.CTkScrollableFrame(self)
        right.grid(row=0, column=1 if not is_rtl else 0, sticky="nsew", padx=6, pady=0)

        ctk.CTkLabel(right, text=tr("settings_storage_paths"), font=("Segoe UI Variable Display", 20, "bold")).pack(pady=(20, 10))

        folder_keys = [
            (tr("tab_icon_converter"),      "export_dir_icons"),
            (tr("tab_svg_converter"),       "export_dir_svgs"),
            (tr("tab_logo_designer"),       "export_dir_logos"),
            (tr("tab_signature_generator"), "export_dir_signatures"),
            (tr("tab_palette_generator"),   "export_dir_palettes"),
            (tr("tab_projects"),            "projects_dir"),
        ]
        for label, key in folder_keys:
            self._folder_row(right, label, key)

        self._sep(right)

        ctk.CTkButton(
            right, text=tr("settings_open_data_dir"),
            fg_color="transparent", border_width=1,
            height=40,
            command=lambda: os.startfile(str(ICONORA_DOCS))
        ).pack(fill="x", padx=16, pady=10)

        # ── Bottom bar ───────────────────────────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=15)

        side = "left" if not is_rtl else "right"

        ctk.CTkButton(bar, text="💾 " + tr("btn_save_project"), width=220, height=50,
                      font=("Segoe UI Variable Display", 14, "bold"),
                      corner_radius=12,
                      command=self._save, fg_color=("#3B82F6", "#6366F1"), hover_color=("#2563EB", "#4F46E5")).pack(side=side, padx=12)

        ctk.CTkButton(bar, text="🔄 " + tr("btn_reset_page"), width=180, height=50,
                      fg_color="transparent", border_width=1,
                      corner_radius=12,
                      command=self._restore).pack(side=side, padx=4)


    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _section(parent, text):
        ctk.CTkLabel(parent, text=text, font=("Arial", 11, "bold")).pack(
            anchor="w", padx=16, pady=(14, 2))

    @staticmethod
    def _sep(parent):
        ctk.CTkFrame(parent, height=1,
                     fg_color=("gray80", "gray25")).pack(fill="x", padx=16, pady=10)

    def _folder_row(self, parent, label: str, key: str):
        ctk.CTkLabel(parent, text=label, font=("Arial", 11)).pack(
            anchor="w", padx=16, pady=(10, 0))
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=3)
        entry = ctk.CTkEntry(row, height=34)
        entry.insert(0, self.settings.get(key, ""))
        entry.pack(side="left", expand=True, fill="x")
        ctk.CTkButton(
            row, text="...", width=36, height=34,
            command=lambda k=key, e=entry: self._browse(k, e)
        ).pack(side="left", padx=3)
        self._dir_map[key] = entry

    def _browse(self, key, entry):
        folder = filedialog.askdirectory(initialdir=entry.get() or str(ICONORA_DOCS))
        if folder:
            entry.delete(0, "end")
            entry.insert(0, folder)

    # --------------------------------------------------------------- actions
    def _collect(self) -> dict:
        d = dict(self.settings)
        d["theme"]            = self.theme_var.get()
        d["language"]         = self.lang_var.get()
        d["default_quality"]  = int(self.q_slider.get())
        d["auto_open_folder"] = self.auto_open_var.get()
        d["ai_enabled"]       = self.ai_enabled_var.get()
        d["ai_endpoint"]      = self.ai_endpoint_entry.get().strip() or "http://127.0.0.1:11434"
        d["ai_model"]         = self.ai_model_entry.get().strip() or "qwen2.5:7b-instruct"
        try:
            d["ai_timeout"] = max(5, int(self.ai_timeout_entry.get().strip() or "30"))
        except Exception:
            d["ai_timeout"] = 30
        for k, e in self._dir_map.items():
            d[k] = e.get()
        return d

    def _test_ai_backend(self):
        endpoint = self.ai_endpoint_entry.get().strip() or "http://127.0.0.1:11434"
        model = self.ai_model_entry.get().strip() or "qwen2.5:7b-instruct"
        try:
            timeout = max(5, int(self.ai_timeout_entry.get().strip() or "30"))
        except Exception:
            timeout = 30

        ai = AIAssistant(endpoint=endpoint, model=model, timeout=timeout)
        ai.enabled = self.ai_enabled_var.get()

        if ai.is_backend_available():
            messagebox.showinfo("AI", tr("msg_ai_backend_ok"))
        else:
            messagebox.showwarning("AI", tr("msg_ai_backend_fail"))

    def _save(self):
        data = self._collect()
        save_settings(data)
        try:
            import customtkinter as ctk2
            ctk2.set_appearance_mode(data["theme"])
        except Exception:
            pass
        messagebox.showinfo(
            "Settings Saved",
            "Settings saved successfully!\nLanguage changes take effect on restart."
        )

    def _restore(self):
        if not messagebox.askyesno("Restore Defaults",
                                   "Reset all settings to their default values?"):
            return
        self.settings = dict(_DEFAULTS)
        save_settings(self.settings)
        for w in self.winfo_children():
            w.destroy()
        self._dir_map.clear()
        self._build_ui()
        messagebox.showinfo("Restored", "Default settings have been restored.")
