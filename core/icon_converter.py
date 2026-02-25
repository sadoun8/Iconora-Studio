"""
Icon Converter Module
تحويل الصور إلى ICO بأحجام متعددة

Professional icon conversion with comprehensive error handling
"""

from PIL import Image
import os
from pathlib import Path
from i18n import tr


class IconConverter:
    """تحويل الصور إلى أيقونات بأحجام متعددة"""

    # أحجام أيقونات Windows القياسية
    STANDARD_SIZES = [
        (16, 16),
        (24, 24),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ]

    def __init__(self, input_image_path: str):
        """
        Initialize IconConverter

        Args:
            input_image_path: مسار الصورة المراد تحويلها
        """
        self.input_path = input_image_path
        self.image = None
        self.load_image()

    def load_image(self):
        """تحميل الصورة / Load image"""
        try:
            self.image = Image.open(self.input_path)
            # تحويل إلى RGBA للشفافية / Convert to RGBA for transparency
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
            return True
        except Exception as e:
            raise Exception(f"{tr('msg_load_error')}{e}")

    def resize_image(self, size: tuple) -> Image.Image:
        """
        تغيير حجم الصورة مع الحفاظ على النسبة
        Resize image while keeping aspect ratio

        Args:
            size: الحجم المطلوب / Desired size (width, height)

        Returns:
            Image.Image: الصورة المعدلة / Resized image
        """
        img = self.image.copy()
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # إنشاء صورة جديدة بالحجم الدقيق مع خلفية شفافة
        # Create new image with exact size and transparent background
        new_image = Image.new('RGBA', size, (0, 0, 0, 0))
        offset = (
            (size[0] - img.size[0]) // 2,
            (size[1] - img.size[1]) // 2
        )
        new_image.paste(img, offset, img)
        return new_image

    def convert_to_ico(self, output_path: str, sizes: list = None):
        """
        تحويل الصورة إلى ملف ICO

        Convert image to ICO file

        Args:
            output_path: مسار الملف الناتج / Output file path
            sizes: قائمة الأحجام المطلوبة / List of desired sizes (optional)
        """
        if sizes is None:
            sizes = self.STANDARD_SIZES

        # إعداد الصور بالأحجام المختلفة / Prepare images in different sizes
        icon_images = [self.resize_image(size) for size in sizes]

        try:
            # حفظ كـ ICO / Save as ICO
            icon_images[0].save(
                output_path,
                format='ICO',
                sizes=sizes
            )
            return True, f"{tr('msg_saved_ico')}{output_path}"
        except Exception as e:
            return False, f"{tr('msg_save_error')}{e}"

    def export_all_sizes(self, output_dir: str, base_name: str = "icon"):
        """
        تصدير جميع الأحجام كصور PNG منفصلة

        Export all sizes as separate PNG images

        Args:
            output_dir: مجلد الحفظ / Output directory
            base_name: اسم الملف الأساسي / Base filename
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = []

        for size in self.STANDARD_SIZES:
            resized = self.resize_image(size)
            filename = f"{base_name}_{size[0]}x{size[1]}.png"
            filepath = os.path.join(output_dir, filename)

            try:
                resized.save(filepath)
                results.append((True, tr("msg_saved_file", filename=filename)))
            except Exception as e:
                results.append((False, tr("msg_error_in", filename=filename, error=str(e))))

        return results

    def get_image_info(self):
        """الحصول على معلومات الصورة / Get image information"""
        return {
            'size': self.image.size,
            'mode': self.image.mode,
            'format': self.image.format
        }

    def generate_ico_multi_resolution(self, output_path: str):
        """
        إنشاء ملف ICO واحد يحتوي على جميع الأحجام
        Create a single ICO file containing all sizes
        (ميزة احترافية / Professional feature)
        """
        return self.convert_to_ico(output_path, self.STANDARD_SIZES)
