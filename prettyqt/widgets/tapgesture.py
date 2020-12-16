from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QTapGesture.__bases__ = (widgets.Gesture,)


class TapGesture(QtWidgets.QTapGesture):
    def get_position(self) -> core.PointF:
        return core.PointF(self.position())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = TapGesture()
