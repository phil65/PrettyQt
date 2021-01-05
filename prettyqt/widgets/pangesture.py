from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QPanGesture.__bases__ = (widgets.Gesture,)


class PanGesture(QtWidgets.QPanGesture):
    def get_delta(self) -> core.PointF:
        return core.PointF(self.delta())

    def get_last_offset(self) -> core.PointF:
        return core.PointF(self.lastOffset())

    def get_offset(self) -> core.PointF:
        return core.PointF(self.offset())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = PanGesture()
