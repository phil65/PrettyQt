from __future__ import annotations

import ctypes
from ctypes import POINTER, Structure, byref, c_int, cdll
from ctypes.wintypes import HWND, POINT, RECT, UINT
from typing import SupportsInt

import win32api
import win32con
import win32gui

from prettyqt.qt import QtWidgets


user32 = ctypes.windll.user32


class MARGINS(Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]


class PWINDOWPOS(Structure):
    _fields_ = [
        ("hWnd", HWND),
        ("hwndInsertAfter", HWND),
        ("x", c_int),
        ("y", c_int),
        ("cx", c_int),
        ("cy", c_int),
        ("flags", UINT),
    ]


class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [("rgrc", RECT * 3), ("lppos", POINTER(PWINDOWPOS))]


LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)


def raise_to_top(h_wnd: SupportsInt):
    h_wnd = int(h_wnd)
    # set to always-on-top and disable it again. that way windows stays in front
    flag = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
    win32gui.SetWindowPos(h_wnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flag)
    win32gui.SetWindowPos(h_wnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flag)


def add_shadow_effect(h_wnd: SupportsInt):
    h_wnd = int(h_wnd)
    margins = MARGINS(-1, -1, -1, -1)
    dwmapi = cdll.LoadLibrary("dwmapi")
    dwmapi.DwmExtendFrameIntoClientArea(h_wnd, byref(margins))


def add_window_animation(h_wnd: SupportsInt):
    h_wnd = int(h_wnd)
    style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
    win32gui.SetWindowLong(
        h_wnd,
        win32con.GWL_STYLE,
        style
        | win32con.WS_MINIMIZEBOX
        | win32con.WS_MAXIMIZEBOX
        | win32con.WS_CAPTION
        | win32con.CS_DBLCLKS
        | win32con.WS_THICKFRAME,
        # | win32con.WS_MINIMIZEBOX,
        # | win32con.WS_MAXIMIZEBOX
        # | win32con.WS_CAPTION
        # | win32con.WS_THICKFRAME
        # | win32con.WS_POPUP
        # | win32con.WS_SYSMENU
    )


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


def is_fullscreen(h_wnd: SupportsInt) -> bool:
    h_wnd = int(h_wnd)
    win_rect = win32gui.GetWindowRect(h_wnd)
    if not win_rect:
        return False

    monitor = win32api.MonitorFromWindow(h_wnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    monitor_info = win32api.GetMonitorInfo(monitor)
    if not monitor_info:
        return False

    monitor_rect = monitor_info["Monitor"]
    return all(i == j for i, j in zip(win_rect, monitor_rect))


def start_system_move(h_wnd: SupportsInt) -> None:
    win32gui.ReleaseCapture()
    win32api.SendMessage(
        int(h_wnd), win32con.WM_SYSCOMMAND, win32con.SC_MOVE | win32con.HTCAPTION, 0
    )


def _native_event(widget: QtWidgets.QWidget, message: SupportsInt) -> tuple[bool, int]:
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    r = widget.devicePixelRatioF()
    x = pt.x / r - widget.x()
    y = pt.y / r - widget.y()
    is_maximize_button = widget.childAt(x, y) is widget.title_bar.maximize_button
    msg = ctypes.wintypes.MSG.from_address(int(message))
    dpi = user32.GetDpiForWindow(msg.hWnd)
    sys_metrics = user32.GetSystemMetricsForDpi(92, dpi)
    border_width = user32.GetSystemMetricsForDpi(win32con.SM_CXFRAME, dpi) + sys_metrics
    border_height = user32.GetSystemMetricsForDpi(win32con.SM_CYFRAME, dpi) + sys_metrics
    match msg.message:
        case win32con.WM_NCHITTEST:
            if widget.is_resizable():
                w, h = widget.width(), widget.height()
                lx = x < border_width
                rx = x > w - 2 * border_width
                ty = y < border_height
                by = y > h - border_height

                if lx and ty:
                    return True, win32con.HTTOPLEFT
                if rx and by:
                    return True, win32con.HTBOTTOMRIGHT
                if rx and ty:
                    return True, win32con.HTTOPRIGHT
                if lx and by:
                    return True, win32con.HTBOTTOMLEFT
                if ty:
                    return True, win32con.HTTOP
                if by:
                    return True, win32con.HTBOTTOM
                if lx:
                    return True, win32con.HTLEFT
                if rx:
                    return True, win32con.HTRIGHT

            if is_maximize_button:
                widget.title_bar.maximize_button.set_state("hover")
                return True, win32con.HTMAXBUTTON
            buttons = widget.title_bar.findChildren(QtWidgets.QPushButton)
            if (
                widget.childAt(x, y) not in buttons
                and border_height < y < widget.title_bar.height()
            ):
                return True, win32con.HTCAPTION

        case 0x2A2 | win32con.WM_MOUSELEAVE:
            widget.title_bar.maximize_button.set_state("normal")
        case win32con.WM_NCLBUTTONDOWN | win32con.WM_NCLBUTTONDBLCLK:
            if is_maximize_button:
                widget.title_bar.on_maximize_button_clicked()
                return True, 0
        case win32con.WM_NCLBUTTONUP | win32con.WM_NCRBUTTONUP:
            if is_maximize_button:
                widget.title_bar.on_maximize_button_clicked()
                return None
        case win32con.WM_NCCALCSIZE:
            rect = ctypes.cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]

            is_max = is_maximized(msg.hWnd)
            is_full = is_fullscreen(msg.hWnd)

            # adjust the size of client rect
            if is_max and not is_full:
                rect.top += border_height
                rect.left += border_width
                rect.right -= border_width
                rect.bottom -= border_height

            return True, win32con.WVR_REDRAW
