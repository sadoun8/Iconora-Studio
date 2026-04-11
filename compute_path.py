from pathlib import Path
import ui.main_window
p = Path(ui.main_window.__file__).parent.parent
with open('path_result.txt','w',encoding='utf-8') as f:
    f.write(str(p))
