# -*- coding: utf-8 -*-

from typing import Optional
from qtpy import QtCore, QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError


TEXT_DIRECTIONS = bidict(
    top_to_bottom=QtWidgets.QProgressBar.TopToBottom,
    bottom_to_top=QtWidgets.QProgressBar.BottomToTop,
)

ALIGNMENTS = bidict(
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
)


QtWidgets.QProgressBar.__bases__ = (widgets.Widget,)


class ProgressBar(QtWidgets.QProgressBar):
    """Progress dialog.

    wrapper for QtWidgets.QProgressBar
    """

    def __init__(
        self, text_visible: bool = True, parent: Optional[QtWidgets.QWidget] = None
    ):
        super().__init__(parent=parent)
        self.setTextVisible(text_visible)

    def set_alignment(self, alignment: str):
        """Set the alignment of the layout.

        Allowed values are "left", "right", "top", "bottom"

        Args:
            alignment: alignment for the layout

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in ALIGNMENTS:
            raise InvalidParamError(alignment, ALIGNMENTS)
        self.setAlignment(ALIGNMENTS[alignment])

    def get_alignment(self) -> str:
        """Return current alignment.

        Possible values: "left", "right", "top", "bottom"

        Returns:
            alignment
        """
        return ALIGNMENTS.inv[self.alignment()]

    def set_text_direction(self, text_direction: str):
        """Set the text direction of the layout.

        Allowed values are "top_to_bottom", "bottom_to_top"

        Args:
            text_direction: text direction for the layout

        Raises:
            InvalidParamError: text direction does not exist
        """
        if text_direction not in TEXT_DIRECTIONS:
            raise InvalidParamError(text_direction, TEXT_DIRECTIONS)
        self.setTextDirection(TEXT_DIRECTIONS[text_direction])

    def get_text_direction(self) -> str:
        """Return current text direction.

        Possible values are "top_to_bottom", "bottom_to_top"

        Returns:
            Text direction
        """
        return TEXT_DIRECTIONS.inv[self.textDirection()]

    def set_range(self, start: int, end: int):
        self.setRange(start, end)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ProgressBar()
    widget.show()
    app.exec_()
