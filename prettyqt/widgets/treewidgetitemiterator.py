from typing import Literal

from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


mod = QtWidgets.QTreeWidgetItemIterator

IteratorFlagStr = Literal[
    "all",
    "hidden",
    "not_hidden",
    "selected",
    "unselected",
    "selectable",
    "not_selectable",
    "drag_enabled",
    "drag_disabled",
    "drop_enabled",
    "drop_disabled",
    "has_children",
    "no_children",
    "checked",
    "not_checked",
    "enabled",
    "disabled",
    "editable",
    "not_editable",
    "user_flag",
]

ITERATOR_FLAGS = bidict(
    all=mod.IteratorFlag.All,
    hidden=mod.IteratorFlag.Hidden,
    not_hidden=mod.IteratorFlag.NotHidden,
    selected=mod.IteratorFlag.Selected,
    unselected=mod.IteratorFlag.Unselected,
    selectable=mod.IteratorFlag.Selectable,
    not_selectable=mod.IteratorFlag.NotSelectable,
    drag_enabled=mod.IteratorFlag.DragEnabled,
    drag_disabled=mod.IteratorFlag.DragDisabled,
    drop_enabled=mod.IteratorFlag.DropEnabled,
    drop_disabled=mod.IteratorFlag.DropDisabled,
    has_children=mod.IteratorFlag.HasChildren,
    no_children=mod.IteratorFlag.NoChildren,
    checked=mod.IteratorFlag.Checked,
    not_checked=mod.IteratorFlag.NotChecked,
    enabled=mod.IteratorFlag.Enabled,
    disabled=mod.IteratorFlag.Disabled,
    editable=mod.IteratorFlag.Editable,
    not_editable=mod.IteratorFlag.NotEditable,
    user_flag=mod.IteratorFlag.UserFlag,
)


class TreeWidgetItemIterator(QtWidgets.QTreeWidgetItemIterator):
    def __init__(
        self,
        other: (
            QtWidgets.QTreeWidget
            | QtWidgets.QTreeWidgetItem
            | QtWidgets.QTreeWidgetItemIterator
        ),
        flags: QtWidgets.QTreeWidgetItemIterator.IteratorFlag | None = None,
        hidden: bool | None = None,
        selected: bool | None = None,
        selectable: bool | None = None,
        draggable: bool | None = None,
        droppable: bool | None = None,
        has_children: bool | None = None,
        checked: bool | None = None,
        enabled: bool | None = None,
        editable: bool | None = None,
        user_flag: bool = False,
    ):
        if isinstance(other, QtWidgets.QTreeWidgetItemIterator):
            super().__init__(other)
        else:
            if flags is None:
                flags = mod.IteratorFlag.All
            if hidden is True:
                flags |= mod.IteratorFlag.Hidden
            elif hidden is False:
                flags |= mod.IteratorFlag.NotHidden
            if selected is True:
                flags |= mod.IteratorFlag.Selected
            elif selected is False:
                flags |= mod.IteratorFlag.Unselected
            if selectable is True:
                flags |= mod.IteratorFlag.Selectable
            elif selectable is False:
                flags |= mod.IteratorFlag.NotSelectable
            if draggable is True:
                flags |= mod.IteratorFlag.DragEnabled
            elif draggable is False:
                flags |= mod.IteratorFlag.DragDisabled
            if droppable is True:
                flags |= mod.IteratorFlag.DropEnabled
            elif droppable is False:
                flags |= mod.IteratorFlag.DropDisabled
            if has_children is True:
                flags |= mod.IteratorFlag.HasChildren
            elif has_children is False:
                flags |= mod.IteratorFlag.NoChildren
            if checked is True:
                flags |= mod.IteratorFlag.Checked
            elif checked is False:
                flags |= mod.IteratorFlag.NotChecked
            if enabled is True:
                flags |= mod.IteratorFlag.Enabled
            elif enabled is False:
                flags |= mod.IteratorFlag.Disabled
            if editable is True:
                flags |= mod.IteratorFlag.Editable
            elif editable is False:
                flags |= mod.IteratorFlag.NotEditable
            if user_flag:
                flags |= mod.IteratorFlag.UserFlag
            super().__init__(other, flags)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = QtWidgets.QTreeWidget()
    widget = TreeWidgetItemIterator(item)
