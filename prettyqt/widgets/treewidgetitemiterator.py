from __future__ import annotations

from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


mod = QtWidgets.QTreeWidgetItemIterator

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
                flags = mod.All  # type: ignore
            if hidden is True:
                flags |= mod.Hidden  # type: ignore
            elif hidden is False:
                flags |= mod.NotHidden  # type: ignore
            if selected is True:
                flags |= mod.Selected  # type: ignore
            elif selected is False:
                flags |= mod.Unselected  # type: ignore
            if selectable is True:
                flags |= mod.Selectable  # type: ignore
            elif selectable is False:
                flags |= mod.NotSelectable  # type: ignore
            if draggable is True:
                flags |= mod.DragEnabled  # type: ignore
            elif draggable is False:
                flags |= mod.DragDisabled  # type: ignore
            if droppable is True:
                flags |= mod.DropEnabled  # type: ignore
            elif droppable is False:
                flags |= mod.DropDisabled  # type: ignore
            if has_children is True:
                flags |= mod.HasChildren  # type: ignore
            elif has_children is False:
                flags |= mod.NoChildren  # type: ignore
            if checked is True:
                flags |= mod.Checked  # type: ignore
            elif checked is False:
                flags |= mod.NotChecked  # type: ignore
            if enabled is True:
                flags |= mod.Enabled  # type: ignore
            elif enabled is False:
                flags |= mod.Disabled  # type: ignore
            if editable is True:
                flags |= mod.Editable  # type: ignore
            elif editable is False:
                flags |= mod.NotEditable  # type: ignore
            if user_flag is True:
                flags |= mod.UserFlag  # type: ignore
            super().__init__(other, flags)  # type: ignore


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = QtWidgets.QTreeWidget()
    widget = TreeWidgetItemIterator(item)
