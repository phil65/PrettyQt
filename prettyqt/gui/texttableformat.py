from __future__ import annotations

from prettyqt import constants, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError


class TextTableFormat(gui.textframeformat.TextFrameFormatMixin, QtGui.QTextTableFormat):
    def __bool__(self):
        return self.isValid()

    def set_alignment(self, alignment: constants.AlignmentStr):
        """Set the alignment of the layout.

        Args:
            alignment: alignment for the layout

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setAlignment(constants.ALIGNMENTS[alignment])

    def get_alignment(self) -> constants.AlignmentStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.alignment()]

    def get_column_width_constraints(self) -> list[gui.TextLength]:
        return [gui.TextLength(i) for i in self.columnWidthConstraints()]


if __name__ == "__main__":
    fmt = TextTableFormat()
    print(fmt)
