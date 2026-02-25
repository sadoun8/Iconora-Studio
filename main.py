"""
Iconora Studio - Professional Image Conversion Tool
برنامج احترافي لتحويل الصور وتصميم الأيقونات والشعارات

Version: 1.0.0 (Phase 1)
Author: Design Team
License: MIT
"""

import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """نقطة الدخول الرئيسية للتطبيق"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
