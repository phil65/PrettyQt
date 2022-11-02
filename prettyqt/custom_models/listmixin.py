from collections.abc import Iterable
from typing import Any, Callable, Optional

from prettyqt import constants


class ListMixin:
    remove_rows: Callable
    SORT_METHODS: dict[int, Callable]
    change_layout: Callable
    insert_rows: Callable
    removeRow: Callable
    # setData: Callable
    update_row: Callable
    MIME_TYPE: str
    DATA_ROLE = constants.USER_ROLE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore
        self.items = []

    def setData(self, index, value, role):
        if role == self.DATA_ROLE:
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

    def rowCount(self, parent=None):
        """Required override for AbstractitemModels."""
        return len(self.items)

    def data_by_index(self, index):
        return self.items[index.row()]

    def dropMimeData(self, mime_data, action, row, column, parent_index):
        if not mime_data.hasFormat(self.MIME_TYPE):
            return False
        # Since we only drop in between items, parent_index must be invalid,
        # and we use the row arg to know where the drop took place.
        if parent_index.isValid():
            return False
        indexes = mime_data.get_json_data(self.MIME_TYPE)
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
        sorter = self.SORT_METHODS.get(ncol)
        if sorter:
            with self.change_layout():
                self.items.sort(key=sorter, reverse=is_asc)

    def add(self, item: Any, position: Optional[int] = None):
        """Append provided item to the list."""
        self.add_items(items=[item], position=position)
        return item

    def add_items(self, items: Iterable[Any], position: Optional[int] = None):
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
