from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


class LayoutItemMixin:
    def __bool__(self):
        return not self.isEmpty()

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
        return content if (content := self.spacerItem()) else None

    def get_control_types(self) -> list[widgets.sizepolicy.ControlTypeStr]:
        return widgets.sizepolicy.CONTROL_TYPE.get_list(self.controlTypes())


class LayoutItem(LayoutItemMixin, QtWidgets.QLayoutItem):
    pass


if __name__ == "__main__":
    item = LayoutItem("left")
    types = item.get_control_types()
    print(types)
