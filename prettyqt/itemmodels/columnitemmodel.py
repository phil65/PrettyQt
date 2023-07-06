from __future__ import annotations

from collections.abc import Iterable, Sequence
import enum
import logging

from typing import Any

from prettyqt import constants, core, gui, itemmodels


logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200


class ColumnItem:
    """Determines how an object attribute is shown."""

    model: core.QAbstractItemModel
    name: str = ""
    doc: str = "<no help available>"
    col_visible: bool = True
    width: int | str = SMALL_COL_WIDTH
    line_wrap: gui.textoption.WordWrapModeStr = "none"
    selectable: bool = True
    enabled: bool = True
    editable: bool = False
    checkable: bool = False
    tristate: bool = False

    def __init__(self, model: core.QAbstractItemModel):
        self.model = model

    def get_name(self) -> str:
        return self.name

    def get_flags(self, tree_item):
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

    def get_data(self, item, role):
        return NotImplemented

    def set_data(self, item, value, role):
        return NotImplemented

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

    @staticmethod
    def to_checkstate(value: bool):
        return constants.CheckState.Checked if value else constants.CheckState.Unchecked


class ColumnItemModelMixin:
    class ExtraRoles(enum.IntEnum):
        """Addional roles."""

        TreeItemRole = constants.USER_ROLE + 43435
        ColumnItemRole = constants.USER_ROLE + 43436

    def set_columns(self, columns: Sequence[type[ColumnItem]]):
        self._attr_cols = [Col(model=self) for Col in columns]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None

        col = index.column()
        tree_item = self.data_by_index(index)
        col_item = self._attr_cols[col]
        match role:
            case self.ExtraRoles.TreeItemRole:
                return tree_item
            case self.ExtraRoles.ColumnItemRole:
                return col_item
            case _:
                return col_item.get_data(tree_item, role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        col = index.column()
        tree_item = self.data_by_index(index)
        col_item = self._attr_cols[col]
        col_item.set_data(tree_item, value, role)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        if not index.isValid():
            return super().flags(index)  # TODO: whats best here?
        col = index.column()
        tree_item = self.data_by_index(index)
        return self._attr_cols[col].get_flags(tree_item)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self._attr_cols[section].get_name()
            case _, _:
                return None


class ColumnItemModel(ColumnItemModelMixin, itemmodels.TreeModel):
    def __init__(
        self,
        obj=None,
        columns: Sequence[type[ColumnItem]] = [],
        mime_type: str | None = None,
        show_root: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._root_item = self.TreeItem(obj=obj)
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
        items: Sequence,
        columns: Sequence[ColumnItem],
        mime_type: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.items = items
        self.mime_type = mime_type
        self._attr_cols = []
        self.set_columns(columns)

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.items)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
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

    class TestColumn(ColumnItem):
        name = "test"
        checkable = True

        def get_data(self, item, role):
            match role:
                case constants.CHECKSTATE_ROLE:
                    return getattr(item, "test", False)
                case constants.DISPLAY_ROLE:
                    return str(item.get_root_path())
                case constants.USER_ROLE:
                    return str(item.get_root_path())

        def set_data(self, item, value, role):
            match role:
                case constants.CHECKSTATE_ROLE:
                    item.test = value

    items = core.StorageInfo.get_mounted_volumes()
    model = ColumnTableModel(items, [TestColumn])
    table = widgets.TableView()
    table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.exec()
