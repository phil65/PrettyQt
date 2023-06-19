from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
import datetime
import logging
from typing import Any

from prettyqt import constants, core, custom_models, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200


@dataclass  # (frozen=True)
class ColumnItem:
    """Determines how an object attribute is shown."""

    name: str
    label: Callable[[treeitem.TreeItem], str] | None = None
    checkstate: Callable[
        [treeitem.TreeItem], constants.CheckStateStr | QtCore.Qt.CheckState | bool
    ] | None = None
    sort_value: Callable[[treeitem.TreeItem], str | float] | None = None
    tooltip: Callable[[treeitem.TreeItem], str] | None = None
    doc: str = "<no help available>"
    col_visible: bool = True
    width: int | str = SMALL_COL_WIDTH
    alignment: Callable | int | constants.AlignmentStr | None = None
    line_wrap: gui.textoption.WordWrapModeStr = "none"
    foreground_color: Callable | str | None = None
    background_color: Callable | str | None = None
    decoration: Callable | QtGui.QIcon | None = None
    font: Callable | QtGui.QFont | str | None = None
    selectable: bool = True
    enabled: bool = True
    editable: bool = False
    checkable: bool = False
    tristate: bool = False
    set_edit: Callable | None = None
    set_checkstate: Callable | None = None
    user_data: dict | Callable | None = None

    def __post_init__(self):
        super().__init__()
        self.model = None

    def get_name(self) -> str:
        return self.name

    def get_flag(self, tree_item):
        flag = constants.NO_FLAGS
        if self.selectable:
            flag |= constants.IS_SELECTABLE
        if self.enabled:
            flag |= constants.IS_ENABLED
        if self.editable:
            flag |= constants.IS_EDITABLE
        if self.checkable:
            flag |= constants.IS_CHECKABLE
        if self.tristate:
            flag |= constants.IS_USER_TRISTATE
        return flag

    def get_label(self, tree_item) -> str:
        match self.label:
            case None:
                return ""
            case Callable():
                return self.label(tree_item)
            case _:
                return self.label

    def get_sort_value(self, tree_item) -> str | int:
        match self.sort_value:
            case None:
                return self.get_label(tree_item)
            case Callable():
                return self.sort_value(tree_item)
            case _:
                return self.sort_value

    def get_user_data(self, tree_item, role):
        match self.user_data:
            case None:
                return ""
            case Callable():
                return self.user_data(tree_item, role)
            case dict():
                return self.user_data[role](tree_item)
            case _:
                raise ValueError(self.user_data)

    def get_tooltip(self, tree_item) -> str:
        match self.tooltip:
            case None:
                return ""
            case Callable():
                return self.tooltip(tree_item)
            case str():
                return self.tooltip
            case _:
                raise ValueError(self.tooltip)

    def get_checkstate(self, tree_item) -> bool | QtCore.Qt.CheckState | None:
        match self.checkstate:
            case None | bool():
                return self.checkstate
            case Callable():
                result = self.checkstate(tree_item)
                if isinstance(result, str):
                    result = constants.CHECK_STATE[result]
                return result
            case _:
                raise ValueError(self.checkstate)

    def set_checkstate_value(
        self,
        tree_item,
        value: bool | QtCore.Qt.CheckState | constants.CheckStateStr | None,
    ):
        match value:
            case str():
                value = constants.CHECK_STATE[value]
            case int():
                value = QtCore.Qt.CheckState(value)
        match self.set_checkstate:
            case None:
                return None
            case Callable():
                self.set_checkstate(tree_item, value)
            case _:
                raise ValueError(self.set_checkstate)

    def set_edit_value(self, tree_item, value: str):
        match self.set_edit:
            case None:
                return None
            case Callable():
                self.set_edit(tree_item, value)
            case _:
                raise ValueError(self.set_edit)

    def get_font(self, tree_item) -> QtGui.QFont | None:
        match self.font:
            case None | QtGui.QFont():
                return self.font
            case Callable():
                return self.font(tree_item)
            case str():
                return QtGui.QFont(self.font)
            case _:
                raise ValueError(self.font)

    def get_foreground(self, tree_item) -> QtGui.QColor | None:
        match self.foreground_color:
            case None | QtGui.QColor() | QtGui.QBrush():
                return self.foreground_color
            case Callable():
                return self.foreground_color(tree_item)
            case _:
                raise ValueError(self.foreground_color)

    def get_background(self, tree_item) -> QtGui.QColor | None:
        match self.background_color:
            case None | QtGui.QColor() | QtGui.QBrush():
                return self.background_color
            case Callable():
                return self.background_color(tree_item)
            case _:
                raise ValueError(self.foreground_color)

    def get_decoration(
        self, tree_item
    ) -> QtGui.QColor | QtGui.QPixmap | QtGui.QIcon | None:
        match self.decoration:
            case None | QtGui.QIcon() | QtGui.QPixmap() | QtGui.QColor():
                return self.decoration
            case Callable():
                return self.decoration(tree_item)
            case _:
                raise ValueError(self.decoration)

    def get_alignment(self, tree_item) -> QtCore.Qt.AlignmentFlag:
        match self.alignment:
            case None:
                return constants.ALIGN_CENTER_LEFT
            case Callable():
                return self.alignment(tree_item)
            case str():
                return constants.ALIGNMENTS[self.alignment]
            case QtCore.Qt.AlignmentFlag():
                return self.alignment
            case _:
                raise ValueError(self.alignment)

    def get_width(self) -> int:
        match self.width:
            case "small":
                return SMALL_COL_WIDTH
            case "medium":
                return MEDIUM_COL_WIDTH
            case int():
                return self.width
            case _:
                raise ValueError(self.width)


class ColumnItemModelMixin:
    def set_columns(self, columns: Sequence[ColumnItem]):
        self._attr_cols = columns
        for col in columns:
            col.model = self

    def data(self, index, role=constants.DISPLAY_ROLE):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None

        col = index.column()
        tree_item = self.data_by_index(index)
        col_item = self._attr_cols[col]
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                label = col_item.get_label(tree_item)
                if isinstance(label, datetime.datetime):
                    label = str(label)
                return label
            case constants.DECORATION_ROLE:
                return col_item.get_decoration(tree_item)
            case constants.CHECKSTATE_ROLE:
                return col_item.get_checkstate(tree_item)
            case constants.ALIGNMENT_ROLE:
                return col_item.get_alignment(tree_item)
            case constants.FOREGROUND_ROLE:
                return col_item.get_foreground(tree_item)
            case constants.BACKGROUND_ROLE:
                return col_item.get_background(tree_item)
            case constants.FONT_ROLE:
                return col_item.get_font(tree_item)
            case constants.SORT_ROLE:
                return col_item.get_sort_value(tree_item)
            case constants.TOOLTIP_ROLE:
                return col_item.get_tooltip(tree_item)
            case constants.USER_ROLE:
                return tree_item
            case _:
                if int(role) >= int(constants.USER_ROLE):
                    return col_item.get_user_data(tree_item, role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ):
        if not index.isValid():
            return False
        col = index.column()
        tree_item = self.data_by_index(index)
        match role:
            case constants.EDIT_ROLE:
                self._attr_cols[col].set_edit_value(tree_item, value)
                self.dataChanged.emit(index, index)
                return True
            case constants.CHECKSTATE_ROLE:
                self._attr_cols[col].set_checkstate_value(tree_item, value)
                self.dataChanged.emit(index, index)
                return True

    def flags(self, index: core.ModelIndex):
        if not index.isValid():
            return super().flags(index)  # TODO: whats best here?
        col = index.column()
        tree_item = self.data_by_index(index)
        return self._attr_cols[col].get_flag(tree_item)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self._attr_cols[section].name
            case _, _:
                return None


class ColumnItemModel(ColumnItemModelMixin, custom_models.TreeModel):
    def __init__(
        self,
        obj=None,
        columns: Sequence[ColumnItem] = [],
        mime_type: str | None = None,
        show_root: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._root_item = treeitem.TreeItem(obj=obj)
        self._show_root = show_root
        self.mime_type = mime_type
        self._attr_cols = []
        self.set_columns(columns)
        self.set_root_item(obj)

    def columnCount(self, parent=None):
        return len(self._attr_cols)


class ColumnTableModel(ColumnItemModelMixin, core.AbstractTableModel):
    def __init__(
        self,
        items: list,
        columns: Sequence[ColumnItem],
        mime_type: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.items = items
        self.mime_type = mime_type
        self._attr_cols = []
        self.set_columns(columns)

    def rowCount(self, parent=None):
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.items)

    def columnCount(self, parent=None):
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._attr_cols)

    def data_by_index(self, index: core.ModelIndex):
        return self.items[index.row()]

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ):
        if role == constants.USER_ROLE:
            self.items[index.row()] = value
            self.update_row(index.row())
            return True
        return super().setData(index, value, role)

    def removeRows(self, row: int, count: int, parent):
        end_row = row + count - 1
        with self.remove_rows(row, end_row, parent):
            for i in range(end_row, row - 1, -1):
                self.items.pop(i)
        return True

    def dropMimeData(self, mime_data, action, row, column, parent_index):
        if not mime_data.hasFormat(self.mime_type):
            return False
        # Since we only drop in between items, parent_index must be invalid,
        # and we use the row arg to know where the drop took place.
        if parent_index.isValid():
            return False
        indexes = mime_data.get_json_data(self.mime_type)
        pos = row if row < len(self.items) and row != -1 else len(self.items)
        rem_offset = sum(i <= pos for i in indexes)
        new = [self.items[i] for i in indexes]
        with self.change_layout():
            for i in sorted(indexes, reverse=True):
                self.items.pop(i)
            for item in reversed(new):
                self.items.insert(pos - rem_offset, item)
        return False

    def sort(self, ncol: int, order):
        """Sort table by given column number."""
        is_asc = order == constants.ASCENDING
        if sorter := self._attr_cols[ncol].label:
            with self.change_layout():
                self.items.sort(key=sorter, reverse=is_asc)

    def add(self, item: Any, position: int | None = None):
        """Append provided item to the list."""
        self.add_items(items=[item], position=position)
        return item

    def add_items(self, items: Iterable[Any], position: int | None = None):
        """Append a list of items to the list."""
        if position is None:
            position = len(self.items)
        items = list(items)
        with self.insert_rows(position, position + len(items) - 1):
            for i, _ in enumerate(items):
                self.items.insert(i + position, items[i])
            # self.items.extend(items)
        return items

    def remove_items(self, offsets: Iterable[int]):
        for offset in sorted(offsets, reverse=True):
            self.removeRow(offset)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    test = {}
    colitem = ColumnItem(
        name="Test",
        label=lambda volume: str(volume.get_root_path()),
        checkable=True,
        checkstate=lambda item: getattr(item, "test", False),
        set_checkstate=lambda item, value: setattr(item, "test", value),
        user_data={constants.USER_ROLE + 1: lambda volume: str(volume.get_root_path())},
    )
    items = core.StorageInfo.get_mounted_volumes()
    model = ColumnTableModel(items, [colitem])
    table = widgets.TableView()
    table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
