from typing import Optional

from qtpy import QtCore, QtWidgets

from prettyqt import constants, gui
from prettyqt.utils import InvalidParamError


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
            icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
            data=self.data(QtCore.Qt.UserRole),
        )

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
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
        horizontal: Optional[constants.HorizontalAlignmentStr] = None,
        vertical: Optional[constants.VerticalAlignmentStr] = None,
    ):
        """Set text alignment of the checkbox.

        Args:
            alignment: text alignment to use

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

    def get_icon(self) -> gui.Icon:
        return gui.Icon(self.icon())


if __name__ == "__main__":
    item = TableWidgetItem()
