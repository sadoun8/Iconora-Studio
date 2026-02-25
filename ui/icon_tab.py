"""
Icon Converter Tab (Enhanced)
تبويب تحويل الأيقونات مع معاينة مباشرة

Enhanced icon conversion with live preview and progress tracking
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path
from threading import Thread
from core.icon_converter import IconConverter
from i18n import tr


class IconTab(ctk.CTkFrame):
    """Enhanced Icon Converter Tab with live preview"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.selected_image = None
        self.converter = None
        self.tk_image = None
        self.is_converting = False

        # إعداد الواجهة / Setup UI
        self.setup_ui()

    def setup_ui(self):
        """إعداد واجهة المستخدم / Setup user interface"""

        # ========== صف الأزرار العلوية ==========
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=15, pady=10)

        self.btn_select = ctk.CTkButton(
            button_frame,
            text="📁 " + tr("btn_select_image"),
            command=self.choose_image,
            width=150,
            height=35
        )
        self.btn_select.pack(side="left", padx=5)

        self.btn_convert = ctk.CTkButton(
            button_frame,
            text="💾 " + tr("btn_save_ico"),
            command=self.convert_icon,
            width=150,
            height=35,
            state="disabled"
        )
        self.btn_convert.pack(side="left", padx=5)

        export_btn = ctk.CTkButton(
            button_frame,
            text="📤 " + tr("btn_save_png"),
            command=self.export_png,
            width=150,
            height=35,
            state="disabled"
        )
        export_btn.pack(side="left", padx=5)
        self.export_btn = export_btn

        # ========== قسم المعاينة والخيارات ==========
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # القسم الأيسر - المعاينة / Left side - Preview
        preview_frame = ctk.CTkFrame(content_frame)
        preview_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        preview_title = ctk.CTkLabel(
            preview_frame,
            text=tr("lbl_image_preview"),
            font=("Arial", 14, "bold")
        )
        preview_title.pack(anchor="w", pady=(0, 10))

        self.preview_canvas = ctk.CTkLabel(
            preview_frame,
            text=tr("msg_no_image_selected"),
            width=350,
            height=280,
            fg_color="#2b2b2b",
            corner_radius=10
        )
        self.preview_canvas.pack(fill="both", expand=True, pady=(0, 10))

        # معلومات الملف / File information
        self.info_label = ctk.CTkLabel(
            preview_frame,
            text="",
            font=("Arial", 9),
            text_color="gray",
            wraplength=350
        )
        self.info_label.pack(anchor="w")

        # شريط التقدم / Progress bar
        self.progress_bar = ctk.CTkProgressBar(preview_frame)
        self.progress_bar.pack(fill="x", pady=(10, 0))
        self.progress_bar.set(0)

        # القسم الأيمن - خيارات / Right side - Options
        options_frame = ctk.CTkFrame(content_frame)
        options_frame.pack(side="right", fill="both", padx=(10, 0), pady=0)

        # عنوان الخيارات / Options title
        options_title = ctk.CTkLabel(
            options_frame,
            text=tr("select_sizes"),
            font=("Arial", 14, "bold")
        )
        options_title.pack(anchor="w", pady=(0, 15))

        # صندوق قابل للتمرير / Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(
            options_frame,
            width=200,
            height=300
        )
        scroll_frame.pack(fill="both", expand=True)

        self.size_vars = {}
        sizes = [
            ("size_16", (16, 16), True),
            ("size_24", (24, 24), True),
            ("size_32", (32, 32), True),
            ("size_48", (48, 48), True),
            ("size_64", (64, 64), False),
            ("size_128", (128, 128), False),
            ("size_256", (256, 256), True),
        ]

        for size_key, size_tuple, default in sizes:
            var = ctk.BooleanVar(value=default)
            self.size_vars[size_tuple] = var

            checkbox = ctk.CTkCheckBox(
                scroll_frame,
                text=tr(size_key),
                variable=var,
                font=("Arial", 11)
            )
            checkbox.pack(anchor="w", pady=8)

    def choose_image(self):
        """اختيار صورة من الجهاز / Choose image from system"""
        types = [
            (tr("lbl_image_files"), "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
            (tr("lbl_all_files"), "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title=tr("dlg_select_image"),
            filetypes=types
        )

        if file_path:
            self.selected_image = file_path
            self.btn_convert.configure(state="normal")
            self.export_btn.configure(state="normal")

            try:
                self.converter = IconConverter(file_path)
                self.show_preview(file_path)
            except Exception as e:
                messagebox.showerror(
                    tr("lbl_error"),
                    f"{tr('msg_load_error')}{str(e)}"
                )
                self.selected_image = None
                self.btn_convert.configure(state="disabled")
                self.export_btn.configure(state="disabled")

    def show_preview(self, image_path: str):
        """عرض معاينة الصورة / Display image preview"""
        try:
            img = Image.open(image_path)
            original_size = img.size

            # تصغير الصورة للمعاينة / Resize for preview
            img.thumbnail((350, 280), Image.Resampling.LANCZOS)

            # تحويل إلى PhotoImage / Convert to PhotoImage
            self.tk_image = ImageTk.PhotoImage(img)
            self.preview_canvas.configure(image=self.tk_image, text="")

            # عرض معلومات الملف / Display file information
            file_name = os.path.basename(image_path)
            file_size = os.path.getsize(image_path) / 1024
            info_text = (
                f"{tr('lbl_filename')}: {file_name}\n"
                f"{tr('lbl_dimensions')}: {original_size[0]}×{original_size[1]}\n"
                f"{tr('lbl_size')}: {file_size:.1f} KB"
            )
            self.info_label.configure(text=info_text)

        except Exception as e:
            messagebox.showerror(
                tr("lbl_error"),
                f"{tr('msg_load_error')}{str(e)}"
            )

    def convert_icon(self):
        """تحويل الصورة إلى ICO / Convert image to ICO"""
        if not self.converter:
            messagebox.showerror(
                tr("lbl_error"),
                tr("msg_select_image_first")
            )
            return

        selected_sizes = [
            size for size, var in self.size_vars.items() if var.get()
        ]

        if not selected_sizes:
            messagebox.showerror(
                tr("lbl_error"),
                tr("msg_select_size")
            )
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".ico",
            title=tr("dlg_save_ico"),
            filetypes=[(tr("lbl_ico_files"), "*.ico")]
        )

        if save_path:
            self.is_converting = True
            self.btn_convert.configure(state="disabled")
            self.progress_bar.set(0)

            conversion_thread = Thread(
                target=self._perform_ico_conversion,
                args=(save_path, selected_sizes)
            )
            conversion_thread.daemon = True
            conversion_thread.start()

    def _perform_ico_conversion(self, save_path: str, sizes: list):
        """تنفيذ التحويل إلى ICO / Perform ICO conversion"""
        try:
            self.progress_bar.set(0.3)

            success, message = self.converter.convert_to_ico(save_path, sizes)

            self.progress_bar.set(0.8)

            if success:
                self.progress_bar.set(1.0)
                messagebox.showinfo(
                    tr("msg_success"),
                    f"{tr('msg_saved_ico')}\n{save_path}"
                )
            else:
                messagebox.showerror(tr("lbl_error"), message)

        except Exception as e:
            messagebox.showerror(
                tr("lbl_error"),
                f"{tr('msg_error_occurred')}{str(e)}"
            )

        finally:
            self.progress_bar.set(0)
            self.btn_convert.configure(state="normal")
            self.is_converting = False

    def export_png(self):
        """تصدير صور PNG منفصلة / Export separate PNG files"""
        if not self.converter:
            messagebox.showerror(
                tr("lbl_error"),
                tr("msg_select_image_first")
            )
            return

        folder = filedialog.askdirectory(
            title=tr("dlg_select_folder")
        )

        if folder:
            self.is_converting = True
            self.export_btn.configure(state="disabled")
            self.progress_bar.set(0)

            export_thread = Thread(
                target=self._perform_png_export,
                args=(folder,)
            )
            export_thread.daemon = True
            export_thread.start()

    def _perform_png_export(self, folder: str):
        """تنفيذ تصدير PNG / Perform PNG export"""
        try:
            base_name = Path(self.selected_image).stem
            self.progress_bar.set(0.2)

            results = self.converter.export_all_sizes(folder, base_name)

            self.progress_bar.set(0.9)

            successCount = sum(1 for success, _ in results if success)
            total = len(results)

            message = f"{tr('msg_exported_files')}: {successCount}/{total}\n\n"
            for success, msg in results:
                message += f"{'✅' if success else '❌'} {msg}\n"

            messagebox.showinfo(tr("msg_results"), message)

        except Exception as e:
            messagebox.showerror(
                tr("lbl_error"),
                f"{tr('msg_error_occurred')}{str(e)}"
            )

        finally:
            self.progress_bar.set(0)
            self.export_btn.configure(state="normal")
            self.is_converting = False
