from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
import logging
from typing import Any

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200


@dataclass(frozen=True)
class ColumnItem:
    """Determines how an object attribute is shown."""

    name: str
    label: Callable[[treeitem.TreeItem], str] | None
    checkstate: Callable[
        [treeitem.TreeItem], constants.StateStr | QtCore.Qt.CheckState | bool
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
    font: Callable | QtGui.QFont | None = None
    selectable: bool = True
    enabled: bool = True
    editable: bool = False
    checkable: bool = False
    tristate: bool = False
    set_edit: Callable | None = None
    set_checkstate: Callable | None = None
    user_data: dict | Callable | None = None

    # def __post_init__(self):
    #     super().__init__()

    def get_name(self) -> str:
        return self.name

    def get_flag(self, tree_item):
        flag = constants.NO_FLAGS
        if self.selectable:
            flag |= constants.IS_SELECTABLE  # type: ignore
        if self.enabled:
            flag |= constants.IS_ENABLED  # type: ignore
        if self.editable:
            flag |= constants.IS_EDITABLE  # type: ignore
        if self.checkable:
            flag |= constants.IS_CHECKABLE  # type: ignore
        if self.tristate:
            flag |= constants.IS_USER_TRISTATE  # type: ignore
        return flag

    def get_label(self, tree_item) -> str:
        if self.label is None:
            return ""
        elif callable(self.label):
            return self.label(tree_item)
        return self.label

    def get_sort_value(self, tree_item) -> str | int:
        if self.sort_value is None:
            return self.get_label()
        elif callable(self.sort_value):
            return self.sort_value(tree_item)
        return self.sort_value

    def get_user_data(self, tree_item, role):
        if self.user_data is None:
            return ""
        elif callable(self.user_data):
            return self.user_data(tree_item, role)
        return self.user_data[role](tree_item)

    def get_tooltip(self, tree_item) -> str:
        if self.tooltip is None:
            return ""
        elif callable(self.tooltip):
            return self.tooltip(tree_item)
        return self.tooltip

    def get_checkstate(self, tree_item) -> bool | QtCore.Qt.CheckState | None:
        if self.checkstate is None:
            return None
        elif callable(self.checkstate):
            result = self.checkstate(tree_item)
            if isinstance(result, str):
                result = constants.STATE[result]
            return result
        return self.checkstate

    def set_checkstate_value(
        self, tree_item, value: bool | QtCore.Qt.CheckState | constants.StateStr | None
    ):
        if self.set_checkstate is None:
            return None
        if isinstance(value, str):
            value = constants.STATE[value]
        if callable(self.set_checkstate):
            self.set_checkstate(tree_item, value)
        else:
            raise ValueError(self.set_checkstate)

    def set_edit_value(self, tree_item, value: str):
        if self.set_edit is None:
            return None
        if callable(self.set_edit):
            self.set_edit(tree_item, value)
        else:
            raise ValueError(self.set_edit)

    def get_font(self, tree_item) -> QtGui.QFont | None:
        if self.font is None:
            return None
        elif callable(self.font):
            return self.font(tree_item)
        return self.font

    def get_foreground_color(self, tree_item) -> QtGui.QColor | None:
        if self.foreground_color is None:
            return None
        elif callable(self.foreground_color):
            return self.foreground_color(tree_item)
        return self.foreground_color

    def get_background_color(self, tree_item) -> QtGui.QColor | None:
        if self.background_color is None:
            return None
        elif callable(self.background_color):
            return self.background_color(tree_item)
        return self.background_color

    def get_decoration(
        self, tree_item
    ) -> QtGui.QColor | QtGui.QPixmap | QtGui.QIcon | None:
        if self.decoration is None:
            return None
        elif callable(self.decoration):
            return self.decoration(tree_item)
        return self.decoration

    def get_alignment(self, tree_item) -> int:
        if self.alignment is None:
            return constants.ALIGN_LEFT  # type: ignore
        elif callable(self.alignment):
            return self.alignment(tree_item)
        elif isinstance(self.alignment, str):
            return constants.ALIGNMENTS[self.alignment]
        return self.alignment

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
    def __init__(
        self,
        attr_cols: list[ColumnItem] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self._attr_cols = attr_cols or []

    def columnCount(self, _parent=None):
        return len(self._attr_cols)

    def data(self, index, role):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None

        col = index.column()
        tree_item = self.tree_item(index)

        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                val = self._attr_cols[col].get_label(tree_item)
                return val.replace("\n", " ")
            case constants.DECORATION_ROLE:
                return self._attr_cols[col].get_decoration(tree_item)
            case constants.CHECKSTATE_ROLE:
                return self._attr_cols[col].get_checkstate(tree_item)
            case constants.ALIGNMENT_ROLE:
                return self._attr_cols[col].get_alignment(tree_item)
            case constants.FOREGROUND_ROLE:
                return self._attr_cols[col].get_foreground_color(tree_item)
            case constants.BACKGROUND_ROLE:
                return self._attr_cols[col].get_background_color(tree_item)
            case constants.FONT_ROLE:
                return self._attr_cols[col].get_font(tree_item)
            case constants.SORT_ROLE:
                return self._attr_cols[col].get_sort_value(tree_item)
            case constants.TOOLTIP_ROLE:
                return self._attr_cols[col].get_tooltip(tree_item)
            case _:
                if int(role) >= int(constants.USER_ROLE):
                    return self._attr_cols[col].get_user_data(tree_item, role)

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        col = index.column()
        tree_item = self.tree_item(index)
        match role:
            case constants.EDIT_ROLE:
                self._attr_cols[col].set_edit_value(tree_item, value)
                self.dataChanged.emit(index, index)
                return True
            case constants.CHECKSTATE_ROLE:
                self._attr_cols[col].set_checkstate_value(tree_item, value)
                self.dataChanged.emit(index, index)
                return True

    def flags(self, index):
        if not index.isValid():
            return constants.NO_CHILDREN
        col = index.column()
        tree_item = self.tree_item(index)
        return self._attr_cols[col].get_flag(tree_item)

    def headerData(self, section, orientation, role):
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self._attr_cols[section].name
            case _, _:
                return None


class ColumnItemModel(ColumnItemModelMixin, core.AbstractItemModel):
    def __init__(self, *args, **kwargs):
        self._root_item = core.ModelIndex()
        super().__init__(*args, **kwargs)

    def root_index(self) -> core.ModelIndex:  # TODO: needed?
        """Return the index that returns the root element (same as an invalid index)."""
        return core.ModelIndex()

    @property
    def root_item(self) -> treeitem.TreeItem:
        """Return the root ObjectBrowserTreeItem."""
        return self._root_item

    def tree_item(self, index: core.ModelIndex) -> treeitem.TreeItem:
        return index.internalPointer() if index.isValid() else self.root_item

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        if parent is None:
            logger.debug("parent is None")
            parent = core.ModelIndex()

        parent_item = self.tree_item(parent)

        if not self.hasIndex(row, column, parent):
            return core.ModelIndex()

        if child_item := parent_item.child(row):
            return self.createIndex(row, column, child_item)
        return core.ModelIndex()

    def parent(self, index: core.ModelIndex) -> QtCore.QModelIndex:  # type:ignore
        if not index.isValid():
            return core.ModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()  # type: ignore

        if parent_item is None or parent_item == self.root_item:
            return core.ModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        return 0 if parent.column() > 0 else self.tree_item(parent).child_count()

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        return 0 if parent.column() > 0 else self.tree_item(parent).has_children

    def canFetchMore(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return 0
        else:
            return not self.tree_item(parent).children_fetched

    def fetchMore(self, parent: core.ModelIndex | None = None):
        """Fetch the children given the model index of a parent node.

        Adds the children to the parent.
        """
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return

        parent_item = self.tree_item(parent)
        if parent_item.children_fetched:
            return

        tree_items = self._fetch_object_children(parent_item)

        with self.insert_rows(0, len(tree_items) - 1, parent):
            for tree_item in tree_items:
                parent_item.append_child(tree_item)
            parent_item.children_fetched = True

    def _fetch_object_children(self, treeitem):
        return []


class ColumnTableModel(ColumnItemModelMixin, core.AbstractTableModel):
    def __init__(
        self,
        items: list,
        columns: list[ColumnItem],
        mime_type: str | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(columns, parent)
        self.items = items
        self.mime_type = mime_type

    def rowCount(self, parent=None):
        return len(self.items)

    def tree_item(self, index: core.ModelIndex):
        return self.items[index.row()]

    def setData(self, index, value, role):
        if role == constants.USER_ROLE:
            self.items[index.row()] = value
            self.update_row(index.row())
            return True
        return super().setData(index, value, role)  # type: ignore

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
            for i in range(len(items)):
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
        checkstate=lambda item: test.get("aa", True),
        set_checkstate=lambda item, value: test.__setitem__("aa", value),
        user_data={constants.USER_ROLE: lambda volume: str(volume.get_root_path())},
    )
    items = core.StorageInfo.get_mounted_volumes()
    model = ColumnTableModel(items, [colitem])
    table = widgets.TableView()
    table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
