# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets
from prettyqt.utils import bidict

TEXT_DIRECTIONS = bidict(top_to_bottom=QtWidgets.QProgressBar.TopToBottom,
                         bottom_to_top=QtWidgets.QProgressBar.BottomToTop)

ALIGNMENTS = bidict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    top=QtCore.Qt.AlignTop,
                    bottom=QtCore.Qt.AlignBottom)


QtWidgets.QProgressBar.__bases__ = (widgets.Widget,)


class ProgressBar(QtWidgets.QProgressBar):
    """Progress dialog

    wrapper for QtWidgets.QProgressBar
    """

    def __init__(self, text_visible=True, parent=None):
        super().__init__(parent=parent)
        self.setTextVisible(text_visible)

    def set_alignment(self, alignment: str):
        """set the alignment of the layout

        Allowed values are "left", "right", "top", "bottom"

        Args:
            mode: alignment for the layout

        Raises:
            ValueError: alignment does not exist
        """
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment!r} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])

    def get_alignment(self) -> str:
        """returns current alignment

        Possible values: "left", "right", "top", "bottom"

        Returns:
            alignment
        """
        return ALIGNMENTS.inv[self.alignment()]

    def set_text_direction(self, text_direction: str):
        """set the text direction of the layout

        Allowed values are "top_to_bottom", "bottom_to_top"

        Args:
            mode: text direction for the layout

        Raises:
            ValueError: text direction does not exist
        """
        if text_direction not in TEXT_DIRECTIONS:
            raise ValueError(f"{text_direction!r} not a valid text direction.")
        self.setTextDirection(TEXT_DIRECTIONS[text_direction])

    def get_text_direction(self) -> str:
        """returns current text direction

        Possible values are "top_to_bottom", "bottom_to_top"

        Returns:
            Text direction
        """
        return TEXT_DIRECTIONS.inv[self.textDirection()]

    def set_range(self, start, end):
        self.setRange(start, end)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ProgressBar()
    widget.show()
    app.exec_()
