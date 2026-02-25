# Iconora Studio - Professional Image Conversion & Design Tool

## 🎯 Project Vision

**Iconora Studio** is a professional Windows application for:
- Converting images to ICO with multiple sizes
- Converting images to SVG (Vector)
- Creating professional logos
- Generating digital signatures
- Background removal
- 3D icon design
- Multi-format export

## 🏗️ Technical Architecture

### Technologies
- **Python 3.12**
- **CustomTkinter** (Modern UI)
- **Pillow** (Image processing)
- **CairoSVG** (SVG conversion)
- **RemBG** (Background removal)
- **svgwrite** (SVG generation)
- **PyInstaller** (Build tool)

### Project Structure
```
IconoraStudio/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── build_exe.py           # Build script
│
├── core/                  # Processing engines
│   ├── icon_converter.py  # ICO conversion ✅
│   ├── svg_converter.py   # SVG conversion (coming)
│   ├── logo_engine.py     # Logo creation (coming)
│   ├── signature_engine.py # Signatures (coming)
│   └── background_remover.py # Background removal (coming)
│
├── ui/                    # User interfaces
│   ├── main_window.py     # Main window ✅
│   ├── icon_tab.py        # Icon converter tab ✅
│   ├── logo_tab.py        # Logo designer (coming)
│   ├── signature_tab.py   # Signature generator (coming)
│   └── settings_tab.py    # Settings (coming)
│
├── assets/
│   ├── fonts/             # Custom fonts
│   ├── templates/         # Ready templates
│   └── icons/             # App icons
│
└── exports/               # Output folder
```

---

## 🚀 Quick Start

### Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python main.py
```

### Build Executable
```bash
# Build to .exe file
python build_exe.py

# Result: dist/IconoraStudio.exe
```

---

## 📋 Development Roadmap

### Phase 1 ✅ – Icon Converter (Current)
- [x] Professional UI with tabs
- [x] Image to ICO conversion
- [x] Multiple sizes support
- [x] Auto export to folder
- **Result**: Professional icon conversion tool

### Phase 2 – SVG Converter (Next)
- [ ] PNG to SVG conversion
- [ ] Background transparency
- [ ] Real-time preview
- [ ] Color changing
- **Result**: Vector conversion tool

### Phase 3 – Logo Designer
- [ ] Company name input
- [ ] Font selection
- [ ] Color picker
- [ ] Gradients
- [ ] Effects (shadow, light)
- [ ] Ready icons & patterns (Minimal, Luxury, 3D)
- **Result**: Professional Logo Designer

### Phase 4 – Signature Generator
- [ ] Arabic & English signatures
- [ ] Ink effects
- [ ] Transparent PNG export
- [ ] Custom sizes
- **Result**: Digital signature tool

### Phase 5 – Advanced Tools
- [ ] Background removal (RemBG)
- [ ] 3D effect for icons
- [ ] Image compression
- [ ] Smart resizing
- [ ] Dark/Light theme toggle
- **Result**: Complete professional suite

---

## 💻 Usage Examples

### Convert Image to ICO
1. Open **Icon Converter** tab
2. Click "Select Image"
3. Choose sizes (16x16, 32x32, etc.)
4. Click "Save as ICO"
5. Choose output location

### Export Multiple Sizes
1. Select image
2. Check desired sizes
3. Click "Save PNG"
4. Get individual PNG files for each size

---

## 🎨 UI Design Features

- **Dark theme** (professional look)
- **Modern interface** with CustomTkinter
- **Responsive layout**
- **Full Arabic support**
- **Custom buttons & colors**

---

## 📦 Core Modules

### IconConverter Class
```python
from core.icon_converter import IconConverter

# Load image
converter = IconConverter("image.png")

# Convert to ICO
converter.convert_to_ico("output.ico", [(32,32), (64,64)])

# Export individual sizes
converter.export_all_sizes("output_folder/")

# Get image info
info = converter.get_image_info()
```

---

## 🔧 Adding New Features

### Example: Add SVG Tab

1. **Create engine** (`core/svg_converter.py`):
```python
class SVGConverter:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def to_svg(self, output_path):
        # Conversion logic
        pass
```

2. **Create UI tab** (`ui/svg_tab.py`):
```python
from customtkinter import CTkFrame, CTkButton
from core.svg_converter import SVGConverter

class SVGTab(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # UI setup
```

3. **Add to main window** (`ui/main_window.py`):
```python
from ui.svg_tab import SVGTab

svg_tab = tab_view.add("SVG Converter")
svg_content = SVGTab(svg_tab)
svg_content.pack(fill="both", expand=True)
```

---

## 🎯 Professional Features

| Feature | Status |
|---------|--------|
| Multi-size ICO export | ✅ Phase 1 |
| SVG conversion | 📅 Phase 2 |
| Logo creation | 📅 Phase 3 |
| Digital signatures | 📅 Phase 4 |
| Background removal | 📅 Phase 5 |
| 3D effects | 📅 Phase 5 |
| Dark/Light theme | 📅 Phase 5 |
| Project save (.iconora) | 📅 Phase 5 |

---

## 🚀 Future Monetization

- **Free version**: Image conversion only
- **Pro version**: Logos + Signatures + Background removal
- **Lifetime license**: One-time purchase
- **Annual subscription**: For updates

---

## 📝 Configuration

### Color Scheme
- **Background**: `#1a1a1a`
- **Primary**: Blue
- **Font**: Arial
- **Theme**: Dark

### Standard Icon Sizes
- 16x16 (favicon)
- 32x32 (small icon)
- 48x48 (medium icon)
- 64x64 (large icon)
- 128x128 (extra large)
- 256x256 (ultra large)

---

## 🐛 Error Handling

All operations include proper error handling with user-friendly messages.

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 👨‍💻 Development Notes

- **Code Style**: PEP 8
- **Module Pattern**: Separation of concerns
- **UI Framework**: CustomTkinter (modern alternative to Tkinter)
- **Image Processing**: Pillow with advanced options

---

**Last Updated**: February 25, 2026
**Version**: 1.0.0 (Phase 1)
**Status**: 🟢 Active Development
