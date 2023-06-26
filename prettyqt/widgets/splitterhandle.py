from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets


class SplitterHandle(widgets.WidgetMixin, QtWidgets.QSplitterHandle):
    double_clicked = core.Signal(object)

    def __init__(
        self,
        orientation: constants.OrientationStr | QtCore.Qt.Orientation,
        parent: QtWidgets.QSplitter,
        **kwargs,
    ):
        ori = (
            constants.ORIENTATION[orientation]
            if isinstance(orientation, str)
            else orientation
        )
        super().__init__(ori, parent, **kwargs)

    def mouseDoubleClickEvent(self, ev):
        self.double_clicked.emit(self)

    def set_orientation(
        self, orientation: constants.OrientationStr | constants.Orientation
    ):
        """Set the orientation of the slider.

        Args:
            orientation: orientation for the slider
        """
        self.setOrientation(constants.ORIENTATION.get_enum_value(orientation))

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
    app.exec()
