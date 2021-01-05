from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QTapAndHoldGesture.__bases__ = (widgets.Gesture,)


class TapAndHoldGesture(QtWidgets.QTapAndHoldGesture):
    def get_position(self) -> core.PointF:
        return core.PointF(self.position())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = TapAndHoldGesture()
