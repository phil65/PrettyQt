from __future__ import annotations

from prettyqt import constants, widgets


class LayoutItemMixin:
    def __bool__(self):
        return not self.isEmpty()

    def set_alignment(self, alignment: constants.AlignmentStr):
        """Set the alignment of the layout.

        Args:
            alignment: alignment for the layout
        """
        self.setAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    def get_alignment(self) -> constants.AlignmentStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.alignment()]

    def get_item(
        self,
    ) -> widgets.QWidget | widgets.QLayout | widgets.QSpacerItem | None:
        if content := self.widget():
            return content
        if content := self.layout():
            return content
        return content if (content := self.spacerItem()) else None

    def get_control_types(self) -> list[widgets.sizepolicy.ControlTypeStr]:
        return widgets.sizepolicy.CONTROL_TYPE.get_list(self.controlTypes())

    def get_expanding_directions(self) -> list[constants.OrientationStr]:
        return constants.ORIENTATION.get_list(self.expandingDirections())


class LayoutItem(LayoutItemMixin, widgets.QLayoutItem):
    pass


if __name__ == "__main__":
    item = LayoutItem(constants.AlignmentFlag.AlignLeft)
    types = item.get_control_types()
