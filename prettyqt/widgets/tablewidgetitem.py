from __future__ import annotations

import os

from prettyqt import constants, gui, iconprovider
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, types


class TableWidgetItem(QtWidgets.QTableWidgetItem):
    def __setitem__(self, index: int, value):
        self.setData(index, value)

    def __getitem__(self, index: int):
        return self.data(index)

    def serialize_fields(self):
        return dict(
            text=self.text(),
            tool_tip=self.toolTip(),
            status_tip=self.statusTip(),
            checkstate=self.get_checkstate(),
            icon=self.get_icon(),
            data=self.data(constants.USER_ROLE),  # type: ignore
        )

    def set_icon(self, icon: types.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(self, state: constants.StateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in constants.STATE:
            raise InvalidParamError(state, constants.STATE)
        self.setCheckState(constants.STATE[state])

    def get_checkstate(self) -> constants.StateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.STATE.inverse[self.checkState()]

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
        if horizontal is None and vertical is not None:
            flag = constants.V_ALIGNMENT[vertical]
        elif vertical is None and horizontal is not None:
            flag = constants.H_ALIGNMENT[horizontal]
        elif vertical is not None and horizontal is not None:
            flag = constants.V_ALIGNMENT[vertical] | constants.H_ALIGNMENT[horizontal]
        else:
            return
        self.setTextAlignment(flag)

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        if icon.isNull():
            return None
        return gui.Icon(icon)

    def set_tooltip(
        self,
        tooltip: str | types.PathType,
        size: types.SizeType | None = None,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        self.setToolTip(tooltip)


if __name__ == "__main__":
    item = TableWidgetItem()
