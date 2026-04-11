import traceback
from ui.main_window import MainWindow

try:
    win = MainWindow()
    print("Created MainWindow successfully")
except Exception as e:
    traceback.print_exc()
