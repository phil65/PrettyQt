from __future__ import annotations

from ctypes import Structure, c_int, windll, byref, sizeof
from ctypes.wintypes import DWORD, HWND, UINT, RECT, LPARAM
import win32con
from typing import SupportsInt

import win32api
import win32gui
from win32comext.shell import shellcon


class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("hWnd", HWND),
        ("uCallbackMessage", UINT),
        ("uEdge", UINT),
        ("rc", RECT),
        ("lParam", LPARAM),
    ]


def raise_to_top(h_wnd: SupportsInt):
    h_wnd = int(h_wnd)
    # set to always-on-top and disable it again. that way windows stays in front
    flag = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
    win32gui.SetWindowPos(h_wnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flag)
    win32gui.SetWindowPos(h_wnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flag)


def set_window_nonresizable(h_wnd: SupportsInt):
    h_wnd = int(h_wnd)
    style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
    style &= ~win32con.WS_SIZEBOX
    style &= ~win32con.WS_THICKFRAME
    style &= ~win32con.WS_MAXIMIZEBOX
    win32gui.SetWindowLong(h_wnd, win32con.GWL_STYLE, style)


def is_window_resizable(h_wnd: SupportsInt) -> bool:
    h_wnd = int(h_wnd)
    style = win32api.GetWindowLong(h_wnd, win32con.GWL_STYLE)
    return style & win32con.WS_SIZEBOX != 0


def is_maximized(h_wnd: SupportsInt) -> bool:
    h_wnd = int(h_wnd)
    window_placement = win32gui.GetWindowPlacement(h_wnd)
    return window_placement[1] == win32con.SW_MAXIMIZE if window_placement else False


def start_system_move(h_wnd: SupportsInt) -> None:
    win32gui.ReleaseCapture()
    win32api.SendMessage(
        int(h_wnd), win32con.WM_SYSCOMMAND, win32con.SC_MOVE | win32con.HTCAPTION, 0
    )  # pyside6-frameless-window uses "+" instead of "|"?


def get_monitor_info(h_wnd, dw_flags):
    if monitor := win32api.MonitorFromWindow(h_wnd, dw_flags):
        return win32api.GetMonitorInfo(monitor)


def is_full_screen(h_wnd):
    if not h_wnd:
        return False
    h_wnd = int(h_wnd)

    win_rect = win32gui.GetWindowRect(h_wnd)
    if not win_rect:
        return False

    monitor_info = get_monitor_info(h_wnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitor_info:
        return False

    monitor_rect = monitor_info["Monitor"]
    return all(i == j for i, j in zip(win_rect, monitor_rect))


def get_resize_border_thickness():
    result = win32api.GetSystemMetrics(
        win32con.SM_CXSIZEFRAME
    ) + win32api.GetSystemMetrics(92)

    if result > 0:
        return result

    b_result = c_int(0)
    windll.dwmapi.DwmIsCompositionEnabled(byref(b_result))
    return 8 if bool(b_result.value) else 4


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def is_auto_hide():
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(0, 0, 0, 0), 0)
        taskbar_state = windll.shell32.SHAppBarMessage(
            shellcon.ABM_GETSTATE, byref(appbar_data)
        )
        return taskbar_state == shellcon.ABS_AUTOHIDE

    @classmethod
    def get_position(cls, h_wnd):
        monitor_info = get_monitor_info(h_wnd, win32con.MONITOR_DEFAULTTONEAREST)
        if not monitor_info:
            return cls.NO_POSITION

        monitor = RECT(*monitor_info["Monitor"])
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
        for position in (cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM):
            appbar_data.uEdge = position
            if windll.shell32.SHAppBarMessage(11, byref(appbar_data)):
                return position

        return cls.NO_POSITION
