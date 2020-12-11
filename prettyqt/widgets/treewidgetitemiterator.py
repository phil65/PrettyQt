from typing import Optional, Union

from qtpy import QtWidgets

from prettyqt.utils import bidict


ITERATOR_FLAGS = bidict(
    all=QtWidgets.QTreeWidgetItemIterator.All,
    hidden=QtWidgets.QTreeWidgetItemIterator.Hidden,
    not_hidden=QtWidgets.QTreeWidgetItemIterator.NotHidden,
    selected=QtWidgets.QTreeWidgetItemIterator.Selected,
    unselected=QtWidgets.QTreeWidgetItemIterator.Unselected,
    selectable=QtWidgets.QTreeWidgetItemIterator.Selectable,
    not_selectable=QtWidgets.QTreeWidgetItemIterator.NotSelectable,
    drag_enabled=QtWidgets.QTreeWidgetItemIterator.DragEnabled,
    drag_disabled=QtWidgets.QTreeWidgetItemIterator.DragDisabled,
    drop_enabled=QtWidgets.QTreeWidgetItemIterator.DropEnabled,
    drop_disabled=QtWidgets.QTreeWidgetItemIterator.DropDisabled,
    has_children=QtWidgets.QTreeWidgetItemIterator.HasChildren,
    no_children=QtWidgets.QTreeWidgetItemIterator.NoChildren,
    checked=QtWidgets.QTreeWidgetItemIterator.Checked,
    not_checked=QtWidgets.QTreeWidgetItemIterator.NotChecked,
    enabled=QtWidgets.QTreeWidgetItemIterator.Enabled,
    disabled=QtWidgets.QTreeWidgetItemIterator.Disabled,
    editable=QtWidgets.QTreeWidgetItemIterator.Editable,
    not_editable=QtWidgets.QTreeWidgetItemIterator.NotEditable,
    user_flag=QtWidgets.QTreeWidgetItemIterator.UserFlag,
)


class TreeWidgetItemIterator(QtWidgets.QTreeWidgetItemIterator):
    def __init__(
        self,
        other: Union[
            QtWidgets.QTreeWidget,
            QtWidgets.QTreeWidgetItem,
            QtWidgets.QTreeWidgetItemIterator,
        ],
        flags: Optional[int] = None,
        hidden: Optional[bool] = None,
        selected: Optional[bool] = None,
        selectable: Optional[bool] = None,
        draggable: Optional[bool] = None,
        droppable: Optional[bool] = None,
        has_children: Optional[bool] = None,
        checked: Optional[bool] = None,
        enabled: Optional[bool] = None,
        editable: Optional[bool] = None,
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
            super().__init__(other, flags)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = QtWidgets.QTreeWidget()
    widget = TreeWidgetItemIterator(item)
