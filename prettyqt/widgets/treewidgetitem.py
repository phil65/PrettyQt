from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


mod = QtWidgets.QTreeWidgetItem

CHILD_INDICATOR_POLICY = bidict(
    show=mod.ChildIndicatorPolicy.ShowIndicator,
    dont_show=mod.ChildIndicatorPolicy.DontShowIndicator,
    dont_show_when_childless=mod.ChildIndicatorPolicy.DontShowIndicatorWhenChildless,
)

ChildIndicatorPolicyStr = Literal["show", "dont_show", "dont_show_when_childless"]


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def serialize_fields(self):
        data = [
            self.data(i, constants.USER_ROLE)  # type: ignore
            for i in range(self.columnCount())
        ]
        return dict(
            text=[self.text(i) for i in range(self.columnCount())],
            tool_tip=[self.toolTip(i) for i in range(self.columnCount())],
            status_tip=[self.statusTip(i) for i in range(self.columnCount())],
            checkstate=[self.get_checkstate(i) for i in range(self.columnCount())],
            icon=[self.get_icon(i) for i in range(self.columnCount())],
            data=data,
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
        item = self.child(index)
        if item is None:
            raise KeyError(index)
        return item

    def __delitem__(self, index: int):
        self.takeChild(index)

    def __add__(self, other: QtWidgets.QTreeWidgetItem) -> TreeWidgetItem:
        self.addChild(other)
        return self

    def set_size_hint(self, hint: types.SizeType, column: int = 0):
        if isinstance(hint, tuple):
            hint = QtCore.QSize(*hint)
        self.setSizeHint(column, hint)

    def sort_children(self, column: int, descending: bool = False):
        order = constants.DESCENDING if descending else constants.ASCENDING
        self.sortChildren(column, order)

    def set_icon(self, icon: types.IconType, column: int = 0):
        """Set the icon for the action.

        Args:
            icon: icon to use
            column: column
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(column, icon)

    def get_background(self, column: int = 0) -> gui.Brush:
        return gui.Brush(self.background(column))

    def get_foreground(self, column: int = 0) -> gui.Brush:
        return gui.Brush(self.foreground(column))

    def get_font(self, column: int = 0) -> gui.Font:
        return gui.Font(self.font(column))

    def get_icon(self, column: int = 0) -> gui.Icon | None:
        icon = self.icon(column)
        if icon.isNull():
            return None
        return gui.Icon(icon)

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
