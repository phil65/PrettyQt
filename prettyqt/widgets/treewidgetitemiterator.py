from __future__ import annotations

from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


ITERATOR_FLAGS = bidict(
    all=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.All,
    hidden=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Hidden,
    not_hidden=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.NotHidden,
    selected=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Selected,
    unselected=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Unselected,
    selectable=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Selectable,
    not_selectable=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.NotSelectable,
    drag_enabled=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.DragEnabled,
    drag_disabled=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.DragDisabled,
    drop_enabled=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.DropEnabled,
    drop_disabled=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.DropDisabled,
    has_children=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.HasChildren,
    no_children=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.NoChildren,
    checked=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Checked,
    not_checked=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.NotChecked,
    enabled=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Enabled,
    disabled=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Disabled,
    editable=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.Editable,
    not_editable=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.NotEditable,
    user_flag=QtWidgets.QTreeWidgetItemIterator.IteratorFlag.UserFlag,
)


class TreeWidgetItemIterator(QtWidgets.QTreeWidgetItemIterator):
    def __init__(
        self,
        other: (
            QtWidgets.QTreeWidget
            | QtWidgets.QTreeWidgetItem
            | QtWidgets.QTreeWidgetItemIterator
        ),
        flags: QtWidgets.QTreeWidgetItemIterator.IteratorFlags | None = None,
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
                flags = QtWidgets.QTreeWidgetItemIterator.All
            if hidden is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.Hidden
            elif hidden is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.NotHidden
            if selected is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.Selected
            elif selected is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.Unselected
            if selectable is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.Selectable
            elif selectable is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.NotSelectable
            if draggable is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.DragEnabled
            elif draggable is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.DragDisabled
            if droppable is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.DropEnabled
            elif droppable is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.DropDisabled
            if has_children is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.HasChildren
            elif has_children is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.NoChildren
            if checked is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.Checked
            elif checked is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.NotChecked
            if enabled is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.Enabled
            elif enabled is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.Disabled
            if editable is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.Editable
            elif editable is False:
                flags |= QtWidgets.QTreeWidgetItemIterator.NotEditable
            if user_flag is True:
                flags |= QtWidgets.QTreeWidgetItemIterator.UserFlag
            super().__init__(other, flags)  # type: ignore


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = QtWidgets.QTreeWidget()
    widget = TreeWidgetItemIterator(item)
