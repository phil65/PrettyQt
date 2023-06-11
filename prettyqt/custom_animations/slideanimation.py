from __future__ import annotations

from collections.abc import Callable

from prettyqt import core
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import datatypes


class SlideAnimation(core.PropertyAnimation):
    ID = "slide"

    def __init__(
        self,
        duration: int = 1000,
        start: tuple[int, int] | core.Point = (0, 0),
        end: tuple[int, int] | core.Point = (0, 0),
        easing: core.easingcurve.TypeStr = "in_out_sine",
        parent: QtCore.QObject | None = None,
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
    val = SlideAnimation()
    val.set_end_value((100, 100))
    btn = widgets.PushButton("ts")
    btn.show()
    val.apply_to(btn)
    val.start()
    app.main_loop()
