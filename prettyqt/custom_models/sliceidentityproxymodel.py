from __future__ import annotations

import logging

from prettyqt import core
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class SliceIdentityProxyModel(core.IdentityProxyModel):
    def __init__(self, indexer=None, **kwargs):
        super().__init__(**kwargs)
        self._indexer = None
        self.set_indexer(indexer)

    def indexer_contains(self, index: core.ModelIndex) -> bool:
        return helpers.is_position_in_index(index.column(), index.row(), self._indexer)

    def set_indexer(self, indexer):
        match indexer:
            case None:
                self._indexer = (slice(None), slice(None))
            case int() as column:
                self._indexer = (slice(column, column + 1), slice(None))
            case slice() as colslice:
                self._indexer = (colslice, slice(None))
            case col_slice, row_slice:
                self.set_column_slice(col_slice)
                self.set_row_slice(row_slice)
            case _:
                raise TypeError(indexer)

    def get_column_slice(self) -> slice:
        match self._indexer:
            case None | (None, _):
                return slice(None)
            case (slice() as colslice, _):
                return colslice
            case _:
                raise TypeError(self._indexer)

    def get_row_slice(self) -> slice:
        match self._indexer:
            case None | (_, None):
                return slice(None)
            case (_, slice() as rowslice):
                return rowslice
            case _:
                raise TypeError(self._indexer)

    def set_column_slice(self, value: slice | int | None) -> slice:
        match value:
            case slice() as colslice:
                self._indexer = (colslice, self.get_row_slice())
            case int() as col:
                self._indexer = (slice(col, col + 1), self.get_row_slice())
            case None:
                self._indexer = (slice(None), self.get_row_slice())
            case _:
                raise TypeError(value)

    def set_row_slice(self, value: slice | int | None) -> slice:
        match value:
            case slice() as rowslice:
                self._indexer = (self.get_column_slice(), rowslice)
            case int() as row:
                self._indexer = (self.get_column_slice(), slice(row, row + 1))
            case None:
                self._indexer = (self.get_column_slice(), slice(None))
            case _:
                raise TypeError(value)

    def get_row_range(self) -> range:
        sl = self.get_row_slice()
        row_count = self.sourceModel().rowCount()
        return range(sl.start or 0, sl.stop or row_count, sl.step or 1)

    def get_column_range(self) -> range:
        sl = self.get_column_slice()
        col_count = self.sourceModel().columnCount()
        return range(sl.start or 0, sl.stop or col_count, sl.step or 1)

    def position_in_column_slice(self, col: int) -> int:
        sl = self.get_column_slice()
        return (col - (sl.start or 0)) / (sl.step or 1)

    def position_in_row_slice(self, row: int) -> int:
        sl = self.get_row_slice()
        return (row - (sl.start or 0)) / (sl.step or 1)

    column_slice = core.Property(slice, get_column_slice, set_column_slice)
    row_slice = core.Property(slice, get_column_slice, set_column_slice)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    table = widgets.TableView()
    table.set_model(["a", "b", "c"])
    table.proxifier.get_proxy("read_only", index=(0, 0))
    table.show()
    with app.debug_mode():
        app.main_loop()
