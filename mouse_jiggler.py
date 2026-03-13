import ctypes
import platform
import threading
from ctypes import wintypes


user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
shell32 = ctypes.WinDLL("shell32", use_last_error=True)

WNDPROCTYPE = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)

WM_DESTROY = 0x0002
WM_COMMAND = 0x0111
WM_RBUTTONUP = 0x0205
WM_LBUTTONDBLCLK = 0x0203
WM_APP = 0x8000
WM_TRAYICON = WM_APP + 1

WS_OVERLAPPED = 0x00000000
CW_USEDEFAULT = 0x80000000
IDI_APPLICATION = 32512
IDC_ARROW = 32512
COLOR_WINDOW = 5
TPM_LEFTALIGN = 0x0000
TPM_BOTTOMALIGN = 0x0020
TPM_RIGHTBUTTON = 0x0002
MF_STRING = 0x0000
MF_SEPARATOR = 0x0800
MF_GRAYED = 0x0001

NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
NIF_INFO = 0x00000010

ID_TRAY_STATUS = 1001
ID_TRAY_START = 1002
ID_TRAY_STOP = 1003
ID_TRAY_EXIT = 1004

DEFAULT_INTERVAL_SECONDS = 15
DEFAULT_OFFSET_PIXELS = 1
TRAY_TIP = "Mouse Jiggler"
TRAY_INFO_TITLE = "Mouse Jiggler"


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT),
        ("lPrivate", wintypes.DWORD),
    ]


class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROCTYPE),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", wintypes.WCHAR * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", wintypes.WCHAR * 256),
        ("uTimeoutOrVersion", wintypes.UINT),
        ("szInfoTitle", wintypes.WCHAR * 64),
        ("dwInfoFlags", wintypes.DWORD),
        ("guidItem", ctypes.c_byte * 16),
        ("hBalloonIcon", wintypes.HICON),
    ]


user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASS)]
user32.RegisterClassW.restype = wintypes.ATOM
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HWND,
    wintypes.HMENU,
    wintypes.HINSTANCE,
    wintypes.LPVOID,
]
user32.CreateWindowExW.restype = wintypes.HWND
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = ctypes.c_long
user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.DestroyWindow.restype = wintypes.BOOL
user32.PostQuitMessage.argtypes = [ctypes.c_int]
user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
user32.LoadIconW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
user32.LoadIconW.restype = wintypes.HICON
user32.LoadCursorW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
user32.LoadCursorW.restype = wintypes.HCURSOR
user32.CreatePopupMenu.restype = wintypes.HMENU
user32.AppendMenuW.argtypes = [wintypes.HMENU, wintypes.UINT, wintypes.UINT_PTR, wintypes.LPCWSTR]
user32.TrackPopupMenu.argtypes = [
    wintypes.HMENU,
    wintypes.UINT,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HWND,
    wintypes.LPCRECT,
]
user32.DestroyMenu.argtypes = [wintypes.HMENU]
user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SetForegroundWindow.argtypes = [wintypes.HWND]
kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
kernel32.GetModuleHandleW.restype = wintypes.HMODULE
shell32.Shell_NotifyIconW.argtypes = [wintypes.DWORD, ctypes.POINTER(NOTIFYICONDATA)]
shell32.Shell_NotifyIconW.restype = wintypes.BOOL


def get_cursor_pos():
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def set_cursor_pos(x, y):
    user32.SetCursorPos(x, y)


class MouseJigglerTrayApp:
    def __init__(self):
        self.interval_seconds = DEFAULT_INTERVAL_SECONDS
        self.offset_pixels = DEFAULT_OFFSET_PIXELS
        self.running = False
        self.direction = 1
        self.stop_event = threading.Event()
        self.worker = None

        self.hinstance = kernel32.GetModuleHandleW(None)
        self.class_name = "MouseJigglerTrayWindow"
        self.hwnd = None
        self.window_proc = WNDPROCTYPE(self._window_proc)
        self.nid = None

    def run(self):
        self._create_window()
        self._add_tray_icon()
        self.start()
        self._message_loop()

    def _create_window(self):
        wndclass = WNDCLASS()
        wndclass.lpfnWndProc = self.window_proc
        wndclass.hInstance = self.hinstance
        wndclass.lpszClassName = self.class_name
        wndclass.hIcon = user32.LoadIconW(None, ctypes.cast(IDI_APPLICATION, wintypes.LPCWSTR))
        wndclass.hCursor = user32.LoadCursorW(None, ctypes.cast(IDC_ARROW, wintypes.LPCWSTR))
        wndclass.hbrBackground = COLOR_WINDOW + 1

        atom = user32.RegisterClassW(ctypes.byref(wndclass))
        if not atom and ctypes.get_last_error() != 1410:
            raise ctypes.WinError(ctypes.get_last_error())

        self.hwnd = user32.CreateWindowExW(
            0,
            self.class_name,
            self.class_name,
            WS_OVERLAPPED,
            0,
            0,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            None,
            None,
            self.hinstance,
            None,
        )
        if not self.hwnd:
            raise ctypes.WinError(ctypes.get_last_error())

    def _build_notify_icon_data(self):
        data = NOTIFYICONDATA()
        data.cbSize = ctypes.sizeof(NOTIFYICONDATA)
        data.hWnd = self.hwnd
        data.uID = 1
        data.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
        data.uCallbackMessage = WM_TRAYICON
        data.hIcon = user32.LoadIconW(None, ctypes.cast(IDI_APPLICATION, wintypes.LPCWSTR))
        data.szTip = self._tray_text()
        return data

    def _add_tray_icon(self):
        self.nid = self._build_notify_icon_data()
        if not shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(self.nid)):
            raise ctypes.WinError(ctypes.get_last_error())

    def _update_tray_icon(self):
        if not self.nid:
            return
        self.nid.uFlags = NIF_TIP
        self.nid.szTip = self._tray_text()
        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))

    def _show_balloon(self, message):
        if not self.nid:
            return
        self.nid.uFlags = NIF_INFO
        self.nid.szInfoTitle = TRAY_INFO_TITLE
        self.nid.szInfo = message
        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))
        self.nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP

    def _tray_text(self):
        state = "Running" if self.running else "Stopped"
        return f"{TRAY_TIP} ({state})"

    def _message_loop(self):
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def start(self):
        if self.running:
            return
        if self.worker and self.worker.is_alive():
            self.worker.join(timeout=1)
        self.running = True
        self.stop_event.clear()
        self.worker = threading.Thread(target=self._jiggle_loop, daemon=True)
        self.worker.start()
        self._update_tray_icon()
        self._show_balloon("Mouse movement started.")

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.stop_event.set()
        if self.worker and self.worker.is_alive():
            self.worker.join(timeout=1)
        self._update_tray_icon()
        self._show_balloon("Mouse movement stopped.")

    def exit(self):
        self.stop()
        if self.nid:
            shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))
            self.nid = None
        if self.hwnd:
            user32.DestroyWindow(self.hwnd)

    def _jiggle_loop(self):
        while not self.stop_event.is_set():
            x, y = get_cursor_pos()
            offset = self.offset_pixels * self.direction
            set_cursor_pos(x + offset, y)
            self.direction *= -1
            if self.stop_event.wait(self.interval_seconds):
                break

    def _show_menu(self):
        menu = user32.CreatePopupMenu()
        if not menu:
            return

        status_text = f"Status: {'Running' if self.running else 'Stopped'}"
        user32.AppendMenuW(menu, MF_STRING | MF_GRAYED, ID_TRAY_STATUS, status_text)
        user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
        user32.AppendMenuW(menu, MF_STRING, ID_TRAY_START, "Start")
        user32.AppendMenuW(menu, MF_STRING, ID_TRAY_STOP, "Stop")
        user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
        user32.AppendMenuW(menu, MF_STRING, ID_TRAY_EXIT, "Exit")

        point = POINT()
        user32.GetCursorPos(ctypes.byref(point))
        user32.SetForegroundWindow(self.hwnd)
        user32.TrackPopupMenu(
            menu,
            TPM_LEFTALIGN | TPM_BOTTOMALIGN | TPM_RIGHTBUTTON,
            point.x,
            point.y,
            0,
            self.hwnd,
            None,
        )
        user32.DestroyMenu(menu)

    def _window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_COMMAND:
            command = wparam & 0xFFFF
            if command == ID_TRAY_START:
                self.start()
                return 0
            if command == ID_TRAY_STOP:
                self.stop()
                return 0
            if command == ID_TRAY_EXIT:
                self.exit()
                return 0

        if msg == WM_TRAYICON:
            if lparam == WM_RBUTTONUP:
                self._show_menu()
                return 0
            if lparam == WM_LBUTTONDBLCLK:
                if self.running:
                    self.stop()
                else:
                    self.start()
                return 0

        if msg == WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0

        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)


def main():
    if platform.system() != "Windows":
        raise RuntimeError("This app is intended to run on Windows.")

    app = MouseJigglerTrayApp()
    app.run()


if __name__ == "__main__":
    main()
