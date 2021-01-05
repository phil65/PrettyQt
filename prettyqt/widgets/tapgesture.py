from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QTapGesture.__bases__ = (widgets.Gesture,)


class TapGesture(QtWidgets.QTapGesture):
    def get_position(self) -> core.PointF:
        return core.PointF(self.position())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = TapGesture()
