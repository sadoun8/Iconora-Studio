"""Iconora Studio - Professional Design Suite
Main application window with modern sidebar navigation.
"""
from __future__ import annotations

import os
import sys
import traceback
import tkinter as tk
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ── State ─────────────────────────────────────────────────────────────────────
_IMPORT_ERROR = None
_USE_CTK      = False

# ── Localisation ──────────────────────────────────────────────────────────────
try:
    from i18n import tr, set_language, get_language, TRANSLATIONS
except ImportError as e:
    _IMPORT_ERROR = f"Localisation Error: {e}"
    TRANSLATIONS  = {}
    def tr(k, **kw): return k
    def set_language(l): pass

# ── CustomTkinter ─────────────────────────────────────────────────────────────
try:
    import customtkinter as ctk
    _USE_CTK = True
    import config
except Exception as e:
    _USE_CTK = False
    _IMPORT_ERROR = _IMPORT_ERROR or f"CustomTkinter Error: {e}"

# ── Tab Imports ───────────────────────────────────────────────────────────────
TABS_AVAILABLE = True # Always True now, we load them lazily

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
PAGE_MAP = {
    "icon":     "ui.icon_tab.IconConverterTab",
    "svg":      "ui.svg_tab.SVGConverterTab",
    "logo":     "ui.logo_tab.LogoDesignerTab",
    "sig":      "ui.signature_tab.SignatureTab",
    "pal":      "ui.palette_tab.PaletteTab",
    "proj":     "ui.project_tab.ProjectManagerTab",
    "settings": "ui.settings_tab.SettingsTab",
}

NAV_ITEMS = [
    ("tab_icon_converter",       "📦",  "icon"),
    ("tab_svg_converter",        "✨",  "svg"),
    ("tab_logo_designer",        "🎯",  "logo"),
    ("tab_signature_generator",  "✍️",  "sig"),
    ("tab_palette_generator",    "🎨",  "pal"),
    ("tab_projects",             "📁",  "proj"),
    ("tab_settings",             "⚙️",  "settings"),
]


class MainWindow:

    def __init__(self) -> None:
        self.root = ctk.CTk() if _USE_CTK else tk.Tk()
        self.root.title("🎨  Iconora Studio")
        self.root.geometry("1200x780")
        self.root.minsize(980, 640)

        from core.task_executor import TaskExecutor
        self.task_executor = TaskExecutor(max_workers=4)

        if _USE_CTK:
            theme_path = os.path.join(project_root, "assets", "premium_theme.json")
            try:
                if os.path.exists(theme_path):
                    ctk.set_default_color_theme(theme_path)
                ctk.set_appearance_mode("dark")
            except Exception:
                try:
                    ctk.set_default_color_theme("blue")
                except Exception:
                    pass

        self.current_page    = None
        self.nav_buttons: dict[str, object] = {}
        self._active_key     = ""
        self.pages_cache     = {}
        self._is_loading     = False

        self._fix_arabic_clipboard()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        """Graceful shutdown to prevent background-thread leaks."""
        try:
            if hasattr(self, "task_executor") and self.task_executor:
                self.task_executor.shutdown(wait=False)
        except Exception:
            pass
        self.root.destroy()

    # ─── Clipboard Fix ────────────────────────────────────────
    def _fix_arabic_clipboard(self):
        """Forces handling of Ctrl+C/V/X/A regardless of keyboard layout language (e.g., Arabic)."""
        def on_key(event):
            # Check if Control is pressed (state 4 on Windows, or 12 with NumLock, etc.)
            if event.state & 0x0004:
                # If the keysym is already valid for English bindings, let Tkinter handle it to avoid double execution
                if getattr(event, 'keysym', '').lower() in ['c', 'v', 'x', 'a']:
                    return

                # 67=C, 86=V, 88=X, 65=A (These are physical keycodes that don't change with language)
                if event.keycode == 67: # Ctrl+C
                    try: event.widget.event_generate("<<Copy>>")
                    except Exception:
                        pass
                    return "break"
                elif event.keycode == 86: # Ctrl+V
                    try: event.widget.event_generate("<<Paste>>")
                    except Exception:
                        pass
                    return "break"
                elif event.keycode == 88: # Ctrl+X
                    try: event.widget.event_generate("<<Cut>>")
                    except Exception:
                        pass
                    return "break"
                elif event.keycode == 65: # Ctrl+A
                    try:
                        event.widget.select_range(0, 'end')
                        event.widget.icursor('end')
                    except Exception:
                        pass
                    return "break"
        if getattr(self, "root", None):
            self.root.bind_all("<Key>", on_key, add="+")

    # ─── Build UI ─────────────────────────────────────────────
    def _build_ui(self) -> None:
        try:
            if _USE_CTK and TABS_AVAILABLE:
                self._build_modern_ui()
            else:
                self._build_fallback_ui()
        except Exception as e:
            traceback.print_exc()
            self._build_fallback_ui(f"UI Error: {e}")

    def _build_fallback_ui(self, custom_msg=None) -> None:
        for child in list(self.root.children.values()):
            try: child.destroy()
            except Exception:
                pass
        container = tk.Frame(self.root, bg="#f1f5f9")
        container.pack(fill="both", expand=True)
        tk.Label(container, text="Iconora Studio — Recovery Mode",
                 font=("Arial", 22, "bold"), bg="#f1f5f9").pack(pady=30)
        msg = custom_msg or _IMPORT_ERROR or "Unknown Error"
        tk.Label(container, text=f"Details:\n{msg}", fg="#ef4444", font=("Courier", 10),
                 wraplength=700, justify="left", bg="#ffffff", padx=20, pady=20,
                 borderwidth=1, relief="solid").pack(pady=20)
        tk.Label(container, text="Fix: pip install -r requirements.txt", bg="#f1f5f9").pack()
        tk.Button(container, text="Close", command=self.root.quit, height=2, width=16).pack(pady=20)

    def _build_modern_ui(self) -> None:
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True)

        is_rtl       = get_language() == "ar"
        sidebar_side = "right" if is_rtl else "left"

        # ── Sidebar ──
        sidebar = ctk.CTkFrame(container, width=230, corner_radius=0, fg_color=config.COLOR_BG_SECONDARY)
        sidebar.pack(side=sidebar_side, fill="y")
        sidebar.pack_propagate(False)

        # Logo header
        hdr = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=0)
        hdr.pack(fill="x", pady=(20, 10))

        # Add a subtle gradient-like look with a label or just a better styled one
        ctk.CTkLabel(hdr, text="🎨", font=("Arial", 32)).pack()
        ctk.CTkLabel(hdr, text="Iconora Studio",
                     font=("Segoe UI Variable Display", 20, "bold")).pack(pady=(5, 10))

        # Nav buttons
        nav_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_container.pack(fill="both", expand=True, pady=10)

        for tr_key, icon, key in NAV_ITEMS:
            label = tr(tr_key)
            btn = ctk.CTkButton(
                nav_container,
                text=f"  {icon}   {label}",
                anchor="w" if not is_rtl else "e",
                fg_color="transparent",
                hover_color=("gray85", "gray20"),
                text_color=("gray20", "gray95"),
                height=48,
                corner_radius=12,
                font=("Segoe UI Variable Text", 13, "normal"),
                command=lambda k=key: self._show(k),
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.nav_buttons[key] = btn

        # Language switcher and Reset at the very bottom
        bottom = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=12, pady=16)

        # Bottom Frame for Reset & Save
        action_frame = ctk.CTkFrame(bottom, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 10))

        self.btn_reset = ctk.CTkButton(
            action_frame,
            text=tr("btn_reset_page"),
            command=self._reset_current_page,
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="white",
            height=30
        )
        self.btn_reset.pack(fill="x", pady=5)

        self.btn_save_proj = ctk.CTkButton(
            action_frame,
            text=tr("btn_save_project"),
            command=lambda: self._save_current_project(),
            fg_color="#10b981",
            hover_color="#059669",
            text_color="white",
            height=30
        )
        self.btn_save_proj.pack(fill="x", pady=5)

        lang_btn = ctk.CTkSegmentedButton(bottom, values=["العربية", "English"],
                                          command=self._change_language)
        lang_btn.set("العربية" if is_rtl else "English")
        lang_btn.pack(fill="x")

        # ── Content area ──
        self.content = ctk.CTkFrame(container, fg_color="transparent")
        self.content.pack(side="right" if is_rtl else "left", fill="both", expand=True,
                          padx=16, pady=16)

        # Show default page
        self._show("icon")

    @staticmethod
    def _special_label(tr_key: str) -> str:
        labels = {
            "__projects__": "Projects",
            "__settings__": "Settings",
        }
        return labels.get(tr_key, tr_key)

    # ─── Navigation ───────────────────────────────────────────
    def _save_current_project(self):
        try:
            from core.project_manager import ProjectManager
            import tkinter.simpledialog as simpledialog
            from tkinter import messagebox

            pm = ProjectManager()
            data = None
            current_page = self.current_page

            if hasattr(current_page, 'get_project_data'):
                data = current_page.get_project_data()
            else:
                # Fallback for older tabs or specific logic
                if self._active_key == "logo" and hasattr(current_page, 'entry_text'):
                    data = {
                        'type': 'logo_designer',
                        'text': current_page.entry_text.get() if hasattr(current_page.entry_text, 'get') else "",
                        'style': current_page.style_var.get(),
                        'layout': current_page.layout_var.get(),
                        'font_size': int(current_page.size_slider.get()),
                        'color1': current_page._rgb_to_hex(current_page.color1),
                        'color2': current_page._rgb_to_hex(current_page.color2),
                        'icon_path': current_page.icon_path or ""
                    }
                elif self._active_key == "pal" and hasattr(current_page, 'style_var'):
                    data = {
                        'type': 'palette',
                        'style': current_page.style_var.get(),
                        'palette': current_page.selected_palette or ""
                    }
                elif self._active_key == "sig" and hasattr(current_page, 'entry_name'):
                    data = {
                        'type': 'signature',
                        'name': current_page.entry_name.get(),
                        'title': current_page.entry_title.get(),
                        'color': current_page._rgb_to_hex(current_page.ink_color),
                        'font_size': int(current_page.font_size_slider.get()) # Fixed from font_size to font_size_slider
                    }

            if not data:
                messagebox.showinfo("Info", "Saving not supported for this view yet.")
                return

            name = simpledialog.askstring(tr("btn_save_project"), tr("project_name") + ":")
            if name:
                res = pm.save_project(name, data)
                if res['success']:
                    messagebox.showinfo("Saved", f"Project '{name}' saved successfully!")
                else:
                    messagebox.showerror("Error", res['message'])
        except Exception as e:
            traceback.print_exc()
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to save project: {e}")

    def _show(self, key: str):
        if self._is_loading: return

        # Highlight active button
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=config.COLOR_ACCENT,
                              text_color="white",
                              font=("Segoe UI Variable Display", 13, "bold"))
            else:
                btn.configure(fg_color="transparent",
                              text_color=("gray20", "gray95"),
                              font=("Segoe UI Variable Text", 13, "normal"))

        self._active_key = key

        # Hide current contents
        for w in self.content.winfo_children():
            w.pack_forget()

        # Instantiate tab
        if key not in self.pages_cache:
            self._is_loading = True

            # Show a simple loading indicator
            load_label = ctk.CTkLabel(self.content, text="⚡ Loading Component...", font=("Arial", 16))
            load_label.pack(expand=True)
            self.root.update_idletasks()

            def _async_load():
                try:
                    import importlib
                    module_path, class_name = PAGE_MAP[key].rsplit(".", 1)
                    module = importlib.import_module(module_path)
                    cls = getattr(module, class_name)

                    if key == "proj":
                        page = cls(self.content, load_callback=self._load_project)
                    else:
                        page = cls(self.content)

                    return page
                except Exception as e:
                    traceback.print_exc()
                    return e

            def _on_load_done(result):
                self._is_loading = False
                load_label.destroy()

                if isinstance(result, Exception):
                    err = ctk.CTkLabel(self.content, text=f"⚠ Error loading page:\n{result}",
                                       text_color="red", wraplength=700)
                    err.pack(pady=40)
                else:
                    self.pages_cache[key] = result
                    self._display_page(key)

            self.task_executor.submit_task(_async_load, on_complete=lambda r: self.root.after(0, _on_load_done, r.result))
        else:
            self._display_page(key)

    def _display_page(self, key: str):
        page = self.pages_cache[key]
        page.pack(fill="both", expand=True)
        self.current_page = page

    def _reset_current_page(self):
        if self._active_key and self._active_key in self.pages_cache:
            page = self.pages_cache[self._active_key]
            if hasattr(page, 'cleanup'):
                page.cleanup()
            page.destroy()
            del self.pages_cache[self._active_key]
        self._show(self._active_key)

    def _make_page(self, key: str):
        # This is now handled in _show's async loader
        pass

    # ─── Language ─────────────────────────────────────────────
    def _change_language(self, label: str):
        new_lang = "ar" if label == "العربية" else "en"
        if new_lang != get_language():
            set_language(new_lang)
            for w in self.root.winfo_children():
                w.destroy()
            self._build_ui()

    # ─── Project Loading ──────────────────────────────────────
    def _load_project(self, data: dict) -> bool:
        type_map = {
            "icon_converter": "icon",
            "svg_converter":  "svg",
            "logo_designer":  "logo",
            "signature":      "sig",
            "palette":        "pal",
        }
        key = type_map.get(data.get("type"))
        if key:
            self._show(key)
            if hasattr(self.current_page, "load_project_data"):
                self.current_page.load_project_data(data)
                return True
        return False

    def run(self):
        self.root.mainloop()
