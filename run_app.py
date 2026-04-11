#!/usr/bin/env python
"""
بسيط لتشغيل Iconora Studio
Simple launcher for Iconora Studio
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

if __name__ == "__main__":
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق / Error running application: {e}")
        import traceback
        traceback.print_exc()
