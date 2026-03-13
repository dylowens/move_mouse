using System.ComponentModel;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace MouseJigglerExe;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new TrayApplicationContext());
    }
}

internal sealed class TrayApplicationContext : ApplicationContext
{
    private const int DefaultMouseIntervalMilliseconds = 15_000;
    private const int DefaultWindowsKeyIntervalMilliseconds = 60_000;
    private const int DefaultOffsetPixels = 50;
    private const byte VkLwin = 0x5B;
    private const uint KeyeventfKeyup = 0x0002;

    private readonly NotifyIcon notifyIcon;
    private readonly ToolStripMenuItem statusItem;
    private readonly ToolStripMenuItem startItem;
    private readonly ToolStripMenuItem stopItem;
    private readonly System.Windows.Forms.Timer mouseTimer;
    private readonly System.Windows.Forms.Timer windowsKeyTimer;

    private bool running = true;
    private int direction = 1;

    public TrayApplicationContext()
    {
        statusItem = new ToolStripMenuItem("Status: Running") { Enabled = false };
        startItem = new ToolStripMenuItem("Start");
        stopItem = new ToolStripMenuItem("Stop");

        var menu = new ContextMenuStrip();
        menu.Items.Add(statusItem);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(startItem);
        menu.Items.Add(stopItem);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(new ToolStripMenuItem("Exit", null, (_, _) => ExitThread()));

        notifyIcon = new NotifyIcon
        {
            Icon = SystemIcons.Application,
            ContextMenuStrip = menu,
            Text = BuildTrayText(),
            Visible = true
        };

        notifyIcon.MouseDoubleClick += (_, e) =>
        {
            if (e.Button == MouseButtons.Left)
            {
                ToggleRunning();
            }
        };

        startItem.Click += (_, _) => StartJiggling();
        stopItem.Click += (_, _) => StopJiggling();

        mouseTimer = new System.Windows.Forms.Timer { Interval = DefaultMouseIntervalMilliseconds };
        mouseTimer.Tick += (_, _) => JiggleMouse();
        mouseTimer.Start();

        windowsKeyTimer = new System.Windows.Forms.Timer { Interval = DefaultWindowsKeyIntervalMilliseconds };
        windowsKeyTimer.Tick += (_, _) => ToggleStartMenu();
        windowsKeyTimer.Start();

        UpdateMenuState();
        ShowBalloon("Mouse movement and Windows key toggling started.");
    }

    protected override void ExitThreadCore()
    {
        mouseTimer.Stop();
        windowsKeyTimer.Stop();
        notifyIcon.Visible = false;
        notifyIcon.Dispose();
        mouseTimer.Dispose();
        windowsKeyTimer.Dispose();
        base.ExitThreadCore();
    }

    private void ToggleRunning()
    {
        if (running)
        {
            StopJiggling();
        }
        else
        {
            StartJiggling();
        }
    }

    private void StartJiggling()
    {
        if (running)
        {
            return;
        }

        running = true;
        UpdateMenuState();
        ShowBalloon("Mouse movement and Windows key toggling started.");
    }

    private void StopJiggling()
    {
        if (!running)
        {
            return;
        }

        running = false;
        UpdateMenuState();
        ShowBalloon("Mouse movement and Windows key toggling stopped.");
    }

    private void UpdateMenuState()
    {
        statusItem.Text = running ? "Status: Running" : "Status: Stopped";
        startItem.Enabled = !running;
        stopItem.Enabled = running;
        notifyIcon.Text = BuildTrayText();
    }

    private string BuildTrayText()
    {
        return running ? "Mouse Jiggler (Running)" : "Mouse Jiggler (Stopped)";
    }

    private void ShowBalloon(string message)
    {
        notifyIcon.BalloonTipTitle = "Mouse Jiggler";
        notifyIcon.BalloonTipText = message;
        notifyIcon.ShowBalloonTip(3000);
    }

    private void JiggleMouse()
    {
        if (!running)
        {
            return;
        }

        if (!NativeMethods.GetCursorPos(out var point))
        {
            throw new Win32Exception(Marshal.GetLastWin32Error());
        }

        var offset = DefaultOffsetPixels * direction;
        if (!NativeMethods.SetCursorPos(point.X + offset, point.Y))
        {
            throw new Win32Exception(Marshal.GetLastWin32Error());
        }

        direction *= -1;
    }

    private void ToggleStartMenu()
    {
        if (!running)
        {
            return;
        }

        TapWindowsKey();
        Thread.Sleep(150);
        TapWindowsKey();
    }

    private static void TapWindowsKey()
    {
        NativeMethods.keybd_event(VkLwin, 0, 0, 0);
        NativeMethods.keybd_event(VkLwin, 0, KeyeventfKeyup, 0);
    }
}

internal static class NativeMethods
{
    [StructLayout(LayoutKind.Sequential)]
    internal struct Point
    {
        public int X;
        public int Y;
    }

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool GetCursorPos(out Point point);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool SetCursorPos(int x, int y);

    [DllImport("user32.dll", SetLastError = true)]
    internal static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, nuint dwExtraInfo);
}
