# -*- coding: utf-8 -*-

from qtpy import QtCore, QtWidgets

from prettyqt import gui, core
from prettyqt.utils import bidict, InvalidParamError


STATES = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

CHILD_INDICATOR_POLICY = bidict(
    show=QtWidgets.QTreeWidgetItem.ShowIndicator,
    dont_show=QtWidgets.QTreeWidgetItem.DontShowIndicator,
    dont_show_when_childless=QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless,
)


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __repr__(self):
        return "TreeWidgetItem()"

    def serialize_fields(self):
        icon = self.icon(0)
        return dict(
            text=[self.text(i) for i in range(self.columnCount())],
            tool_tip=[self.toolTip(i) for i in range(self.columnCount())],
            status_tip=[self.statusTip(i) for i in range(self.columnCount())],
            checkstate=[self.get_checkstate(i) for i in range(self.columnCount())],
            icon=gui.Icon(icon) if not icon.isNull() else None,
            data=[self.data(i, QtCore.Qt.UserRole) for i in range(self.columnCount())],
        )

    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        self.__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def set_icon(self, icon: gui.icon.IconType, column: int = 0):
        """Set the icon for the action.

        Args:
            icon: icon to use
            column: column
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(column, icon)

    def get_background(self, column: int = 0) -> gui.Brush:
        return gui.Brush(self.background(column))

    def get_foreground(self, column: int = 0) -> gui.Brush:
        return gui.Brush(self.foreground(column))

    def get_font(self, column: int = 0) -> gui.Font:
        return gui.Font(self.font(column))

    def get_icon(self, column: int = 0) -> gui.Icon:
        return gui.Icon(self.icon(column))

    def set_checkstate(self, state: str, column: int = 0):
        """Set checkstate of the checkbox.

        valid values are: unchecked, partial, checked

        Args:
            state: checkstate to use
            column: column

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in STATES:
            raise InvalidParamError(state, STATES)
        self.setCheckState(column, STATES[state])

    def get_checkstate(self, column: int = 0) -> str:
        """Return checkstate.

        possible values are "unchecked", "partial", "checked"

        Args:
            column: column

        Returns:
            checkstate
        """
        return STATES.inv[self.checkState(column)]

    def set_child_indicator_policy(self, policy: str):
        """Set the child indicator policy.

        Allowed values are "show", "dont_show", "dont_show_when_childless"

        Args:
            policy: child indicator policy

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in CHILD_INDICATOR_POLICY:
            raise InvalidParamError(policy, CHILD_INDICATOR_POLICY)
        self.setChildIndicatorPolicy(CHILD_INDICATOR_POLICY[policy])

    def get_child_indicator_policy(self) -> str:
        """Return current child indicator policy.

        Possible values: "show", "dont_show", "dont_show_when_childless"

        Returns:
            child indicator policy
        """
        return CHILD_INDICATOR_POLICY.inv[self.childIndicatorPolicy()]


if __name__ == "__main__":
    item = TreeWidgetItem()
    item.setData(0, 1000, "test")
