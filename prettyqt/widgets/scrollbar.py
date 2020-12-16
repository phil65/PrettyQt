from typing import Optional, Union

from qtpy import QtWidgets

from prettyqt import constants, core, widgets


QtWidgets.QScrollBar.__bases__ = (widgets.AbstractSlider,)


class ScrollBar(QtWidgets.QScrollBar):

    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: Union[int, constants.OrientationStr] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in constants.ORIENTATION:
            orientation = constants.ORIENTATION[orientation]
        super().__init__(orientation, parent)
        self.valueChanged.connect(self.on_value_change)
