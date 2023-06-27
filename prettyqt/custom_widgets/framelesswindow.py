from __future__ import annotations

from ctypes import cast
from ctypes.wintypes import MSG, LPRECT
from enum import Enum
from sys import getwindowsversion

import win32con
from ctypes import Structure, c_int, POINTER
from ctypes.wintypes import HWND, UINT, RECT

from prettyqt import core, constants, gui, widgets
from prettyqt.qt import QtCore, QtGui

from prettyqt.utils.platforms.windows import misc, windoweffects


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


def invert_color(color: str) -> str:
    inverted_color = ""
    for i in range(0, 5, 2):
        channel = int(color[i : i + 2], base=16)
        inverted_color += hex(round(channel / 6))[2:].upper().zfill(2)
    inverted_color += color[-2:]
    return inverted_color


def get_resize_border_thickness(h_wnd):
    window = gui.GuiApplication.find_window(h_wnd)
    if not window:
        return 0
    thickness = misc.get_border_thickness()
    return round(thickness * window.devicePixelRatio())


class CustomBase(widgets.Widget):
    def __init__(
        self, use_mica: bool = False, theme: str = "auto", color: str = "F0F0F0A0"
    ):
        """Customizable window without titlebar.

        Parameters
        ----------
        use_mica: 'bool
            Use mica or acrylic effect, (Mica Win11 only)
        theme: 'auto', 'dark', 'light'
            Use dark, light or system theme
        color: str
            Window background color
        """
        super().__init__()
        self.is_win11 = getwindowsversion().build >= 22000
        self.use_mica = use_mica if self.is_win11 else False
        match theme:
            case "auto":
                self.dark_mode = self.get_palette().is_dark()
            case "dark":
                self.dark_mode = True
            case "light":
                self.dark_mode = False
            case _:
                raise ValueError(theme)
        if len(color) != 8:
            raise ValueError("Wrong argument 'color': must be 8 hex symbols")
        self.acrylic_color = invert_color(color) if self.dark_mode else color
        self.effect_enabled = False
        self.win_effects = windoweffects.WindowsEffects()
        self.win_effects.add_window_animation(self.winId())
        self.setWindowFlags(constants.WindowType.FramelessWindowHint)
        self.win_effects.add_window_animation(self.winId())
        self.set_effect()
        if self.is_win11:
            self.win_effects.add_blur_behind_window(self.winId())
            self.win_effects.add_shadow_effect(self.winId())
        self.setStyleSheet("CustomBase{ background:transparent; }")

        self._effect_timer = core.Timer(self, interval=100, single_shot=True)
        self._effect_timer.timeout.connect(self.set_effect)

    def set_effect(self, enable: bool = True):
        if self.effect_enabled == enable:
            return
        self.effect_enabled = enable
        if enable and self.use_mica:
            self.win_effects.add_mica_effect(self.winId(), self.dark_mode)
        elif enable:
            self.win_effects.add_acrylic_effect(self.winId(), self.acrylic_color)
        else:
            self.win_effects.remove_background_effect(self.winId())
        self.update()

    def _temporary_disable_effect(self):
        self.set_effect(False)
        self._effect_timer.stop()
        self._effect_timer.start()

    def moveEvent(self, event):
        if self.is_win11 or not self._effect_timer:
            return super().moveEvent(event)
        self._temporary_disable_effect()

    def paintEvent(self, event):
        if self.effect_enabled:
            return super().paintEvent(event)
        with gui.Painter(self) as painter:
            painter.setOpacity(0.8)
            if self.dark_mode:
                painter.setBrush(constants.GlobalColor.black)
            else:
                painter.setBrush(constants.GlobalColor.white)
            painter.drawRect(self.rect())

    def nativeEvent(self, event_type, message):
        msg = MSG.from_address(int(message))
        if not msg.hWnd:
            return False, 0
        if msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            is_max = misc.is_maximized(msg.hWnd)
            is_full = misc.is_full_screen(msg.hWnd)

            # Adjust the size of client rect
            if is_max and not is_full:
                thickness = misc.get_resize_border_thickness(msg.hWnd)
                rect.top += thickness
                rect.left += thickness
                rect.right -= thickness
                rect.bottom -= thickness

            # Handle the situation that an auto-hide taskbar is enabled
            if (is_max or is_full) and misc.Taskbar.is_auto_hide():
                match misc.Taskbar.get_position(msg.hWnd):
                    case misc.Taskbar.LEFT:
                        rect.top += misc.Taskbar.AUTO_HIDE_THICKNESS
                    case misc.Taskbar.BOTTOM:
                        rect.bottom -= misc.Taskbar.AUTO_HIDE_THICKNESS
                    case misc.Taskbar.LEFT:
                        rect.left += misc.Taskbar.AUTO_HIDE_THICKNESS
                    case misc.Taskbar.RIGHT:
                        rect.right -= misc.Taskbar.AUTO_HIDE_THICKNESS

            res = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, res

        return False, 0


class TitleBarButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class TitleBarButton(widgets.ToolButton):
    def __init__(self, parent, dark_mode: bool):
        super().__init__(parent)
        if dark_mode:
            color = "FFFFFF"
            self._icon_color = constants.GlobalColor.white
        else:
            color = "000000"
            self._icon_color = constants.GlobalColor.black
        self.colors = "transparent", f"#20{color}", f"#40{color}"
        self._style = """
        border: none;
        margin: 0px;
        """
        self._state = TitleBarButtonState.NORMAL
        self.set_state(TitleBarButtonState.NORMAL)
        self.setFixedSize(46, 32)

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        self.setStyleSheet(
            f"background-color: {self.colors[state.value]};\n{self._style}"
        )

    def enterEvent(self, e):
        self.set_state(TitleBarButtonState.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.set_state(TitleBarButtonState.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == constants.MouseButton.LeftButton:
            self.set_state(TitleBarButtonState.PRESSED)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.set_state(TitleBarButtonState.HOVER)
        super().mouseReleaseEvent(e)


class MinimizeButton(TitleBarButton):
    def paintEvent(self, event):
        super().paintEvent(event)
        with gui.Painter(self) as painter:
            pen = QtGui.QPen(self._icon_color)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    def __init__(self, parent, dark_mode):
        super().__init__(parent, dark_mode)
        self.is_max = False

    def paintEvent(self, event):
        super().paintEvent(event)
        with gui.Painter(self) as painter:
            pen = QtGui.QPen(self._icon_color)
            pen.setCosmetic(True)
            painter.setPen(pen)

            r = self.devicePixelRatioF()
            painter.scale(1 / r, 1 / r)
            if not self.is_max:
                painter.drawRect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
            else:
                r_18, r_8 = int(18 * r), int(8 * r)
                painter.drawRect(r_18, int(13 * r), r_8, r_8)
                x0 = r_18 + int(2 * r)
                y0 = 13 * r
                dw = int(2 * r)
                path = gui.PainterPath(QtCore.QPointF(x0, y0))
                path.lineTo(x0, y0 - dw)
                path.lineTo(x0 + 8 * r, y0 - dw)
                path.lineTo(x0 + 8 * r, y0 - dw + 8 * r)
                path.lineTo(x0 + 8 * r - dw, y0 - dw + 8 * r)
                painter.drawPath(path)


class CloseButton(TitleBarButton):
    def __init__(self, parent, dark_mode):
        super().__init__(parent, dark_mode)
        self._dark_mode = dark_mode
        self.colors = "transparent", "#C42B1C", "#C83C30"
        self.set_state(TitleBarButtonState.NORMAL)
        self._white_icon = gui.Icon(r"prettyqt\resources\close_white.svg")
        if self._dark_mode:
            self.setIcon(self._white_icon)
        else:
            self._black_icon = gui.Icon(r"prettyqt\resources\close_black.svg")
            self.setIcon(self._black_icon)
        self.setIconSize(QtCore.QSize(46, 32))

    def enterEvent(self, event):
        if not self._dark_mode:
            self.setIcon(self._white_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self._dark_mode:
            self.setIcon(self._black_icon)
        super().leaveEvent(event)


class TitleBar(widgets.Widget):
    def __init__(self, parent, dark_mode):
        super().__init__(parent)
        self.setFixedHeight(32)

        self.icon = widgets.Label(self)
        self.title = widgets.Label(self)
        self.min_btn = MinimizeButton(self, dark_mode)
        self.max_btn = MaximizeButton(self, dark_mode)
        self.close_btn = CloseButton(self, dark_mode)
        self.h_box_layout = widgets.HBoxLayout(self, spacing=0, margin=0)

        if dark_mode:
            self.title.setStyleSheet("color: white")
        self.icon.setFixedSize(10, 16)

        self.h_box_layout.addWidget(self.icon)
        self.h_box_layout.addWidget(self.title)
        self.h_box_layout.addWidget(self.min_btn)
        self.h_box_layout.addWidget(self.max_btn)
        self.h_box_layout.addWidget(self.close_btn)

        self.min_btn.clicked.connect(self.window().showMinimized)
        self.max_btn.clicked.connect(self.__toggle_max_state)
        self.close_btn.clicked.connect(self.window().close)

    def __toggle_max_state(self):
        is_max = self.window().isMaximized()
        self.max_btn.is_max = not is_max
        if is_max:
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mouseDoubleClickEvent(self, event):
        if event.button() == constants.MouseButton.LeftButton:
            self.__toggle_max_state()

    def mouseMoveEvent(self, event):
        if not event.pos().x() < self.width() - 46 * 3:
            return
        win_id = self.window().winId()
        misc.start_system_move(win_id)


class FramelessWindow(CustomBase):
    BORDER_WIDTH = 4

    def __init__(self, use_mica=True, theme="auto", color="F2F2F299"):
        """Customizable window with custom titlebar.

        Parameters
        ----------
        use_mica: 'false', 'true', 'if available'
            Use mica or acrylic effect,
            'if available' mode will select according to the current OS
        theme: 'auto', 'dark', 'light'
            Use dark, light or system theme
        color: str
            Window background color
        """
        self._max_btn_hovered = False
        self.title_bar = None
        super().__init__(use_mica, theme, color)
        self.title_bar = TitleBar(self, self.dark_mode)
        self.setContentsMargins(0, 32, 0, 0)

    def setWindowTitle(self, title):
        self.title_bar.title.setText(title)
        super().setWindowTitle(title)

    def setWindowIcon(self, icon):
        self.title_bar.icon.setFixedWidth(32)
        self.title_bar.icon.setAlignment(constants.AlignmentFlag.AlignHCenter)
        self.title_bar.icon.setPixmap(icon.pixmap(16, 16))
        super().setWindowIcon(icon)

    def resizeEvent(self, event):
        if not self.title_bar:  # if not initialized
            return
        self.title_bar.setFixedWidth(self.width())
        if not self.use_mica:
            self._temporary_disable_effect()

    def nativeEvent(self, event_type, message):
        msg = MSG.from_address(int(message))
        if not msg.hWnd:
            return False, 0
        if msg.message == win32con.WM_NCHITTEST:
            pos = gui.Cursor.pos()
            x = pos.x() - self.x()
            y = pos.y() - self.y()
            if (
                self.is_win11
                and self.title_bar.childAt(pos - self.geometry().topLeft())
                is self.title_bar.max_btn
            ):
                self._max_btn_hovered = True
                self.title_bar.max_btn.set_state(TitleBarButtonState.HOVER)
                return True, win32con.HTMAXBUTTON
            lx = x < self.BORDER_WIDTH
            rx = x > self.width() - self.BORDER_WIDTH
            ty = y < self.BORDER_WIDTH
            by = y > self.height() - self.BORDER_WIDTH
            if rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx:
                return True, win32con.HTRIGHT
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif ty:
                return True, win32con.HTTOP
        elif self.is_win11 and self._max_btn_hovered:
            max_btn_state = self.title_bar.max_btn.get_state()
            match msg.message:
                case win32con.WM_NCLBUTTONDOWN:
                    self.title_bar.max_btn.set_state(TitleBarButtonState.PRESSED)
                    return True, 0
                case win32con.WM_NCLBUTTONUP | win32con.WM_NCRBUTTONUP:
                    self.title_bar.max_btn.click()
                case 0x2A2 | win32con.WM_MOUSELEAVE if max_btn_state != 0:
                    self._max_btn_hovered = False
                    self.title_bar.max_btn.set_state(TitleBarButtonState.NORMAL)

        return super().nativeEvent(event_type, message)


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("Fusion")
    win = FramelessWindow()
    win.setWindowTitle("Thsi is  a tesxt")
    win.show()
    app.exec()
