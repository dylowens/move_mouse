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

    [DllImport("user32.dll", SetLastError = true)]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
"@

$mouseIntervalMs = 15000
$windowsKeyIntervalMs = 300000
$offsetPixels = 50
$direction = 1
$running = $true
$vkLwin = 0x5B
$keyeventfKeyup = 0x0002

$notifyIcon = New-Object System.Windows.Forms.NotifyIcon
$notifyIcon.Icon = [System.Drawing.SystemIcons]::Application
$notifyIcon.Visible = $true

function Invoke-WindowsKeyTap {
    [NativeMethods]::keybd_event($vkLwin, 0, 0, [UIntPtr]::Zero)
    [NativeMethods]::keybd_event($vkLwin, 0, $keyeventfKeyup, [UIntPtr]::Zero)
}

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

$mouseTimer = New-Object System.Windows.Forms.Timer
$mouseTimer.Interval = $mouseIntervalMs
$mouseTimer.Add_Tick({
    if (-not $script:running) {
        return
    }

    $point = New-Object NativeMethods+POINT
    [void][NativeMethods]::GetCursorPos([ref]$point)
    $offset = $offsetPixels * $script:direction
    [void][NativeMethods]::SetCursorPos($point.X + $offset, $point.Y)
    $script:direction *= -1
})

$windowsKeyTimer = New-Object System.Windows.Forms.Timer
$windowsKeyTimer.Interval = $windowsKeyIntervalMs
$windowsKeyTimer.Add_Tick({
    if (-not $script:running) {
        return
    }

    Invoke-WindowsKeyTap
    Start-Sleep -Seconds 3
    Invoke-WindowsKeyTap
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
    $mouseTimer.Stop()
    $windowsKeyTimer.Stop()
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
        Show-Status "Mouse movement and Windows key toggling stopped."
    }
    else {
        $script:running = $true
        $statusItem.Text = "Status: Running"
        Show-Status "Mouse movement and Windows key toggling started."
    }
    Update-Tray
})

Update-Tray
Show-Status "Mouse movement and Windows key toggling started."
$mouseTimer.Start()
$windowsKeyTimer.Start()

[System.Windows.Forms.Application]::Run()
