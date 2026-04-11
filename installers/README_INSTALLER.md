Iconora Studio — Installer build instructions

Prerequisites

- Windows machine with Inno Setup (Inno Setup 6) installed. Download: <https://jrsoftware.org/>
- The one-dir build output must be at `dist\Iconora Studio` (this folder should contain `Iconora Studio.exe` and related files).
- Internet connection during installation (for downloading Visual C++ Redistributable if not already installed).

Build steps (PowerShell)

```powershell
# from repository root
cd installers
# If ISCC is on PATH or installed in default location, run:
.\build_installer.ps1
```

Or run ISCC directly:

```powershell
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installers\Iconora-Studio.iss"
```

Notes

- The script sets `PrivilegesRequired=admin` so installer will require elevation.
- To sign the installer, pass your signing tool (e.g. `signtool.exe /a /fd SHA256 /tr ...`) after the `.exe` is produced.
- **Visual C++ Redistributable**: The installer automatically downloads and installs Visual C++ Redistributable (x64) from Microsoft's servers if not already installed on the user's system. This is required because the application is built with Python/PyInstaller which depends on VC++ runtime libraries. The download happens silently during installation (requires internet).
- If the end-user's system cannot download the redistributable (firewall/proxy), they can manually install it from: <https://aka.ms/vs/17/release/vc_redist.x64.exe>

*Fix:* previous versions of the `.iss` included a `Check: IsDistPresent` on the
[Files] entry.  That check evaluated during installation on the end‑user's
machine (which obviously doesn't have our build tree) and consequently
skipped copying all of the application files.  The installer built by that
script appeared to run but produced a non‑functional install.  The check is
now removed; the PowerShell helper already aborts the build if `dist\Iconora
Studio` is missing.

## Known Issues & Fixes

### Missing DLL Files Issue (RESOLVED)

**Problem:** The installer previously bundled with cairosvg and rembg, which depend on complex system libraries (libxml2.dll, zlib1.dll, libcairo-2.dll) that are not readily available on Windows.

**Solution Applied:**

- Removed `cairosvg` and `rembg` from `requirements.txt` (not used in core functionality)
- Updated to Pillow 12.1.0 which has pre-built Windows wheels without external dependencies
- Rebuilt with `--onedir` mode ensuing all necessary DLLs are bundled correctly

**Updated requirements.txt contains only:**

```
customtkinter==5.2.2
pillow==12.1.0
svgwrite==1.4.3
PyInstaller==6.4.0
tkinterdnd2==0.3.0
```

**Result:** Installer now works cleanly on any Windows system without requiring external system libraries.

Troubleshooting

- If the installer build fails, open the `.iss` in Inno Setup IDE to get detailed errors.
- Make sure the `dist\Iconora Studio` path exists and is readable.
