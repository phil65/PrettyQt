from __future__ import annotations

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

    def apply_to(self, obj: QtCore.QObject, attribute: str = "windowOpacity"):
        super().apply_to(obj, attribute)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    val = FadeInAnimation()
