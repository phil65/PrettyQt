from collections.abc import Callable, Iterable
from typing import Any

from prettyqt import constants, core


class ListMixin:
    SORT_METHODS: dict[int, Callable]
    MIME_TYPE: str = ""

    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore
        self.items = items or []

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if role == constants.USER_ROLE:
            self.items[index.row()] = value
            self.update_row(index.row())
            return True
        return super().setData(index, value, role)  # type: ignore

    def removeRows(self, row: int, count: int, parent):
        # called by default implementation of QAbstractItemModel::startDrag
        end_row = row + count - 1
        with self.remove_rows(row, end_row, parent):
            for i in range(end_row, row - 1, -1):
                self.items.pop(i)
        return True

    # def insertRows(self, row: int, count: int, parent):
    #     # called by default implementation of QAbstractItemModel::dropMimeData
    #     end_row = row + count - 1
    #     with self.insert_rows(row, end_row, parent):
    #         for i in range(end_row, row - 1, -1):
    #             self.items.insert(i,)
    #     return True

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Required override for AbstractitemModels."""
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 or parent.isValid() else len(self.items)

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
        if sorter := self.SORT_METHODS.get(ncol):
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

    def supportedDropActions(self):
        return constants.MOVE_ACTION

    def mimeTypes(self):
        return [self.MIME_TYPE]

    def mimeData(self, indexes):
        """AbstractItemModel override, defines the data used for drag and drop.

        atm this just returns the positions (not sure if this is perfect)
        """
        mime_data = core.MimeData()
        data = [i.row() for i in indexes if i.column() == 0]
        mime_data.set_json_data(self.MIME_TYPE, data)
        return mime_data

    # list interface

    def pop(self, row=None):
        if row is None:
            row = len(self.items) - 1
        result = self.items[row]
        self.removeRow(row)
        return result

    def __getitem__(self, row):
        return self.items[row]

    def __setitem__(self, row: int | slice, value):
        match row:
            case slice():
                rng = range(row.start or 0, row.stop or len(self.items), row.step or 1)
                for count, i in enumerate(rng):
                    if i < self.rowCount():
                        index = self.index(i)
                        self.setData(i, value[count], role=constants.USER_ROLE)
                    else:
                        self.items.append(value[count])
            case int():
                index = self.index(row)
                self.setData(index, value, role=constants.USER_ROLE)
            case _:
                raise ValueError(row)

    def __len__(self):
        return len(self.items)

    def insert(self, row: int, value):
        with self.insert_row(row):
            self.items.insert(row, value)

    def append(self, value):
        row = len(self.items)
        self.insert(row, value)

    def extend(self, values):
        pos = len(self.items)
        with self.insert_rows(pos, pos + len(values)):
            self.items.extend(values)

    def set_list(self, values):
        """Set the model to a new list."""
        with self.reset_model():
            self.items = values

    def remove(self, item):
        if item in self.items:
            pos = self.items.index(item)
            with self.remove_row(pos):
                self.items.remove(item)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    class Test(ListMixin, core.AbstractTableModel):
        def data(self, index, role):
            if role == constants.DISPLAY_ROLE:
                return self.items[index.row()]

        def columnCount(self, index: core.ModelIndex | None = None):
            return 1

    model = Test()
    model.set_list(["a", "b"])
    app = widgets.app()
    view = widgets.TableView()
    stalker = debugging.Stalker(model)
    view.set_model(model)
    view.show()
    app.sleep(2)
    model.pop(0)
    with app.debug_mode():
        app.exec()
