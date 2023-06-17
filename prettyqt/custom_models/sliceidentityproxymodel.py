from __future__ import annotations

import logging

from prettyqt import core
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class SliceIdentityProxyModel(core.IdentityProxyModel):
    def __init__(self, indexer=None, **kwargs):
        super().__init__(**kwargs)
        self._indexer = (slice(None), slice(None))
        self.set_indexer(indexer)

    def indexer_contains(self, index: core.ModelIndex) -> bool:
        """Check whether given ModelIndex is included in our Indexer."""
        col_slice = self.update_slice_boundaries(self.get_column_slice(), typ="column")
        row_slice = self.update_slice_boundaries(self.get_row_slice(), typ="row")
        # logger.info(f"{col_slice=} {row_slice=}")
        to_check = (col_slice, row_slice)  # instead of _indexer, for negative indexes.
        return helpers.is_position_in_index(index.column(), index.row(), to_check)

    def update_slice_boundaries(self, sl: slice, typ="row") -> slice:
        """Update slice boundaries by resolving negative indexes."""
        # I dont know yet whats the best approach here and which cases I should support.
        source = self.sourceModel()
        if sl.start is not None and sl.start < 0:
            count = source.rowCount() if typ == "row" else source.columnCount()
            start = count + sl.start
            end = count + sl.stop
            # end = start + (sl.stop - sl.start)
            if start < 0:
                raise IndexError(sl.start)
            sl = slice(start, end, sl.step)
        # if sl.stop is not None and sl.stop < 0:
        #     stop = source.columnCount() + sl.stop
        #     if stop < 0:
        #         raise IndexError(sl.stop)
        #     sl = slice(sl.start, stop, sl.step)
        return sl

    def set_indexer(self, indexer):
        """Takes basically anything which is common to use for __getitem__."""
        match indexer:
            case None:
                self._indexer = (slice(None), slice(None))
            case int() as column:
                self.set_column_slice(column)
            case slice() as col_slice:
                self._indexer = (col_slice, slice(None))
            case col_slice, row_slice:
                self.set_column_slice(col_slice)
                self.set_row_slice(row_slice)
            case _:
                raise TypeError(indexer)

    def get_column_slice(self) -> slice:
        match self._indexer:
            case None | (None, _):
                return slice(None)
            case (slice() as col_slice, _):
                # if (source := self.sourceModel()) is not None:
                #     col_slice = self.update_slice_boundaries(col_slice, typ="column")
                return col_slice
            case _:
                raise TypeError(self._indexer)

    def get_row_slice(self) -> slice:
        match self._indexer:
            case None | (_, None):
                return slice(None)
            case (_, slice() as row_slice):
                # if (source := self.sourceModel()) is not None:
                #     row_slice = self.update_slice_boundaries(row_slice, typ="row")
                return row_slice
            case _:
                raise TypeError(self._indexer)

    def set_column_slice(
        self, value: slice | int | None | tuple[int | None, int | None, int | None]
    ) -> slice:
        """Throw anything at this method in order to set the column slice."""
        match value:
            case slice() as col_slice:
                self._indexer = (col_slice, self.get_row_slice())
            case int() as col:
                self._indexer = (slice(col, col + 1), self.get_row_slice())
            case None:
                self._indexer = (slice(None), self.get_row_slice())
            case (
                int() | None as start,
                int() | None as stop,
                int() | None as step,
            ):
                row_slice = slice(start, stop, step)
                self._indexer = (row_slice, self.get_row_slice())
            case _:
                raise TypeError(value)

    def set_row_slice(
        self, value: slice | int | None | tuple[int | None, int | None, int | None]
    ) -> slice:
        """Throw anything at this method in order to set the row slice."""
        match value:
            case slice() as row_slice:
                self._indexer = (self.get_column_slice(), row_slice)
            case int() as row:
                self._indexer = (self.get_column_slice(), slice(row, row + 1))
            case None:
                self._indexer = (self.get_column_slice(), slice(None))
            case (int() | None as start, int() | None as stop, int() | None as step):
                row_slice = slice(start, stop, step)
                self._indexer = (self.get_column_slice(), row_slice)
            case _:
                raise TypeError(value)

    def get_row_range(self) -> range:
        """Return a range for the row slice with valid start / stop / step values."""
        sl = self.get_row_slice()
        row_count = self.sourceModel().rowCount()
        return range(sl.start or 0, sl.stop or row_count, sl.step or 1)

    def get_column_range(self) -> range:
        """Return a range for the column slice with valid start / stop / step values."""
        sl = self.get_column_slice()
        col_count = self.sourceModel().columnCount()
        return range(sl.start or 0, sl.stop or col_count, sl.step or 1)

    def position_in_column_slice(self, col: int) -> int:
        """Can be interpreted as slice.index(col) if slice would be a list."""
        sl = self.get_column_slice()
        return (col - (sl.start or 0)) / (sl.step or 1)

    def position_in_row_slice(self, row: int) -> int:
        """Can be interpreted as slice.index(row) if slice would be a list."""
        sl = self.get_row_slice()
        return (row - (sl.start or 0)) / (sl.step or 1)

    # The Qt typesystems dont like slices (or ranges / tuples)
    # seems what works is to throw tuples at a QtProperty declared as list.
    # otherwise change this to list getters/setters.

    def get_column_tuple(self) -> tuple[int | None, int | None, int | None]:
        """Get tuple representation of the column slice."""
        sl = self.get_column_slice()
        return (sl.start, sl.stop, sl.step)

    def get_row_tuple(self) -> tuple[int | None, int | None, int | None]:
        """Get tuple representation of the row slice."""
        sl = self.get_row_slice()
        return (sl.start, sl.stop, sl.step)

    column_slice = core.Property(list, get_column_tuple, set_column_slice)
    row_slice = core.Property(list, get_row_tuple, set_column_slice)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    table = widgets.TableView()
    table.set_model(["a", "b", "c"])
    table.proxifier.get_proxy("read_only", indexer=(0, 0))
    table.show()
    with app.debug_mode():
        app.main_loop()
