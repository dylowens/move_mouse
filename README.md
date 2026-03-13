# Mouse Jiggler

Small Windows tray app that nudges the mouse cursor slightly on a timer.

## What it does

- Moves the mouse by a small number of pixels
- Default interval is 15 seconds
- Starts in the Windows system tray / notification area
- Lets you `Start`, `Stop`, or `Exit` from the tray icon menu
- Uses only Python standard library modules

## Run on Windows

1. Install Python 3 for Windows.
2. Open Command Prompt in this folder.
3. Run:

```bat
python mouse_jiggler.py
```

The app will start in the tray and begin nudging the mouse immediately. Right-click the tray icon to open the menu.

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

- This script targets Windows because it uses Win32 cursor APIs.
- Double-clicking the tray icon toggles start/stop.
- If your company manages inactivity policies, make sure you are allowed to use software like this.
