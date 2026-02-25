"""
SVG Conversion Tab
علامة تبويب تحويل SVG

SVG conversion interface with preview and progress tracking
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from threading import Thread
from core.svg_converter import SVGConverter
from i18n import tr


class SVGTab(ctk.CTkFrame):
    """SVG Conversion Tab with live preview"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.svg_converter = SVGConverter()
        self.selected_image = None
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
            text="🔄 " + tr("btn_convert_svg"),
            command=self.convert_svg,
            width=150,
            height=35,
            state="disabled"
        )
        self.btn_convert.pack(side="left", padx=5)

        # ========== قسم المعاينة ==========
        preview_frame = ctk.CTkFrame(self)
        preview_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # عنوان المعاينة / Preview title
        preview_title = ctk.CTkLabel(
            preview_frame,
            text=tr("lbl_image_preview"),
            font=("Arial", 14, "bold")
        )
        preview_title.pack(anchor="w", pady=(0, 10))

        # صورة المعاينة / Preview image
        self.preview_canvas = ctk.CTkLabel(
            preview_frame,
            text=tr("msg_no_image_selected"),
            width=400,
            height=300,
            fg_color="#2b2b2b",
            corner_radius=10
        )
        self.preview_canvas.pack(fill="both", expand=True)

        # ========== شريط التقدم والمعلومات ==========
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=15, pady=10)

        # شريط التقدم / Progress bar
        self.progress_bar = ctk.CTkProgressBar(info_frame)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)

        # معلومات الملف / File information
        self.info_label = ctk.CTkLabel(
            info_frame,
            text=tr("msg_no_image_selected"),
            font=("Arial", 10),
            text_color="gray"
        )
        self.info_label.pack(anchor="w")

    def choose_image(self):
        """اختيار صورة من الجهاز / Choose image from system"""
        file_path = filedialog.askopenfilename(
            title=tr("dlg_select_image"),
            filetypes=[
                (tr("lbl_image_files"), "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                (tr("lbl_all_files"), "*.*")
            ]
        )

        if file_path:
            self.selected_image = file_path
            self.btn_convert.configure(state="normal")
            self.show_preview(file_path)

    def show_preview(self, image_path: str):
        """عرض معاينة الصورة / Display image preview"""
        try:
            img = Image.open(image_path)
            original_size = img.size

            # تصغير الصورة للمعاينة / Resize for preview
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)

            # تحويل إلى PhotoImage / Convert to PhotoImage
            self.tk_image = ImageTk.PhotoImage(img)
            self.preview_canvas.configure(image=self.tk_image, text="")

            # عرض معلومات الملف / Display file information
            file_name = os.path.basename(image_path)
            file_size = os.path.getsize(image_path) / 1024  # بالكيلوبايت
            info_text = f"{file_name} | {original_size[0]}x{original_size[1]} | {file_size:.1f} KB"
            self.info_label.configure(text=info_text)

        except Exception as e:
            messagebox.showerror(tr("lbl_error"), f"{tr('msg_load_error')}{str(e)}")

    def convert_svg(self):
        """تحويل الصورة إلى SVG / Convert image to SVG"""
        if not self.selected_image:
            messagebox.showerror(
                tr("lbl_error"),
                tr("msg_select_image_first")
            )
            return

        # تشغيل التحويل في thread منفصل / Run conversion in separate thread
        self.is_converting = True
        self.btn_convert.configure(state="disabled")
        self.progress_bar.set(0)

        conversion_thread = Thread(target=self._perform_conversion)
        conversion_thread.daemon = True
        conversion_thread.start()

    def _perform_conversion(self):
        """تنفيذ التحويل / Perform conversion"""
        try:
            self.progress_bar.set(0.25)

            # تحويل الصورة / Convert image
            success, message, output_path = self.svg_converter.convert_to_svg(
                self.selected_image
            )

            self.progress_bar.set(0.75)

            if success:
                self.progress_bar.set(1.0)
                messagebox.showinfo(
                    tr("msg_success"),
                    f"{message}\n\n{tr('msg_file_saved_at')}\n{output_path}"
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
