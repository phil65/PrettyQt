from __future__ import annotations

from typing import Any

from prettyqt import constants, gui, iconprovider
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes, get_repr, serializemixin


class ListWidgetItem(serializemixin.SerializeMixin, QtWidgets.QListWidgetItem):
    """Item for use with the QListWidget item view class."""

    def __repr__(self):
        return get_repr(self, self.icon(), self.text())

    def __setitem__(self, index: int | constants.ItemDataRoleStr, value):
        self.set_data(index, value)

    def __getitem__(self, index: int | constants.ItemDataRoleStr):
        return self.get_data(index)

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(self, state: constants.CheckStateStr | constants.CheckState):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use
        """
        self.setCheckState(constants.CHECK_STATE.get_enum_value(state))

    def get_checkstate(self) -> constants.CheckStateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.CHECK_STATE.inverse[self.checkState()]

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon | None:
        return None if (icon := super().icon()).isNull() else gui.Icon(icon)

    def set_data(self, role: constants.ItemDataRoleStr | int, data: Any):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        super().setData(role, data)

    def get_data(self, role: constants.ItemDataRoleStr | int):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        return super().data(role)

    def set_size_hint(self, hint: datatypes.SizeType):
        super().setSizeHint(datatypes.to_size(hint))

    def set_text_alignment(
        self,
        horizontal: constants.HorizontalAlignmentStr
        | constants.AlignmentFlag
        | None = None,
        vertical: constants.VerticalAlignmentStr | constants.AlignmentFlag | None = None,
    ):
        """Set text alignment of the checkbox.

        Args:
            horizontal: horizontal text alignment to use
            vertical: vertical text alignment to use

        """
        match horizontal, vertical:
            case None, None:
                return
            case None, _:
                flag = constants.V_ALIGNMENT.get_enum_value(vertical)
            case _, None:
                flag = constants.H_ALIGNMENT.get_enum_value(horizontal)
            case _, _:
                flag = constants.V_ALIGNMENT.get_enum_value(
                    vertical
                ) | constants.H_ALIGNMENT.get_enum_value(horizontal)
        self.setTextAlignment(flag)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.ListWidget()
    item = ListWidgetItem("AB")
    item.set_data("display", "test")
    widget.add(item)
    widget.show()
    app.exec()
