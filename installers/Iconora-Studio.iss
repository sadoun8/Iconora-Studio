; Inno Setup script for Iconora Studio
[Setup]
AppName=Iconora Studio
AppVersion=1.0.0
DefaultDirName={pf}\Iconora Studio
DefaultGroupName=Iconora Studio
OutputBaseFilename=Iconora-Studio-Setup
Compression=lzma
SolidCompression=yes
DisableDirPage=no
UninstallDisplayIcon={app}\Iconora Studio.exe
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
LicenseFile={#SourcePath}\..\EULA.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Application files (one-dir build output)
Source: "{#SourcePath}\..\dist\Iconora Studio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs; Check: IsDistPresent

; Optional Visual C++ Redistributable (place under installers/third_party if you want it bundled)
Source: "{#SourcePath}\third_party\vcredist_x64.exe"; DestDir: "{tmp}"; Flags: dontcopy; Check: FileExistsExpand('{#SourcePath}\\third_party\\vcredist_x64.exe')

[Icons]
Name: "{group}\Iconora Studio"; Filename: "{app}\Iconora Studio.exe"
Name: "{commondesktop}\Iconora Studio"; Filename: "{app}\Iconora Studio.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
; Run VC++ redistributable if bundled
Filename: "{tmp}\vcredist_x64.exe"; Parameters: "/install /quiet /norestart"; Flags: runhidden waituntilterminated skipifdoesntexist
; Launch the app after install
Filename: "{app}\Iconora Studio.exe"; Description: "Launch Iconora Studio"; Flags: nowait postinstall skipifsilent

[Code]
function IsDistPresent(): Boolean;
begin
  Result := DirExists(ExpandConstant('{#SourcePath}\\dist\\Iconora Studio'));
end;

function FileExistsExpand(const S: string): Boolean;
var
  P: string;
begin
  P := ExpandConstant(S);
  Result := FileExists(P);
end;

#define SourcePath "{src}"
