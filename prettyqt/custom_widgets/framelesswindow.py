# parts taken from https://github.com/mustafaahci/FramelessWindow

from __future__ import annotations

import ctypes
from ctypes.wintypes import LONG
import sys
from typing import Literal


try:
    import win32api
    from win32con import (
        GWL_STYLE,
        HTBOTTOM,
        HTBOTTOMLEFT,
        HTBOTTOMRIGHT,
        HTCAPTION,
        HTLEFT,
        HTRIGHT,
        HTTOP,
        HTTOPLEFT,
        HTTOPRIGHT,
        WM_NCCALCSIZE,
        WM_NCHITTEST,
        WS_CAPTION,
        WS_MAXIMIZEBOX,
        WS_MINIMIZEBOX,
        WS_POPUP,
        WS_SYSMENU,
        WS_THICKFRAME,
    )
    import win32gui
except ImportError:
    pass

from prettyqt import widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


SideStr = Literal["left", "top", "right", "bottom"]


class TitleBarIcon(widgets.PushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setStyleSheet(
            "margin: 0;" "padding: 0px;" "font-size: 16px;" "width: 44px;" "height: 30px;"
        )

        self.set_margin(0)


class CustomTitleBar(widgets.Frame):
    def __init__(self, window_widget: QtWidgets.QWidget):
        super().__init__(window_widget)

        self.window_widget = window_widget
        self.minimize_button = TitleBarIcon("🗕")
        self.maximize_button = TitleBarIcon("🗖")
        self.exit_button = TitleBarIcon("✕")
        self.setObjectName("ControlWidget")
        state = QtCore.Qt.WindowState.WindowMinimized
        self.minimize_button.clicked.connect(
            lambda: window_widget.setWindowState(state)  # type: ignore
        )
        self.maximize_button.clicked.connect(
            lambda: (
                window_widget.showNormal()
                if window_widget.isMaximized()
                else window_widget.showMaximized()
            )
        )
        self.exit_button.clicked.connect(window_widget.close)

        self.set_layout("horizontal")
        spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding)
        self.box.addSpacerItem(spacer_item)
        for widget in [
            self.minimize_button,
            self.maximize_button,
            self.exit_button,
        ]:
            self.box.addWidget(widget)

        self.setStyleSheet("width: 100%;" "padding: 0;" "margin: 0;")
        self.setContentsMargins(0, 0, 0, 0)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.window_widget.windowHandle().startSystemMove()


class FramelessWindow(widgets.Widget):
    BORDER_WIDTH = 5

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        # Remove window title bar and frame
        self.setWindowFlags(
            QtCore.Qt.WindowFlag.Window  # type: ignore
            | QtCore.Qt.WindowFlag.FramelessWindowHint
        )

        self.title_bar = CustomTitleBar(self)
        self.main_widget = widgets.MainWindow()

        # Set up layout
        self.main_layout = widgets.BoxLayout("vertical")
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.main_widget)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.grip_layout = widgets.GridLayout()

        self.grip_layout.addLayout(self.main_layout, 1, 1)
        self.grip_layout.addWidget(EdgeGrip("top"), 0, 1)
        self.grip_layout.addWidget(EdgeGrip("right"), 1, 2)
        self.grip_layout.addWidget(EdgeGrip("bottom"), 2, 1)
        self.grip_layout.addWidget(EdgeGrip("left"), 1, 0)
        self.grip_layout.addWidget(EdgeGrip("top_left"), 0, 0)
        self.grip_layout.addWidget(EdgeGrip("top_right"), 0, 2)
        self.grip_layout.addWidget(EdgeGrip("bottom_left"), 2, 0)
        self.grip_layout.addWidget(EdgeGrip("bottom_right"), 2, 2)
        self.grip_layout.setContentsMargins(0, 0, 0, 0)
        self.grip_layout.setSpacing(0)
        self.setLayout(self.grip_layout)

        if sys.platform == "win32":

            self.hwnd = self.winId().__int__()
            window_style = win32gui.GetWindowLong(self.hwnd, GWL_STYLE)
            win32gui.SetWindowLong(
                self.hwnd,
                GWL_STYLE,
                window_style
                | WS_POPUP
                | WS_THICKFRAME
                | WS_CAPTION
                | WS_SYSMENU
                | WS_MAXIMIZEBOX
                | WS_MINIMIZEBOX,
            )

            # if QtWin.isCompositionEnabled():
            #     # Aero Shadow
            #     QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
            # else:
            #     QtWin.resetExtendedFrame(self)

    def __getattr__(self, attr: str):
        return getattr(self.main_widget, attr)

    def changeEvent(self, event):
        # not sure if this should be done on non-windows
        if event.type() == event.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowState.WindowMaximized:  # type: ignore
                margin = abs(self.mapToGlobal(self.rect().topLeft()).y())
                self.setContentsMargins(margin, margin, margin, margin)
            else:
                self.setContentsMargins(0, 0, 0, 0)

        return super().changeEvent(event)

    def nativeEvent(self, event, message):
        return_value, result = super().nativeEvent(event, message)
        if sys.platform != "win32":
            return return_value, result
        # if you use Windows OS
        if event == b"windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # Get the coordinates when the mouse moves.
            x = win32api.LOWORD(LONG(msg.lParam).value)  # type: ignore
            # converted an unsigned int to int (for dual monitor issue)
            if x & 32768:
                x = x | -65536
            y = win32api.HIWORD(LONG(msg.lParam).value)  # type: ignore
            if y & 32768:
                y = y | -65536

            x -= self.frameGeometry().x()
            y -= self.frameGeometry().y()

            # Determine whether there are other widgets at the mouse position.
            if self.childAt(x, y) is not None and self.childAt(
                x, y
            ) is not self.findChild(widgets.Widget, "ControlWidget"):
                # passing
                if (
                    self.width() - self.BORDER_WIDTH > x > self.BORDER_WIDTH
                    and y < self.height() - self.BORDER_WIDTH
                ):
                    return return_value, result

            if msg.message == WM_NCCALCSIZE:
                # Remove system title
                return True, 0

            if msg.message == WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BORDER_WIDTH
                rx = x > w - self.BORDER_WIDTH
                ty = y < self.BORDER_WIDTH
                by = y > h - self.BORDER_WIDTH
                if lx and ty:
                    return True, HTTOPLEFT
                if rx and by:
                    return True, HTBOTTOMRIGHT
                if rx and ty:
                    return True, HTTOPRIGHT
                if lx and by:
                    return True, HTBOTTOMLEFT
                if ty:
                    return True, HTTOP
                if by:
                    return True, HTBOTTOM
                if lx:
                    return True, HTLEFT
                if rx:
                    return True, HTRIGHT
                # Title
                return True, HTCAPTION

        return return_value, result


class EdgeGrip(widgets.Widget):
    def __init__(self, edges: str, grip_size=6, parent=None):
        super().__init__(parent)
        self.edges = edges
        self.grip_size = grip_size
        # Sides
        if edges == "top":
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.setFixedHeight(self.grip_size)
        elif edges == "right":
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.setFixedWidth(self.grip_size)
        elif edges == "bottom":
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.setFixedHeight(self.grip_size)
        elif edges == "left":
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.setFixedWidth(self.grip_size)
        # Corners
        elif edges == "top_left":
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif edges == "top_right":
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif edges == "bottom_left":
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif edges == "bottom_right":
            self.setCursor(QtCore.Qt.SizeFDiagCursor)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.parent().windowHandle().startSystemResize(self.edges)


if __name__ == "__main__":
    app = widgets.app()
    m = FramelessWindow()
    button = widgets.PushButton("test")
    m.set_widget(button)
    m.show()
    m.resize(240, 160)
    app.main_loop()
