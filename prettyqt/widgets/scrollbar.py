from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets


class ScrollBarMixin(widgets.AbstractSliderMixin):
    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: (QtCore.Qt.Orientation | constants.OrientationStr) = "horizontal",
        parent: QtWidgets.QWidget | None = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)
        self.valueChanged.connect(self.on_value_change)

    def scroll_to_next_row(self):
        """Scroll to the next row."""
        self.setValue(self.value() + self.singleStep())

    def scroll_to_previous_row(self):
        """Scroll to the previous row."""
        self.setValue(self.value() - self.singleStep())


class ScrollBar(ScrollBarMixin, QtWidgets.QScrollBar):
    pass
