# Mouse Jiggler

Small Windows tray app that nudges the mouse cursor slightly on a timer.

## What it does

- Moves the mouse 50 pixels every 15 seconds
- Alternates left and right so the cursor oscillates and returns to the same resting position
- Default interval is 15 seconds
- Starts in the Windows system tray / notification area
- Lets you `Start`, `Stop`, or `Exit` from the tray icon menu
- Runs directly on Windows without requiring an extra runtime install

## Run on Windows

PowerShell is available on current Windows installs, so you can run the tray app directly:

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
dotnet publish .\MouseJigglerExe\MouseJigglerExe.csproj -c Release -r win-x64 -o .\release-assets
```

The generated executable will be:

```text
\release-assets\move_mouse.exe
```


## Download the EXE from GitHub Releases

Publishing a GitHub release triggers GitHub Actions to build `move_mouse.exe` and attach it to that release automatically.

Typical flow:

1. Push the repo to GitHub.
2. Create a tag and GitHub release.
3. Wait for the `Build Windows Release` workflow to finish.
4. Download `move_mouse.exe` from the release page.

## Notes

- Double-clicking the tray icon toggles start/stop.
- If your company manages inactivity policies, make sure you are allowed to use software like this.
