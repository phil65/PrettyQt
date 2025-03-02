from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes


if TYPE_CHECKING:
    from collections.abc import Callable


class SlideAnimation(core.PropertyAnimation):
    ID = "slide"

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        duration: int = 1000,
        start: tuple[int, int] | core.Point = (0, 0),
        end: tuple[int, int] | core.Point = (0, 0),
        easing: core.easingcurve.TypeStr = "in_out_sine",
    ):
        super().__init__(parent)
        self.set_easing(easing)
        self.set_start_value(start)
        self.set_end_value(end)
        self.setDuration(duration)

    def set_start_value(self, point: datatypes.PointType):
        offset = datatypes.to_point(point)
        pos = self.parent().geometry().topLeft()
        self.setStartValue(pos + offset)

    def set_end_value(self, point: datatypes.PointType):
        offset = datatypes.to_point(point)
        pos = self.parent().geometry().topLeft()
        self.setEndValue(pos + offset)

    def apply_to(self, obj: QtWidgets.QWidget | Callable):
        if isinstance(obj, QtWidgets.QWidget):
            obj = obj.pos
        super().apply_to(obj)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    btn = widgets.PushButton("ts")
    btn.show()
    val = SlideAnimation(parent=btn)
    val.set_end_value((0, 100))
    val.apply_to(btn)
    val.start()
    app.exec()
