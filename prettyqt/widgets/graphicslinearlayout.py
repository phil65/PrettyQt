from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets


class GraphicsLinearLayout(widgets.GraphicsLayoutMixin, QtWidgets.QGraphicsLinearLayout):
    def __init__(
        self,
        orientation: (constants.OrientationStr | QtCore.Qt.Orientation) = "horizontal",
        parent: QtWidgets.QGraphicsLayoutItem | None = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)

    def __add__(self, other):
        self[self.count()] = other
        return self


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsLinearLayout()
