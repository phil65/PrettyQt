from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtWidgets


AnchorStr = Literal["center", "top", "left", "right", "bottom"]


class ZoomAnimation(core.ParallelAnimationGroup):
    ID = "zoom"

    def __init__(
        self,
        duration: int = 1000,
        start: float = 1.0,
        end: float = 1.0,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        anchor: AnchorStr = "center",
        parent: QtCore.QObject | None = None,
    ):
        self._start = start
        self._end = end
        self._anchor = anchor
        super().__init__(parent)
        # size change animation
        self.anim1 = core.PropertyAnimation()
        # slide animation
        self.anim2 = core.PropertyAnimation()
        self.apply_to(parent)
        self.set_easing(easing)
        self.set_start_value(start)
        self.set_end_value(end)
        self.set_duration(duration)
        self.addAnimation(self.anim1)
        self.addAnimation(self.anim2)

    def set_start_value(self, factor: float):
        size = self.parent().size()
        self._start = factor
        self.anim1.setStartValue(size)
        self.anim2.setStartValue(self.parent().pos())

    def set_end_value(self, factor: float):
        self._end = factor
        zoom_ratio = self._end / self._start
        # setup zoom
        size = self.parent().size()
        new = size.toSizeF() * zoom_ratio * zoom_ratio
        self.anim1.setEndValue(new.toSize())
        # setup move
        move_x = -zoom_ratio * self.parent().width()
        move_y = -zoom_ratio * self.parent().height()
        match self._anchor:
            case "center":
                movement = core.Point(int(move_x / 2), int(move_y / 2))
            case "left":
                movement = core.Point(0, int(move_y / 2))
            case "right":
                movement = core.Point(int(move_x), int(move_y / 2))
            case "top":
                movement = core.Point(int(move_x / 2), 0)
            case "bottom":
                movement = core.Point(int(move_x / 2), int(move_y))
        self.anim2.setEndValue(self.parent().pos() + movement)

    def set_duration(self, duration: int):
        self.anim1.setDuration(duration)
        self.anim2.setDuration(duration)

    def set_easing(self, easing: core.easingcurve.TypeStr | core.QEasingCurve.Type):
        self.anim1.set_easing(easing)
        self.anim2.set_easing(easing)

    def apply_to(self, obj: QtWidgets.QWidget):
        self.anim1.apply_to(obj.size)
        self.anim2.apply_to(obj.pos)

    def start(self, *args, **kwargs):
        # update values before starting
        self.set_start_value(self._start)
        self.set_end_value(self._end)
        super().start(*args, **kwargs)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = ZoomAnimation()
    w = widgets.RadioButton()
    val.apply_to(w)
    val.start()
    w.show()
    app.exec()
