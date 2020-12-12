from __future__ import annotations

from typing import Iterator

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
        return STATES.inverse[self.checkState(column)]

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
        return CHILD_INDICATOR_POLICY.inverse[self.childIndicatorPolicy()]


if __name__ == "__main__":
    item = TreeWidgetItem()
    item[0]
    item.setData(0, 1000, "test")
