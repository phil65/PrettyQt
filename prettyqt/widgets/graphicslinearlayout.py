from typing import Optional, Union

from qtpy import QtCore, QtWidgets

from prettyqt import constants, widgets


QtWidgets.QGraphicsLinearLayout.__bases__ = (widgets.GraphicsLayout,)


class GraphicsLinearLayout(QtWidgets.QGraphicsLinearLayout):
    def __init__(
        self,
        orientation: Union[
            constants.OrientationStr, QtCore.Qt.Orientation
        ] = "horizontal",
        parent: Optional[QtWidgets.QGraphicsLayoutItem] = None,
    ):
        if isinstance(orientation, str) and orientation in constants.ORIENTATION:
            ori = constants.ORIENTATION[orientation]
        else:
            ori = orientation
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
