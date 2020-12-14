from typing import Literal

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError


STATE = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

StateStr = Literal["unchecked", "partial", "checked"]


class StandardItem(QtGui.QStandardItem):
    def __repr__(self):
        return f"StandardItem({self.icon()}, {self.text()!r})"

    def serialize_fields(self):
        return dict(
            text=self.text(),
            tool_tip=self.toolTip(),
            status_tip=self.statusTip(),
            icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
            data=self.data(),
        )

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def clone(self):
        item = self.__class__()
        core.DataStream.copy_data(self, item)
        assert type(item) == StandardItem
        return item

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(self, state: StateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        self.setCheckState(STATE[state])

    def get_checkstate(self) -> StateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return STATE.inverse[self.checkState()]


if __name__ == "__main__":
    item = StandardItem()
    item.setData("test", 1000)
