# Iconora Studio - Project Guidelines

## 🚀 Build & Development Commands
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Application**: `python main.py` or `python run_app.py`
- **Build Executable (.exe)**: `python build_exe.py`
- **Build Installer (Inno Setup)**: `powershell ./installers/build_installer.ps1` (Requires Inno Setup 6+)

## 🛠️ Maintenance Workflow
1. **Version Sync**: Always ensure `AppVersion` in `installers/Iconora-Studio.iss` and `APP_VERSION` in `config.py` match (Current: 1.2.0).
2. **Localization**: Use `tr("key_name")` for all UI strings. Support for Arabic (RTL) and English (LTR) is mandatory.
3. **Project Support**: Any new UI Tab MUST implement `get_project_data()` and `load_project_data(data)`.
4. **Build Automation**: After major changes, verify `build_exe.py` and update `[Files]` in `Iconora-Studio.iss`.
5. **Output Paths**: Use `config.EXPORTS_DIR` (standardized to User Documents to avoid WinError 5 Access Denied).

## 🌍 Localization System
- Primary localization in `i18n.py`.
- Mandatory RTL/LTR support.

## 📦 Installer Configuration (`Iconora-Studio.iss`)
- Keep version synced with `config.py`.
- Supports multi-language installation (AR/EN).
