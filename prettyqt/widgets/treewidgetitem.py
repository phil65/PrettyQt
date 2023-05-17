from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Literal

from prettyqt import constants, gui, iconprovider
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes, get_repr, serializemixin


mod = QtWidgets.QTreeWidgetItem

CHILD_INDICATOR_POLICY = bidict(
    show=mod.ChildIndicatorPolicy.ShowIndicator,
    dont_show=mod.ChildIndicatorPolicy.DontShowIndicator,
    dont_show_when_childless=mod.ChildIndicatorPolicy.DontShowIndicatorWhenChildless,
)

ChildIndicatorPolicyStr = Literal["show", "dont_show", "dont_show_when_childless"]


class TreeWidgetItem(serializemixin.SerializeMixin, QtWidgets.QTreeWidgetItem):
    def __repr__(self):
        return get_repr(self)

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

    def setChecked(self, column: int, checked: bool):
        self.setCheckState(
            column,
            QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked,
        )

    def isChecked(self, col: int) -> bool:
        return self.checkState(col) == QtCore.Qt.CheckState.Checked

    def get_children(self, recursive: bool = False) -> list[QtWidgets.QTreeWidgetItem]:
        """Get children of this item.

        recursive option is written iteratively to also support original QTreeWidgetItems.
        """
        if not recursive:
            return [self.child(i) for i in range(self.childCount())]
        results = []
        nodes = [self]
        while nodes:
            items = []
            for node in nodes:
                results.append(node)
                items.extend(node.child(i) for i in range(node.childCount()))
            nodes = items
        return results[1:]

    def get_top_level_items(self) -> list[QtWidgets.QTreeWidgetItem]:
        return [self.topLevelItem(i) for i in range(self.topLevelItemCount())]

    def collapse(self, recursive: bool = False):
        if recursive:
            for i in range(self.childCount()):
                self.child(i).collapse(True)
        self.setExpanded(False)

    def expand(self, recursive: bool = False):
        self.setExpanded(True)
        if recursive:
            for i in range(self.childCount()):
                self.child(i).expand(True)

    def set_size_hint(self, hint: datatypes.SizeType, column: int = 0):
        if isinstance(hint, tuple):
            hint = QtCore.QSize(*hint)
        self.setSizeHint(column, hint)

    def sort_children(self, column: int, descending: bool = False):
        order = constants.DESCENDING if descending else constants.ASCENDING
        self.sortChildren(column, order)

    def set_data(self, data: Any, role: constants.ItemDataRoleStr | int):
        if isinstance(role, str):
            role = constants.ITEM_DATA_ROLE[role]
        super().setData(data, role)

    def get_data(self, role: constants.ItemDataRoleStr | int) -> Any:
        if isinstance(role, str):
            role = constants.ITEM_DATA_ROLE[role]
        return super().data(role)

    def set_icon(self, icon: datatypes.IconType, column: int = 0):
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
        return None if icon.isNull() else gui.Icon(icon)

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

    def get_text_alignment(self, column: int) -> constants.AlignmentStr:
        return constants.ALIGNMENTS.inverse[self.textAlignment(column)]


if __name__ == "__main__":
    item = TreeWidgetItem()
    print(item.get_text_alignment(0))
