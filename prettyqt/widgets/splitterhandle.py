from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QSplitterHandle.__bases__ = (widgets.Widget,)


class SplitterHandle(QtWidgets.QSplitterHandle):
    def __init__(
        self,
        orientation: constants.OrientationStr | QtCore.Qt.Orientation,
        parent: QtWidgets.QSplitter,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)

    def set_orientation(self, orientation: constants.OrientationStr):
        """Set the orientation of the slider.

        Args:
            orientation: orientation for the slider

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.setOrientation(constants.ORIENTATION[orientation])

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Splitter()
    handle = SplitterHandle("horizontal", w)
    handle.show()
    app.main_loop()
