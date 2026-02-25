# Contributing to Iconora Studio

We welcome contributions! This guide will help you get started.

## Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/iconora-studio.git
cd iconora-studio
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

## Development Workflow

### Making Changes

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Follow PEP 8 style guide
   - Add type hints where possible
   - Write docstrings for functions
   - Keep modules modular and focused

3. **Test your changes**
```bash
python test.py
```

4. **Format your code**
```bash
black .
flake8 .
```

5. **Commit your changes**
```bash
git add .
git commit -m "Add your descriptive message"
```

6. **Push and create a pull request**
```bash
git push origin feature/your-feature-name
```

## Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints for function parameters and returns
- Maximum line length: 100 characters
- Use 4 spaces for indentation

### Example:
```python
from pathlib import Path
from typing import Optional, List

def convert_image(
    input_path: str,
    output_path: str,
    sizes: Optional[List[tuple]] = None
) -> bool:
    """
    Convert image to specified sizes.

    Args:
        input_path: Path to input image
        output_path: Path for output
        sizes: List of (width, height) tuples

    Returns:
        True if successful, False otherwise
    """
    # Implementation here
    pass
```

## Module Architecture

### core/
Processing engines that handle:
- Image conversion
- SVG creation
- Logo generation
- Signature generation
- Background removal

### ui/
User interface components:
- Each feature has its own Tab class
- All styled with CustomTkinter
- Support for Arabic text

### assets/
Static resources:
- fonts/ - Custom fonts
- icons/ - Application icons
- templates/ - Ready-made designs

## Adding a New Feature

### Example: Add Background Removal

1. **Create the engine** (`core/background_remover.py`):
```python
from typing import Optional
from PIL import Image

class BackgroundRemover:
    """Remove background from images"""

    def __init__(self, image_path: str):
        self.image = Image.open(image_path)

    def remove(self) -> Image.Image:
        """Remove background"""
        # Implementation using rembg
        pass
```

2. **Create the UI** (`ui/bg_removal_tab.py`):
```python
import customtkinter as ctk
from core.background_remover import BackgroundRemover

class BackgroundRemovalTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create UI components
        pass
```

3. **Add to main window** (`ui/main_window.py`):
```python
from ui.bg_removal_tab import BackgroundRemovalTab

# In setup_ui method:
bg_tab = tab_view.add("Background Removal")
bg_content = BackgroundRemovalTab(bg_tab)
bg_content.pack(fill="both", expand=True)
```

## Testing

### Run tests
```bash
python test.py
```

### Run specific tests
```bash
pytest tests/
```

### Check code quality
```bash
pylint core/ ui/
flake8 .
black --check .
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions
- Update CHANGELOG.md with your changes

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Formatting
- **refactor**: Code restructuring
- **test**: Adding tests
- **chore**: Build/dependency updates

### Example
```
feat(icon_converter): Add batch conversion support

- Added ability to convert multiple images at once
- Improved progress reporting
- Added cancellation support

Closes #123
```

## Build & Release

### Building for distribution
```bash
python build_exe.py
```

This creates:
- `dist/IconoraStudio.exe` - Standalone executable
- `dist/` - All dependencies included

### Version numbering
We follow semantic versioning: `MAJOR.MINOR.PATCH`

### Phases
- Phase 1: Icon Converter ✅
- Phase 2: SVG Converter
- Phase 3: Logo Designer
- Phase 4: Signature Generator
- Phase 5: Advanced Tools

## Questions?

- Open an issue for bugs
- Start a discussion for ideas
- Check existing issues before posting

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Happy coding! 🚀
