# -*- coding: utf-8 -*-

from qtpy import QtCore, QtWidgets

from prettyqt import gui, core
from prettyqt.utils import bidict, InvalidParamError


STATES = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __repr__(self):
        return "TreeWidgetItem()"

    def serialize_fields(self):
        icon = self.icon(0)
        return dict(
            text=self.text(0),
            tool_tip=self.toolTip(0),
            status_tip=self.statusTip(0),
            checkstate=self.get_checkstate(),
            icon=gui.Icon(icon) if not icon.isNull() else None,
            data=self.data(0, QtCore.Qt.UserRole),
        )

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(0, icon)

    def set_checkstate(self, state: str):
        """Set checkstate of the checkbox.

        valid values are: unchecked, partial, checked

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in STATES:
            raise InvalidParamError(state, STATES)
        self.setCheckState(0, STATES[state])

    def get_checkstate(self) -> str:
        """Return checkstate.

        possible values are "unchecked", "partial", "checked"

        Returns:
            checkstate
        """
        return STATES.inv[self.checkState(0)]


if __name__ == "__main__":
    item = TreeWidgetItem()
    item.setData(0, 1000, "test")
