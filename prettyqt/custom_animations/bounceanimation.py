from __future__ import annotations

from collections.abc import Callable

from prettyqt import core
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import datatypes


class BounceAnimation(core.SequentialAnimationGroup):
    ID = "bounce"

    def __init__(
        self,
        duration: int = 1000,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self.anim1 = core.PropertyAnimation()
        self.anim2 = core.PropertyAnimation()
        self.set_easing(easing)
        self.set_start_value(core.Point(0, 0))
        self.set_end_value(core.Point(0, 100))
        self.addAnimation(self.anim1)
        self.addAnimation(self.anim2)
        self.set_duration(duration)

    def set_start_value(self, point: datatypes.PointType):
        offset = datatypes.to_point(point)
        pos = self.parent().geometry().topLeft()
        self.anim1.setStartValue(pos + offset)
        self.anim2.setEndValue(pos + offset)

    def set_end_value(self, point: datatypes.PointType):
        offset = datatypes.to_point(point)
        pos = self.parent().geometry().topLeft()
        self.anim2.setStartValue(pos + offset)
        self.anim1.setEndValue(pos + offset)

    def set_duration(self, duration: int):
        self.anim1.setDuration(duration // 2)
        self.anim2.setDuration(duration // 2)

    def set_easing(self, easing: core.easingcurve.TypeStr):
        self.anim1.set_easing(easing)
        self.anim2.set_easing(easing)

    def apply_to(self, obj: QtWidgets.QWidget | Callable):
        if isinstance(obj, QtWidgets.QWidget):
            obj = obj.pos
        self.anim1.apply_to(obj)
        self.anim2.apply_to(obj)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = BounceAnimation()
    w = widgets.RadioButton()
    val.apply_to(w)
    val.start()
    w.show()
    app.main_loop()
