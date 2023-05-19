from __future__ import annotations

import html
import os
from typing import Any

from prettyqt import constants, gui, iconprovider
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, datatypes


class TableWidgetItem(QtWidgets.QTableWidgetItem):
    def __setitem__(self, index: int | constants.ItemDataRoleStr, value):
        self.set_data(index, value)

    def __getitem__(self, index: int | constants.ItemDataRoleStr):
        return self.get_data(index)

    def serialize_fields(self):
        return dict(
            text=self.text(),
            tool_tip=self.toolTip(),
            status_tip=self.statusTip(),
            checkstate=self.get_checkstate(),
            icon=self.get_icon(),
            data=self.data(constants.USER_ROLE),  # type: ignore
        )

    def set_editable(self, editable: bool):
        """Set whether this item is user-editable."""
        if editable:
            self.setFlags(self.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
        else:
            self.setFlags(self.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(self, state: constants.CheckStateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in constants.CHECK_STATE:
            raise InvalidParamError(state, constants.CHECK_STATE)
        self.setCheckState(constants.CHECK_STATE[state])

    def get_checkstate(self) -> constants.CheckStateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.CHECK_STATE.inverse[self.checkState()]

    def set_text_alignment(
        self,
        horizontal: constants.HorizontalAlignmentStr | None = None,
        vertical: constants.VerticalAlignmentStr | None = None,
    ):
        """Set text alignment of the checkbox.

        Args:
            horizontal: horizontal text alignment to use
            vertical: vertical text alignment to use

        Raises:
            InvalidParamError: invalid text alignment
        """
        match horizontal, vertical:
            case None, None:
                return
            case None, _:
                flag = constants.V_ALIGNMENT[vertical]
            case _, None:
                flag = constants.H_ALIGNMENT[horizontal]
            case _, _:
                flag = constants.V_ALIGNMENT[vertical] | constants.H_ALIGNMENT[horizontal]
        self.setTextAlignment(flag)

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_data(self, role: constants.ItemDataRoleStr | int, data: Any):
        if isinstance(role, str):
            role = constants.ITEM_DATA_ROLE[role]
        super().setData(role, data)

    def get_data(self, role: constants.ItemDataRoleStr | int) -> Any:
        if isinstance(role, str):
            role = constants.ITEM_DATA_ROLE[role]
        return super().data(role)

    def set_tooltip(
        self,
        tooltip: str | datatypes.PathType,
        size: datatypes.SizeType | None = None,
        rich_text: bool = False,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        if rich_text:
            tooltip = f"<html>{html.escape(tooltip)}</html>"
        super().setToolTip(tooltip)


if __name__ == "__main__":
    item = TableWidgetItem()
