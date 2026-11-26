from typing import TYPE_CHECKING, Any, ClassVar

from prettyqt import constants, core


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence


def _sort_key(value: Any) -> tuple:
    """Sort key which never raises for mixed / missing values.

    None values go last, numbers before everything else.
    """
    match value:
        case None:
            return (2, 0, "")
        case bool() | int() | float():
            return (0, value, "")
        case _:
            return (1, 0, str(value))


if TYPE_CHECKING:
    from prettyqt import core as _core

    # prettyqt item models: AbstractItemModel helpers plus data_by_index()
    class _ListBase(_core.AbstractItemModel):
        def data_by_index(self, index: _core.ModelIndex) -> Any: ...

else:
    _ListBase = object


class ListMixin(_ListBase):
    """Mixin for flat models which are backed by a python list (`self.items`).

    Provides the list interface (`append`, `pop`, `__getitem__` etc.) with correct
    model signals, internal drag & drop and sorting.
    """

    SORT_METHODS: ClassVar[dict[int, Callable[[Any], Any]]] = {}
    """Optional sort key callables per column, called with the list item."""
    MIME_TYPE: str = ""

    def __init__(self, items: Sequence | None = None, **kwargs):
        super().__init__(**kwargs)  # type: ignore
        self.items = items if isinstance(items, list) else list(items or [])

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if role == constants.USER_ROLE and index.isValid():
            self.items[index.row()] = value
            self.update_row(index.row())
            return True
        return super().setData(index, value, role)  # type: ignore

    def removeRows(
        self, row: int, count: int, parent: core.ModelIndex | None = None
    ) -> bool:
        # called by default implementation of QAbstractItemModel::startDrag
        parent = parent or core.ModelIndex()
        if parent.isValid() or count <= 0 or row < 0 or row + count > len(self.items):
            return False
        end_row = row + count - 1
        with self.remove_rows(row, end_row, parent):
            del self.items[row : end_row + 1]
        return True

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Required override for AbstractitemModels."""
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 or parent.isValid() else len(self.items)

    def data_by_index(self, index: core.ModelIndex):
        return self.items[index.row()]

    def dropMimeData(self, mime_data, action, row, column, parent_index) -> bool:
        if not self.MIME_TYPE or not mime_data.hasFormat(self.MIME_TYPE):
            return False
        # Since we only drop in between items, parent_index must be invalid,
        # and we use the row arg to know where the drop took place.
        if parent_index.isValid():
            return False
        indexes = sorted(set(mime_data.get_json_data(self.MIME_TYPE)))
        pos = row if 0 <= row < len(self.items) else len(self.items)
        moved = [self.items[i] for i in indexes]
        remaining = [item for i, item in enumerate(self.items) if i not in indexes]
        insert_at = pos - sum(i < pos for i in indexes)
        new_order = remaining[:insert_at] + moved + remaining[insert_at:]
        # map old rows to new rows to keep persistent indexes valid.
        old_rows = [i for i in range(len(self.items)) if i not in indexes]
        old_rows = old_rows[:insert_at] + indexes + old_rows[insert_at:]
        self._reorder(new_order, old_rows)
        # we moved the items ourselves, so return False to prevent the view
        # from removing the source rows afterwards.
        return False

    def _reorder(self, new_items: list, old_rows: list[int]):
        """Set new item order and update persistent indexes accordingly.

        Arguments:
            new_items: the items in their new order
            old_rows: for each new row, the row the item had before
        """
        # no arguments: PySide6 does not accept parents / hint for the emit call.
        self.layoutAboutToBeChanged.emit()  # type: ignore
        new_row_for_old = {old: new for new, old in enumerate(old_rows)}
        old_persistent = self.persistentIndexList()  # type: ignore
        new_persistent = [
            self.index(new_row_for_old[idx.row()], idx.column())  # type: ignore
            for idx in old_persistent
        ]
        self.items = new_items
        self.changePersistentIndexList(old_persistent, new_persistent)  # type: ignore
        self.layoutChanged.emit()  # type: ignore

    def _get_sort_value(self, row: int, column: int) -> Any:
        if sorter := self.SORT_METHODS.get(column):
            return sorter(self.items[row])
        index = self.index(row, column)  # type: ignore
        value = self.data(index, constants.SORT_ROLE)  # type: ignore
        if value is None:
            value = self.data(index, constants.DISPLAY_ROLE)  # type: ignore
        return value

    def sort(self, column: int, order=constants.ASCENDING):
        """Sort list by given column number."""
        if column < 0 or not self.items:
            return
        rows = sorted(
            range(len(self.items)),
            key=lambda row: _sort_key(self._get_sort_value(row, column)),
            reverse=order == constants.DESCENDING,
        )
        self._reorder([self.items[i] for i in rows], rows)

    def add(self, item: Any, position: int | None = None):
        """Append provided item to the list."""
        self.add_items(items=[item], position=position)
        return item

    def add_items(self, items: Iterable[Any], position: int | None = None):
        """Insert a list of items at given position (default: append)."""
        if position is None:
            position = len(self.items)
        items = list(items)
        if not items:
            return items
        with self.insert_rows(position, position + len(items) - 1):
            self.items[position:position] = items
        return items

    def remove_items(self, offsets: Iterable[int]):
        for offset in sorted(set(offsets), reverse=True):
            self.removeRow(offset)

    def supportedDropActions(self):
        return constants.MOVE_ACTION

    def mimeTypes(self):
        return [self.MIME_TYPE] if self.MIME_TYPE else []

    def mimeData(self, indexes):
        """AbstractItemModel override, defines the data used for drag and drop.

        Contains the rows of the dragged items.
        """
        mime_data = core.MimeData()
        data = sorted({i.row() for i in indexes})
        mime_data.set_json_data(self.MIME_TYPE, data)
        return mime_data

    # list interface

    def pop(self, row: int = -1):
        if row < 0:
            row += len(self.items)
        result = self.items[row]
        self.removeRow(row)
        return result

    def __getitem__(self, row):
        return self.items[row]

    def __setitem__(self, row: int | slice, value):
        match row:
            case slice():
                indices = range(*row.indices(len(self.items)))
                values = list(value)
                if len(indices) != len(values):
                    # size changing slice assignment, just reset.
                    new = list(self.items)
                    new[row] = values
                    self.set_list(new)
                    return
                for i, val in zip(indices, values, strict=True):
                    self.setData(self.index(i, 0), val, role=constants.USER_ROLE)  # type: ignore
            case int():
                if row < 0:
                    row += len(self.items)
                self.setData(self.index(row, 0), value, role=constants.USER_ROLE)  # type: ignore
            case _:
                raise TypeError(row)

    def __len__(self):
        return len(self.items)

    def insert(self, row: int, value):
        row = min(max(row, 0), len(self.items))
        with self.insert_row(row):
            self.items.insert(row, value)

    def append(self, value):
        self.insert(len(self.items), value)

    def extend(self, values: Iterable):
        self.add_items(values)

    def set_list(self, values: Sequence):
        """Set the model to a new list."""
        with self.reset_model():
            self.items = values if isinstance(values, list) else list(values)

    def remove(self, item):
        if item in self.items:
            self.removeRow(self.items.index(item))


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    class Test(ListMixin, core.AbstractTableModel):
        def data(self, index, role):
            if role == constants.DISPLAY_ROLE:
                return self.items[index.row()]
            return None

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
