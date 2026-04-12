"""
Iconora Studio - Professional Image Conversion Tool
برنامج احترافي لتحويل الصور وتصميم الأيقونات والشعارات

Version: 1.2.0 (Phase 6)
Author: Design Team
License: MIT
"""

import sys
import os

# إضافة مسار المشروع والمكتبات الخاصة بالمستخدم
import site
root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.append(user_site)

from legacy_ui.main_window import MainWindow



def main():
    """نقطة الدخول الرئيسية للتطبيق"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
