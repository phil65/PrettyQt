from __future__ import annotations

from prettyqt import constants
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


class LayoutItem(QtWidgets.QLayoutItem):
    # def __bool__(self):
    #     return not self.isEmpty()

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

    def get_item(
        self,
    ) -> QtWidgets.QWidget | QtWidgets.QLayout | QtWidgets.QSpacerItem | None:
        if content := self.widget():
            return content
        if content := self.layout():
            return content
        if content := self.spacerItem():
            return content
        return None
