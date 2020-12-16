from __future__ import annotations

from typing import Iterator, Literal

from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError, bidict


CHILD_INDICATOR_POLICY = bidict(
    show=QtWidgets.QTreeWidgetItem.ShowIndicator,
    dont_show=QtWidgets.QTreeWidgetItem.DontShowIndicator,
    dont_show_when_childless=QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless,
)

ChildIndicatorPolicyStr = Literal["show", "dont_show", "dont_show_when_childless"]


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __repr__(self):
        return f"{type(self).__name__}()"

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
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __iter__(self) -> Iterator[QtWidgets.QTreeWidgetItem]:
        return iter(self.child(i) for i in range(self.childCount()))

    def __len__(self):
        return self.childCount()

    def __getitem__(self, index: int) -> QtWidgets.QTreeWidgetItem:
        return self.child(index)

    def __delitem__(self, index: int):
        self.takeChild(index)

    def __add__(self, other: QtWidgets.QTreeWidgetItem) -> TreeWidgetItem:
        self.addChild(other)
        return self

    def sort_children(self, column: int, descending: bool = False):
        order = QtCore.Qt.DescendingOrder if descending else QtCore.Qt.AscendingOrder
        self.sortChildren(column, order)

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

    def set_checkstate(self, state: constants.StateStr, column: int = 0):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use
            column: column

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in constants.STATE:
            raise InvalidParamError(state, constants.STATE)
        self.setCheckState(column, constants.STATE[state])

    def get_checkstate(self, column: int = 0) -> constants.StateStr:
        """Return checkstate.

        Args:
            column: column

        Returns:
            checkstate
        """
        return constants.STATE.inverse[self.checkState(column)]

    def set_child_indicator_policy(self, policy: ChildIndicatorPolicyStr):
        """Set the child indicator policy.

        Args:
            policy: child indicator policy

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in CHILD_INDICATOR_POLICY:
            raise InvalidParamError(policy, CHILD_INDICATOR_POLICY)
        self.setChildIndicatorPolicy(CHILD_INDICATOR_POLICY[policy])

    def get_child_indicator_policy(self) -> ChildIndicatorPolicyStr:
        """Return current child indicator policy.

        Returns:
            child indicator policy
        """
        return CHILD_INDICATOR_POLICY.inverse[self.childIndicatorPolicy()]


if __name__ == "__main__":
    item = TreeWidgetItem()
    item[0]
    item.setData(0, 1000, "test")
