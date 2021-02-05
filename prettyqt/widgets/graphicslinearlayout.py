from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets


QtWidgets.QGraphicsLinearLayout.__bases__ = (widgets.GraphicsLayout,)


class GraphicsLinearLayout(QtWidgets.QGraphicsLinearLayout):
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

    def serialize_fields(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        for i, (item, pos) in enumerate(zip(state["widgets"], state["positions"])):
            x, y = pos
            self[x, y] = item

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other):
        self[self.count()] = other
        return self


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsLinearLayout()
