from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import types


class SlideAnimation(core.PropertyAnimation):
    def __init__(
        self, duration: int = 1000, easing: core.easingcurve.TypeStr = "in_out_sine"
    ):
        super().__init__()
        self.set_easing(easing)
        self.set_start_value(core.Point(0, 0))
        self.setDuration(duration)

    def set_start_value(self, point: types.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setStartValue(point)

    def set_end_value(self, point: types.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setEndValue(point)

    def apply_to(self, obj: QtCore.QObject, attribute: str = "pos"):
        super().apply_to(obj, attribute)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = SlideAnimation()
