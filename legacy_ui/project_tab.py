"""
Iconora Studio - Project Manager Tab UI
Modernized with sidebar integration.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from core.project_manager import ProjectManager
from i18n import tr, get_language

class ProjectManagerTab(ctk.CTkFrame):
    """Modernized UI for managing .iconora projects"""

    def __init__(self, parent, load_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.pm = ProjectManager()
        self.load_callback = load_callback
        self.selected_project = None
        self._build_ui()
        self._refresh_projects()

    def _build_ui(self):
        """Build the modernized project manager UI"""
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        is_en = get_language() == "en"

        # ── Left Pane: Project List ──────────────────────────────────────────
        self.list_pane = ctk.CTkScrollableFrame(self, width=380, corner_radius=0, fg_color=("gray95", "gray10"))
        self.list_pane.grid(row=0, column=0 if is_en else 1, sticky="nsew")

        ctk.CTkLabel(self.list_pane, text="📂 Project Center", font=("Segoe UI Variable Display", 26, "bold")).pack(pady=(30, 20))

        # Action: Import
        self.btn_import = ctk.CTkButton(
            self.list_pane, text="⬇️ Import External Project",
            command=self._import_project,
            height=45, corner_radius=10,
            font=("Segoe UI Variable Display", 13, "bold"),
            fg_color="transparent", border_width=1
        )
        self.btn_import.pack(fill="x", padx=20, pady=(0, 20))

        self.projects_container = ctk.CTkFrame(self.list_pane, fg_color="transparent")
        self.projects_container.pack(fill="x", padx=10)

        # ── Right Pane: Details ──────────────────────────────────────────────
        self.details_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.details_pane.grid(row=0, column=1 if is_en else 0, sticky="nsew", padx=30, pady=30)

        self._show_empty_state()

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text="Ready", font=("Segoe UI Variable Text", 10), text_color="gray")
        self.status_bar.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

    def _show_empty_state(self):
        for widget in self.details_pane.winfo_children():
            widget.destroy()
        
        container = ctk.CTkFrame(self.details_pane, fg_color="transparent")
        container.pack(expand=True)
        
        ctk.CTkLabel(container, text="📂", font=("Segoe UI Variable Display", 64)).pack()
        ctk.CTkLabel(container, text="Select a project to view details", font=("Segoe UI Variable Text", 16), text_color="gray").pack(pady=10)

    def _refresh_projects(self):
        for widget in self.projects_container.winfo_children():
            widget.destroy()

        res = self.pm.list_projects()
        if res['success']:
            projects = res['projects']
            if not projects:
                ctk.CTkLabel(self.projects_container, text="No projects found", font=("Segoe UI Variable Text", 12), text_color="gray").pack(pady=20)
                return

            for proj in projects:
                name = proj['name']
                is_selected = (self.selected_project == name)
                
                card = ctk.CTkFrame(self.projects_container, height=70, corner_radius=12, 
                                    fg_color=("white", "gray14") if not is_selected else ("#3B82F6", "#6366F1"))
                card.pack(fill="x", pady=6, padx=5)
                card.pack_propagate(False)

                btn = ctk.CTkButton(
                    card, text=f"  {name}", 
                    font=("Segoe UI Variable Text", 14, "bold"),
                    fg_color="transparent", 
                    text_color=("black", "white") if not is_selected else "white",
                    hover_color=("gray90", "gray20") if not is_selected else None,
                    anchor="w", 
                    command=lambda n=name: self._show_details(n)
                )
                btn.pack(fill="both", expand=True)
        else:
            self.status_bar.configure(text=f"Error: {res['message']}")

    def _show_details(self, name):
        self.selected_project = name
        self._refresh_projects() # Update selection highlight
        
        res = self.pm.load_project(name)
        if not res['success']: return

        for widget in self.details_pane.winfo_children():
            widget.destroy()

        data = res['data']
        content = data.get('data', {})
        
        # Header
        header = ctk.CTkFrame(self.details_pane, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(header, text=name, font=("Segoe UI Variable Display", 32, "bold")).pack(side="left")
        
        type_tag = ctk.CTkFrame(header, fg_color=("#DBEAFE", "#1E3A8A"), corner_radius=20)
        type_tag.pack(side="left", padx=20)
        ctk.CTkLabel(type_tag, text=content.get('type', 'Unknown').upper(), 
                     font=("Segoe UI Variable Text", 10, "bold"), text_color=("#1E40AF", "#93C5FD")).pack(padx=12, pady=4)

        # Info Cards
        info_container = ctk.CTkFrame(self.details_pane, fg_color=("white", "gray12"), corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        info_container.pack(fill="x", padx=0, pady=0)

        details = [
            ("🕒 Last Modified", data.get('modified', 'Unknown')[:19]),
            ("📄 Filename", f"{name}.iconora"),
            ("📁 Project Type", content.get('type', 'Unknown').title())
        ]

        for label, val in details:
            row = ctk.CTkFrame(info_container, fg_color="transparent")
            row.pack(fill="x", padx=25, pady=15)
            ctk.CTkLabel(row, text=label, font=("Segoe UI Variable Text", 13, "bold"), width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val, font=("Segoe UI Variable Text", 13), text_color="gray").pack(side="left")
            if label != details[-1][0]:
                ctk.CTkFrame(info_container, height=1, fg_color=("gray90", "gray20")).pack(fill="x", padx=25)

        # Actions
        actions = ctk.CTkFrame(self.details_pane, fg_color="transparent")
        actions.pack(side="bottom", fill="x", pady=0)

        ctk.CTkButton(
            actions, text="🚀 Open in Studio", 
            height=55, corner_radius=12,
            fg_color=("#3B82F6", "#6366F1"), hover_color=("#2563EB", "#4F46E5"),
            font=("Segoe UI Variable Display", 16, "bold"), 
            command=self._load_selected
        ).pack(fill="x", pady=(0, 15))

        row2 = ctk.CTkFrame(actions, fg_color="transparent")
        row2.pack(fill="x")
        
        ctk.CTkButton(
            row2, text="⬆️ Export", 
            height=45, corner_radius=10,
            fg_color="transparent", border_width=1,
            command=self._export_selected
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            row2, text="🗑️ Delete Project", 
            height=45, corner_radius=10,
            fg_color="#EF4444", hover_color="#DC2626", 
            command=self._delete_selected
        ).pack(side="left", fill="x", expand=True)

    def _load_selected(self):
        if not self.selected_project: return
        res = self.pm.load_project(self.selected_project)
        if res['success'] and self.load_callback:
            if self.load_callback(res['data']['data']):
                self.status_bar.configure(text=f"✅ Loaded {self.selected_project}", text_color="#2ecc71")
            else:
                messagebox.showwarning("Incompatible", "Project type not supported by current view.")

    def _delete_selected(self):
        if not self.selected_project: return
        if messagebox.askyesno("Confirm", f"Delete project '{self.selected_project}' forever?"):
            self.pm.delete_project(self.selected_project)
            self.selected_project = None
            self._refresh_projects()
            for widget in self.details_pane.winfo_children(): widget.destroy()
            ctk.CTkLabel(self.details_pane, text="Select a project to view details", font=("Arial", 16), text_color="gray").pack(expand=True)

    def _export_selected(self):
        if not self.selected_project: return
        path = filedialog.asksaveasfilename(defaultextension=".iconora", filetypes=[("Iconora", "*.iconora")])
        if path:
            self.pm.export_project(self.selected_project, path)
            messagebox.showinfo("Export Successful", f"Project exported to:\n{path}")

    def _import_project(self):
        path = filedialog.askopenfilename(filetypes=[("Iconora", "*.iconora *.json")])
        if path:
            res = self.pm.import_project(path)
            if res['success']:
                self._refresh_projects()
                messagebox.showinfo("Imported", "Project imported successfully!")
            else:
                messagebox.showerror("Error", res['message'])
