Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class NativeMethods
{
    [StructLayout(LayoutKind.Sequential)]
    public struct POINT
    {
        public int X;
        public int Y;
    }

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool GetCursorPos(out POINT lpPoint);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SetCursorPos(int X, int Y);
}
"@

$intervalMs = 15000
$offsetPixels = 50
$direction = 1
$running = $true

$notifyIcon = New-Object System.Windows.Forms.NotifyIcon
$notifyIcon.Icon = [System.Drawing.SystemIcons]::Application
$notifyIcon.Visible = $true

function Get-TrayText {
    if ($script:running) {
        return "Mouse Jiggler (Running)"
    }
    return "Mouse Jiggler (Stopped)"
}

function Show-Status {
    param(
        [string]$Message
    )

    $notifyIcon.BalloonTipTitle = "Mouse Jiggler"
    $notifyIcon.BalloonTipText = $Message
    $notifyIcon.ShowBalloonTip(3000)
}

function Update-Tray {
    $notifyIcon.Text = Get-TrayText
}

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = $intervalMs
$timer.Add_Tick({
    if (-not $script:running) {
        return
    }

    $point = New-Object NativeMethods+POINT
    [void][NativeMethods]::GetCursorPos([ref]$point)
    $offset = $offsetPixels * $script:direction
    [void][NativeMethods]::SetCursorPos($point.X + $offset, $point.Y)
    $script:direction *= -1
})

$menu = New-Object System.Windows.Forms.ContextMenuStrip

$statusItem = $menu.Items.Add("Status: Running")
$statusItem.Enabled = $false
[void]$menu.Items.Add("-")

$startItem = $menu.Items.Add("Start")
$startItem.Add_Click({
    if (-not $script:running) {
        $script:running = $true
        $statusItem.Text = "Status: Running"
        Update-Tray
        Show-Status "Mouse movement started."
    }
})

$stopItem = $menu.Items.Add("Stop")
$stopItem.Add_Click({
    if ($script:running) {
        $script:running = $false
        $statusItem.Text = "Status: Stopped"
        Update-Tray
        Show-Status "Mouse movement stopped."
    }
})

[void]$menu.Items.Add("-")

$exitItem = $menu.Items.Add("Exit")
$exitItem.Add_Click({
    $timer.Stop()
    $notifyIcon.Visible = $false
    $notifyIcon.Dispose()
    $menu.Dispose()
    [System.Windows.Forms.Application]::Exit()
})

$notifyIcon.ContextMenuStrip = $menu
$notifyIcon.Add_MouseDoubleClick({
    if ($script:running) {
        $script:running = $false
        $statusItem.Text = "Status: Stopped"
        Show-Status "Mouse movement stopped."
    }
    else {
        $script:running = $true
        $statusItem.Text = "Status: Running"
        Show-Status "Mouse movement started."
    }
    Update-Tray
})

Update-Tray
Show-Status "Mouse movement started."
$timer.Start()

[System.Windows.Forms.Application]::Run()
