; Inno Setup script for Iconora Studio
[Setup]
AppName=Iconora Studio
AppVersion=2.0.0
DefaultDirName={commonpf}\Iconora Studio
DefaultGroupName=Iconora Studio
OutputBaseFilename=Iconora-Studio-Setup-v2.0.0
Compression=lzma
SolidCompression=yes
DisableDirPage=no
UninstallDisplayIcon={app}\Iconora Studio.exe
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
LicenseFile=..\EULA.txt
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[Files]
Source: "..\dist\Iconora Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Code]
const
  VCRedistURL = 'https://aka.ms/vs/17/release/vc_redist.x64.exe';

procedure DownloadVCRedist();
var
  ResultCode: Integer;
  VCRedistFilePath: String;
  PSCmd: String;
begin
  VCRedistFilePath := ExpandConstant('{tmp}\vc_redist.x64.exe');

  if not FileExists(VCRedistFilePath) then
  begin
    PSCmd := Format('powershell -NoProfile -Command "try { Invoke-WebRequest -Uri ''%s'' -OutFile ''%s'' -UseBasicParsing } catch { exit 1 }"', [VCRedistURL, VCRedistFilePath]);
    Log('Downloading Visual C++ Redistributable...');
    if not Exec(ExpandConstant('{cmd}'), '/c ' + PSCmd, '', SW_HIDE, ewWaitUntilTerminated, ResultCode) or (ResultCode <> 0) then
    begin
      Log('Failed to download Visual C++ Redistributable, but continuing installation...');
    end;
  end;
end;

function FileExistsExpand(const S: string): Boolean;
var
  P: string;
begin
  P := ExpandConstant(S);
  Result := FileExists(P);
end;

procedure InitializeWizard();
begin
  DownloadVCRedist();
end;

[Icons]
Name: "{group}\Iconora Studio"; Filename: "{app}\Iconora Studio.exe"
Name: "{commondesktop}\Iconora Studio"; Filename: "{app}\Iconora Studio.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/install /quiet /norestart"; Flags: runhidden waituntilterminated skipifdoesntexist
Filename: "{app}\Iconora Studio.exe"; Description: "Launch Iconora Studio"; Flags: nowait postinstall skipifsilent
