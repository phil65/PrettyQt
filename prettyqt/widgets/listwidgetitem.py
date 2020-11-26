# -*- coding: utf-8 -*-

from qtpy import QtCore, QtWidgets

from prettyqt import gui, core
from prettyqt.utils import bidict, InvalidParamError


STATES = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)


class ListWidgetItem(QtWidgets.QListWidgetItem):
    def __repr__(self):
        return f"ListWidgetItem({self.icon()}, {self.text()!r})"

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

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

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
        self.setCheckState(STATES[state])

    def get_checkstate(self) -> str:
        """Return checkstate.

        possible values are "unchecked", "partial", "checked"

        Returns:
            checkstate
        """
        return STATES.inv[self.checkState()]

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon:
        return gui.Icon(self.icon())


if __name__ == "__main__":
    item = ListWidgetItem()
    item.setData(1000, "test")
