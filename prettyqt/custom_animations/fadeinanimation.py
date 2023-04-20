from __future__ import annotations

from collections.abc import Callable

from prettyqt import core
from prettyqt.qt import QtCore


class FadeInAnimation(core.PropertyAnimation):
    def __init__(
        self, duration: int = 1000, easing: core.easingcurve.TypeStr = "in_out_sine"
    ):
        super().__init__()
        self.set_easing(easing)
        self.setStartValue(0.0)
        self.setEndValue(1.0)
        self.setDuration(duration)

    def apply_to(self, obj: QtCore.QObject | Callable):
        if isinstance(obj, QtCore.QObject):
            obj = obj.windowOpacity
        super().apply_to(obj)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = FadeInAnimation()
    w = widgets.PushButton("Test")
    val.apply_to(w)
    val.start()
    w.show()
    app.main_loop()
