from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


class BounceAnimation(core.SequentialAnimationGroup):
    def __init__(
        self, duration: int = 1000, easing: core.easingcurve.TypeStr = "in_out_sine"
    ):
        super().__init__()
        self.anim1 = core.PropertyAnimation()
        self.anim2 = core.PropertyAnimation()
        self.set_easing(easing)
        self.set_start_value((0, 0))
        # self.set_end_value(core.Point(0, 100))
        self.addAnimation(self.anim1)
        self.addAnimation(self.anim2)
        self.set_duration(duration)

    def set_start_value(self, point: types.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.anim1.setStartValue(point)
        self.anim2.setEndValue(point)

    def set_end_value(self, point: types.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.anim2.setStartValue(point)
        self.anim1.setEndValue(point)

    def set_duration(self, duration: int):
        self.anim1.setDuration(duration // 2)
        self.anim2.setDuration(duration // 2)

    def set_easing(self, easing: core.easingcurve.TypeStr):
        self.anim1.set_easing(easing)
        self.anim2.set_easing(easing)

    def apply_to(self, obj: QtWidgets.QWidget):
        self.anim1.apply_to(obj, "pos")
        self.anim2.apply_to(obj, "pos")


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = BounceAnimation()
