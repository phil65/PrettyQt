from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


class GraphicsLinearLayout(widgets.GraphicsLayoutMixin, QtWidgets.QGraphicsLinearLayout):
    def __init__(
        self,
        orientation: constants.OrientationStr | constants.Orientation = "horizontal",
        parent: QtWidgets.QGraphicsLayoutItem | None = None,
    ):
        ori = constants.ORIENTATION.get_enum_value(orientation)
        super().__init__(ori, parent)

    def __add__(self, other):
        self[self.count()] = other
        return self


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsLinearLayout()
