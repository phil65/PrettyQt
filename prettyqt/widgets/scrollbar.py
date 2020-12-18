from typing import Optional, Union

from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, widgets


QtWidgets.QScrollBar.__bases__ = (widgets.AbstractSlider,)


class ScrollBar(QtWidgets.QScrollBar):

    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: Union[
            QtCore.Qt.Orientation, constants.OrientationStr
        ] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)
        self.valueChanged.connect(self.on_value_change)
