# Mouse Jiggler

Small Windows tray app that nudges the mouse cursor slightly on a timer.

## What it does

- Moves the mouse by a small number of pixels
- Default interval is 15 seconds
- Starts in the Windows system tray / notification area
- Lets you `Start`, `Stop`, or `Exit` from the tray icon menu
- Uses only Python standard library modules

## Run on Windows without Python

PowerShell is available on current Windows installs, so you can run the tray app directly without installing Python:

```powershell
powershell -ExecutionPolicy Bypass -File .\mouse_jiggler.ps1
```

If you want to use PowerShell 7 specifically:

```powershell
pwsh -File .\mouse_jiggler.ps1
```

The app will start in the tray and begin nudging the mouse immediately. Right-click the tray icon to open the menu.

## Build a standalone EXE

This repo also includes a native Windows Forms tray app in [`MouseJigglerExe`](/C:/Users/dylow/OneDrive/Documents/Playground/MouseJigglerExe/MouseJigglerExe.csproj). It can be published as a single-file self-contained executable:

```powershell
dotnet publish .\MouseJigglerExe\MouseJigglerExe.csproj -c Release
```

The generated executable will be:

```text
.\MouseJigglerExe\bin\Release\net9.0-windows\win-x64\publish\move_mouse.exe
```

## Run on Windows with Python

1. Install Python 3 for Windows.
2. Open Command Prompt in this folder.
3. Run:

```bat
python mouse_jiggler.py
```

## Download the EXE from GitHub Releases

Once this repo is on GitHub, publishing a release will trigger GitHub Actions to build a Windows executable and attach `move_mouse.exe` to that release automatically.

Typical flow:

1. Push the repo to GitHub.
2. Create a tag and GitHub release.
3. Wait for the `Build Windows Release` workflow to finish.
4. Download `move_mouse.exe` from the release page.

## Optional: local build

If you want a standalone `.exe`, install PyInstaller and build it:

```bat
pip install pyinstaller
pyinstaller --noconsole --onefile --name move_mouse mouse_jiggler.py
```

The executable will be created under `dist\move_mouse.exe`.

## Notes

- Both implementations target Windows because they use Win32 cursor APIs.
- [`mouse_jiggler.ps1`](/C:/Users/dylow/OneDrive/Documents/Playground/mouse_jiggler.ps1) does not require Python on the host machine.
- Double-clicking the tray icon toggles start/stop.
- If your company manages inactivity policies, make sure you are allowed to use software like this.
