from __future__ import annotations

from typing import List, Literal, Optional

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtWidgets


SideStr = Literal["left", "top", "right", "bottom"]


class SideGrip(widgets.Widget):
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget],
        edge: SideStr,
    ):
        super().__init__(parent=parent)
        if edge == "left":
            self.set_cursor("size_horizonal")
            self.resize_fn = self.resize_left
        elif edge == "top":
            self.set_cursor("size_vertical")
            self.resize_fn = self.resize_top
        elif edge == "right":
            self.set_cursor("size_horizonal")
            self.resize_fn = self.resize_right
        else:
            self.set_cursor("size_vertical")
            self.resize_fn = self.resize_bottom
        self.mouse_pos = None

    def resize_left(self, delta: QtCore.QPoint):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resize_top(self, delta: QtCore.QPoint):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resize_right(self, delta: QtCore.QPoint):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resize_bottom(self, delta: QtCore.QPoint):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_pos is not None:
            delta = event.pos() - self.mouse_pos
            self.resize_fn(delta)

    def mouseReleaseEvent(self, event):
        self.mouse_pos = None


class FramelessWindow(widgets.MainWindow):
    _grip_size = 4

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent=parent)
        self.set_flags(frameless=True)
        sides: List[SideStr] = ["left", "top", "right", "bottom"]
        self.side_grips = [SideGrip(self, side) for side in sides]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.corner_grips = [widgets.SizeGrip(self) for i in range(4)]
        self.set_margin(self.grip_size)

    @property
    def grip_size(self) -> int:
        return self._grip_size

    def set_grip_size(self, size: int):
        if size == self._grip_size:
            return
        self._grip_size = max(2, size)
        self.set_margin(self.grip_size)
        self.update_grips()

    def update_grips(self):
        outer = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inner = outer.adjusted(
            self.grip_size, self.grip_size, -self.grip_size, -self.grip_size
        )

        # top left
        rect = core.Rect(outer.topLeft(), inner.topLeft())
        self.corner_grips[0].setGeometry(rect)
        # top right
        rect = core.Rect(outer.topRight(), inner.topRight()).normalized()
        self.corner_grips[1].setGeometry(rect)
        # bottom right
        rect = core.Rect(inner.bottomRight(), outer.bottomRight())
        self.corner_grips[2].setGeometry(rect)
        # bottom left
        rect = core.Rect(outer.bottomLeft(), inner.bottomLeft()).normalized()
        self.corner_grips[3].setGeometry(rect)

        # left edge
        self.side_grips[0].setGeometry(0, inner.top(), self.grip_size, inner.height())
        # top edge
        self.side_grips[1].setGeometry(inner.left(), 0, inner.width(), self.grip_size)
        # right edge
        self.side_grips[2].setGeometry(
            inner.right(),
            inner.top(),
            self.grip_size,
            inner.height(),
        )
        # bottom edge
        self.side_grips[3].setGeometry(
            self.grip_size,
            inner.bottom(),
            inner.width(),
            self.grip_size,
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grips()


if __name__ == "__main__":
    app = widgets.app()
    m = FramelessWindow()
    button = widgets.PushButton("test")
    m.set_widget(button)
    m.show()
    m.resize(240, 160)
    app.exec_()
