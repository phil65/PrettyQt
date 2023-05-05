import ctypes
from ctypes.wintypes import HBITMAP, HICON, LPCWSTR, RECT  # , HWND
import enum
import logging
from typing import Literal, SupportsInt

import comtypes.client as cc
import comtypes.gen.TaskbarLib as tbl


# from comtypes.gen import _683BF642_E9CA_4124_BE43_67065B2FA653_0_1_0


logger = logging.getLogger(__name__)
cc.GetModule("./TaskbarLib.tlb")

taskbar = cc.CreateObject(
    "{56FDF344-FD6D-11d0-958A-006097C9A090}", interface=tbl.ITaskbarList3
)
dwmapi = ctypes.WinDLL("dwmapi")
taskbar.HrInit()


class State(enum.IntEnum):
    no_progress = 0
    indeterminate = 1
    normal = 2
    error = 4
    paused = 8


class TaskBarItem:
    def __init__(self, hwnd: SupportsInt | None = None):
        self.state = "normal"
        self.progress = 0
        self.tabs = []
        if hwnd is None:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            taskbar.ActivateTab(hwnd)
        self.win_id = int(hwnd)

    def set_progress_state(
        self,
        value: Literal[
            "no_progress", "indeterminate", "normal", "error", "paused", "done"
        ],
    ):
        match value:
            case "no_progress":
                taskbar.SetProgressState(self.win_id, State.no_progress)
                self.state = "no_progress"
            case "indeterminate":
                taskbar.SetProgressState(self.win_id, State.indeterminate)
                self.state = "indeterminate"
            case "normal":
                taskbar.SetProgressState(self.win_id, State.normal)
                self.state = "normal"
            case "error":
                taskbar.SetProgressState(self.win_id, State.error)
                self.state = "error"
            case "paused":
                taskbar.SetProgressState(self.win_id, State.paused)
                self.state = "paused"
            case "done":
                ctypes.windll.user32.FlashWindow(self.win_id, True)
                self.set_progress_state("no_progress")
            case _:
                raise ValueError(value)

    def set_progress_value(self, value: int, total: int = 100):
        if value > 100 or value < 0 or value > total:
            raise ValueError(value)
        result = taskbar.setProgressValue(self.win_id, value, total)
        return bool(result)

    def activate_tab(self):
        logger.info(f"Activate tab {self.win_id}")
        result = taskbar.ActivateTab(self.win_id)
        return bool(result)

    def set_thumbnail_clip(self, rect: tuple[int, int, int, int]) -> bool:
        logger.info(f"Set thumnail clip to {rect!r} for handle {self.win_id}")
        area = RECT(*rect)
        result = taskbar.SetThumbnailClip(self.win_id, area)
        return bool(result)

    def set_thumbnail_tooltip(self, tooltip: str) -> bool:
        logger.info(f"Set thumnail tooltip {tooltip!r} for handle {self.win_id}")
        result = taskbar.SetThumbnailTooltip(self.win_id, LPCWSTR(tooltip))
        return bool(result)

    def register_tab(self, tab_win_id: SupportsInt):
        tab_win_id = int(tab_win_id)
        logger.info(f"Register tab {tab_win_id} in handle {self.win_id}")
        result = taskbar.RegisterTab(tab_win_id, self.win_id)
        taskbar.SetTabOrder(tab_win_id, 0)
        # self.set_window_attribute(7, True)
        self.tabs.append(tab_win_id)
        return bool(result)

    def unregister_tab(self, tab_win_id: SupportsInt):
        tab_win_id = int(tab_win_id)
        # if tab_win_id not in self.tabs:
        #     raise ValueError(f"no handle with {tab_win_id} registered.")
        logger.info(f"Register tab {tab_win_id}")
        result = taskbar.UnregisterTab(tab_win_id)
        self.tabs.remove(tab_win_id)
        return bool(result)

    def set_tab_active(self, tab_win_id: SupportsInt):
        tab_win_id = int(tab_win_id)
        logger.info(f"Set tab {tab_win_id} for handle {self.win_id} active")
        result = taskbar.SetTabActive(tab_win_id, self.win_id, 0)
        return bool(result)

    def set_overlay_icon(self, icon, description: str = ""):
        logger.info(f"Set overlay icon for {self.win_id}")

        # CreateIconFromResourceEx = windll.user32.CreateIconFromResourceEx
        # size_x, size_y = 32, 32
        # LR_DEFAULTCOLOR = 0

        # with open(png_path, "rb") as f:
        #     png = f.read()
        # hicon = CreateIconFromResourceEx(
        #     png, len(png), 1, 0x30000, size_x, size_y, LR_DEFAULTCOLOR
        # )

        overlay_icon = HICON(icon)
        accessible_name = LPCWSTR(description)
        result = taskbar.SetOverlayIcon(self.win_id, overlay_icon, accessible_name)
        return bool(result)

    def set_iconic_live_preview_bitmap(self, bitmap: HBITMAP):  # available via QImage
        logger.info(f"Set iconic live preview for {self.win_id}")
        dwmapi.DwmSetIconicLivePreviewBitmap(self.win_id, bitmap, 0)

    def set_iconic_thumbnail(self, thumbnail: HBITMAP):  # available via QImage
        logger.info(f"Set iconic thumbnail for {self.win_id}")
        # SM_CXSMICON = 49
        # SM_CYSMICON = 50
        # ico_x = GetSystemMetrics(SM_CXSMICON)
        # ico_y = GetSystemMetrics(SM_CYSMICON)
        # icon = encode_for_locale(self._icon)
        # hicon = LoadImageA(0, icon, IMAGE_ICON, ico_x, ico_y, LR_LOADFROMFILE)
        # dwmapi.DwmSetIconicThumbnail(self.win_id, HBITMAP(thumbnail), 0)

    def set_window_attribute(self, key, value):  # available via QImage
        logger.info(f"Set iconic thumbnail for {self.win_id}")
        dwmapi.DwmSetWindowAttribute(
            self.win_id,
            key,  # DWMWA_FORCE_ICONIC_REPRESENTATION = 7
            # DWMWA_HAS_ICONIC_BITMAP = 10
            ctypes.byref(ctypes.c_bool(value)),
            ctypes.sizeof(ctypes.c_bool(value)),
        )


if __name__ == "__main__":
    import time

    prog = TaskBarItem()
    prog.set_iconic_live_preview_bitmap(HBITMAP())
    print("state indeterminate")
    prog.set_progress_state("indeterminate")
    prog.set_thumbnail_tooltip("jkfdsjfkjk")
    prog.set_thumbnail_clip((0, 20, 50, 80))
    time.sleep(5)
    # print("state normal, set progress")
    # prog.set_progress_state("normal")

    # for i in range(100):
    #     prog.set_progress_value(i)
    #     time.sleep(0.05)
    # print("state paused, set progress")
    # prog.set_progress_value(0)

    # prog.set_progress_state("paused")

    # for i in range(100):
    #     prog.set_progress_value(i)
    #     time.sleep(0.05)

    # print("state error, set progress")
    # prog.set_progress_value(0)
    # prog.set_progress_state("error")

    # for i in range(100):
    #     prog.set_progress_value(i)
    #     time.sleep(0.05)

    # print("state done.")
    # prog.set_progress_value(0)

    # prog.set_progress_state("done")
    # time.sleep(3)
