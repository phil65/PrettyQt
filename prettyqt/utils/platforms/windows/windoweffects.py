from __future__ import annotations

from ctypes import Structure, POINTER, c_int, sizeof, pointer, cdll, c_bool, byref
from ctypes.wintypes import DWORD, ULONG, BOOL, HRGN, LPCVOID, LONG
import enum
import sys
from typing import SupportsInt

import win32con
import win32gui


class WINDOWCOMPOSITIONATTRIB(enum.Enum):
    WCA_ACCENT_POLICY = 19
    WCA_USEDARKMODECOLORS = 26


class ACCENT_STATE(enum.Enum):
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4  # Acrylic effect
    ACCENT_ENABLE_HOSTBACKDROP = 5  # Mica effect


class DWMWINDOWATTRIBUTE(enum.Enum):
    DWMWA_NCRENDERING_POLICY = 2


class DWMNCRENDERINGPOLICY(enum.Enum):
    DWMNCRP_DISABLED = 1


class ACCENT_POLICY(Structure):
    _fields_ = [
        ("AccentState", DWORD),
        ("AccentFlags", DWORD),
        ("GradientColor", DWORD),
        ("AnimationId", DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ("Attribute", DWORD),
        ("Data", POINTER(ACCENT_POLICY)),
        ("SizeOfData", ULONG),
    ]


class MARGINS(Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]


class DWM_BLURBEHIND(Structure):
    _fields_ = [
        ("dwFlags", DWORD),
        ("fEnable", BOOL),
        ("hRgnBlur", HRGN),
        ("fTransitionOnMaximized", BOOL),
    ]


class WindowsEffects:
    """Class for applying Windows effects."""

    def __init__(self):
        # Initialize structure
        self.accent_policy = ACCENT_POLICY()
        self.win_comp_attr_data = WINDOWCOMPOSITIONATTRIBDATA()
        self.win_comp_attr_data.Attribute = (
            WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        )
        self.win_comp_attr_data.SizeOfData = sizeof(self.accent_policy)
        self.win_comp_attr_data.Data = pointer(self.accent_policy)

        # Declare the function signature of the API
        user_32 = cdll.LoadLibrary("user32")
        self.set_win_comp_attr = user_32.SetWindowCompositionAttribute
        dwm_api = cdll.LoadLibrary("dwmapi")
        self.dwm_ext_frame_into_client_area = dwm_api.DwmExtendFrameIntoClientArea
        self.dwm_enable_blur_behind_win = dwm_api.DwmEnableBlurBehindWindow
        self.dwm_set_win_attr = dwm_api.DwmSetWindowAttribute

        self.set_win_comp_attr.argtypes = [c_int, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
        self.dwm_ext_frame_into_client_area.argtypes = [c_int, POINTER(MARGINS)]
        self.dwm_enable_blur_behind_win.argtypes = [c_int, POINTER(DWM_BLURBEHIND)]
        self.dwm_set_win_attr.argtypes = [c_int, DWORD, LPCVOID, DWORD]

        self.set_win_comp_attr.restype = c_bool
        self.dwm_ext_frame_into_client_area.restype = LONG
        self.dwm_enable_blur_behind_win.restype = LONG
        self.dwm_set_win_attr.restype = LONG

    def add_acrylic_effect(
        self,
        h_wnd: SupportsInt,
        gradient_color: str,
        enable_shadow: bool = True,
        animation_id: int = 0,
    ):
        gradient_color = "".join(gradient_color[i : i + 2] for i in range(6, -1, -2))
        gradient_color = DWORD(int(gradient_color, base=16))
        accent_flags = DWORD(0x20 | 0x40 | 0x80 | 0x100) if enable_shadow else DWORD(0)
        animation_id = DWORD(animation_id)

        self.accent_policy.AccentState = (
            ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value
        )
        self.accent_policy.AccentFlags = accent_flags
        self.accent_policy.GradientColor = gradient_color
        self.accent_policy.AnimationId = animation_id
        self.set_win_comp_attr(int(h_wnd), pointer(self.win_comp_attr_data))

    def add_mica_effect(self, h_wnd: SupportsInt, dark_mode: bool = False):
        h_wnd = int(h_wnd)
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_ENABLE_HOSTBACKDROP.value
        self.set_win_comp_attr(h_wnd, pointer(self.win_comp_attr_data))

        if dark_mode:
            self.win_comp_attr_data.Attribute = (
                WINDOWCOMPOSITIONATTRIB.WCA_USEDARKMODECOLORS.value
            )
            self.set_win_comp_attr(h_wnd, pointer(self.win_comp_attr_data))
            self.win_comp_attr_data.Attribute = (
                WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
            )

        if sys.getwindowsversion().build >= 22523:
            self.dwm_set_win_attr(h_wnd, 38, byref(c_int(2)), 4)
        else:
            self.dwm_set_win_attr(h_wnd, 1029, byref(c_int(1)), 4)

    def remove_background_effect(self, h_wnd: SupportsInt):
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.set_win_comp_attr(int(h_wnd), pointer(self.win_comp_attr_data))

    def add_shadow_effect(self, h_wnd: SupportsInt):
        margins = MARGINS(-1, -1, -1, -1)
        self.dwm_ext_frame_into_client_area(int(h_wnd), byref(margins))

    def remove_shadow_effect(self, h_wnd: SupportsInt):
        self.dwm_set_win_attr(
            int(h_wnd),
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_DISABLED.value)),
            4,
        )

    @staticmethod
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
            | win32con.WS_THICKFRAME
            # | win32con.CS_DBLCLKS
            # | win32con.WS_POPUP
            # | win32con.WS_SYSMENU
        )

    def add_blur_behind_window(self, h_wnd: SupportsInt):
        blur_behind = DWM_BLURBEHIND(1, True, 0, False)
        self.dwm_enable_blur_behind_win(int(h_wnd), byref(blur_behind))
