"""
Iconora Studio - Signature Gallery Dialog
Browse and reuse saved signatures.
"""
import customtkinter as ctk
import os
import json
from PIL import Image
from i18n import tr, get_language
from config import EXPORT_SUBDIRS

class SignatureLibraryDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.title(tr("sig_gallery_title"))
        self.geometry("900x600")
        self.callback = callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        ctk.CTkLabel(hdr, text=tr("sig_gallery_title"), font=("Segoe UI Variable Display", 24, "bold")).pack(side="left")

        # Search
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(hdr, placeholder_text="Search...", width=250, textvariable=self.search_var)
        self.search_entry.pack(side="right")
        self.search_var.trace_add("write", lambda *args: self._refresh_grid())

        # Scrollable area
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=("gray90", "gray15"))
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Load data
        self.library_data = []
        self._load_library()
        self._refresh_grid()

    def _load_library(self):
        lib_path = EXPORT_SUBDIRS["Signatures"] / "library.json"
        if lib_path.exists():
            try:
                with open(lib_path, "r", encoding="utf-8") as f:
                    self.library_data = json.load(f)
            except Exception:
                self.library_data = []

    def _refresh_grid(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        search_query = self.search_var.get().lower()

        # Grid settings
        cols = 3
        current_row = 0
        current_col = 0

        filtered_items = [item for item in self.library_data if search_query in item["name"].lower()]

        if not filtered_items:
            ctk.CTkLabel(self.scroll, text="No signatures found.").pack(pady=40)
            return

        for item in reversed(filtered_items): # Show newest first
            card = ctk.CTkFrame(self.scroll, fg_color=("white", "gray20"), corner_radius=10, border_width=1, border_color=("gray80", "gray30"))
            card.grid(row=current_row, column=current_col, padx=10, pady=10, sticky="nsew")

            # Preview Image
            preview_name = f"lib_{item['name'].lower().replace(' ', '_')}.png"
            preview_path = EXPORT_SUBDIRS["Signatures"] / preview_name

            if preview_path.exists():
                try:
                    p_img = Image.open(preview_path)
                    # Resize for preview
                    p_img.thumbnail((240, 100), Image.Resampling.LANCZOS)
                    ctk_img = ctk.CTkImage(light_image=p_img, dark_image=p_img, size=p_img.size)
                    lbl_img = ctk.CTkLabel(card, image=ctk_img, text="")
                    lbl_img.image = ctk_img
                    lbl_img.pack(pady=10, padx=10)
                except Exception:
                    ctk.CTkLabel(card, text="[No Preview]").pack(pady=20)
            else:
                ctk.CTkLabel(card, text="[No Preview]").pack(pady=20)

            # Info
            ctk.CTkLabel(card, text=item["name"], font=("Segoe UI Variable Text", 14, "bold")).pack()
            ctk.CTkLabel(card, text=item.get("title", ""), font=("Segoe UI Variable Text", 10), text_color="gray").pack()

            # Use Button
            btn = ctk.CTkButton(card, text="Load & Edit", height=30, fg_color=("#3B82F6", "#6366F1"),
                               command=lambda i=item: self._use_signature(i))
            btn.pack(pady=10, padx=20, fill="x")

            # Delete Button
            del_btn = ctk.CTkButton(card, text="🗑", width=30, height=30, fg_color="transparent", text_color="red",
                                   command=lambda i=item: self._delete_signature(i))
            del_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

            current_col += 1
            if current_col >= cols:
                current_col = 0
                current_row += 1

        # Configure columns
        for i in range(cols):
            self.scroll.grid_columnconfigure(i, weight=1)

    def _use_signature(self, item):
        if self.callback:
            self.callback(item)
        self.destroy()

    def _delete_signature(self, item):
        from tkinter import messagebox
        if messagebox.askyesno(tr("msg_confirm"), f"Delete '{item['name']}' from library?"):
            try:
                self.library_data.remove(item)
                # Update file
                lib_path = EXPORT_SUBDIRS["Signatures"] / "library.json"
                with open(lib_path, "w", encoding="utf-8") as f:
                    json.dump(self.library_data, f, indent=4, ensure_ascii=False)

                # Also delete preview if possible
                preview_name = f"lib_{item['name'].lower().replace(' ', '_')}.png"
                preview_path = EXPORT_SUBDIRS["Signatures"] / preview_name
                if preview_path.exists():
                    try:
                        os.remove(preview_path)
                    except Exception:
                        pass

                self._refresh_grid()
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Error", f"Failed to delete: {e}")
