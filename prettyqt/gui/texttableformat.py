from __future__ import annotations

from prettyqt import constants, gui


class TextTableFormat(gui.textframeformat.TextFrameFormatMixin, gui.QTextTableFormat):
    def __bool__(self):
        return self.isValid()

    def set_alignment(self, alignment: constants.AlignmentStr | constants.AlignmentFlag):
        """Set the alignment of the format.

        Args:
            alignment: alignment for the format
        """
        self.setAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

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
