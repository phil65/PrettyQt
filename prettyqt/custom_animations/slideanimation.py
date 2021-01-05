from __future__ import annotations

from typing import Tuple, Union

from prettyqt import core
from prettyqt.qt import QtWidgets


class SlideAnimation(core.PropertyAnimation):
    def __init__(
        self, duration: int = 1000, easing: core.easingcurve.TypeStr = "in_out_sine"
    ):
        super().__init__()
        self.set_easing(easing)
        self.set_start_value(core.Point(0, 0))
        self.setDuration(duration)

    def set_start_value(self, point: Union[core.Point, Tuple[int, int]]):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setStartValue(point)

    def set_end_value(self, point: Union[core.Point, Tuple[int, int]]):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setEndValue(point)

    def apply_to(self, obj: QtWidgets.QWidget, attribute: str = "pos"):
        super().apply_to(obj, attribute)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = SlideAnimation()
