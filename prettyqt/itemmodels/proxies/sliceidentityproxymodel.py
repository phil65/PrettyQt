from __future__ import annotations

import logging

from prettyqt import core


logger = logging.getLogger(__name__)


class SliceIdentityProxyModel(core.IdentityProxyModel):
    """Base model for slice proxy models.

    By itself, this proxy does nothing.
    It just provides all needed helper functions to deal with slices.
    `indexer_contains` should be just by subclasses in order to check whether the proxy
    should be applied.
    """

    def __init__(self, indexer=None, **kwargs):
        super().__init__(**kwargs)
        self._indexer = (slice(None), slice(None))
        self.set_indexer(indexer)

    def indexer_contains(self, index: core.ModelIndex | tuple[int, int]) -> bool:
        """Check whether given ModelIndex is included in our Indexer."""
        if isinstance(index, core.ModelIndex):
            parent = self.mapToSource(index.parent()) if index.isValid() else None
            row, column = index.row(), index.column()
        else:
            parent = None
            row, column = index
        return row in self.get_row_range(parent) and column in self.get_column_range()

    def update_slice_boundaries(self, sl: slice, count: int) -> slice:
        """Update slice boundaries by resolving negative indexes."""
        return slice(*sl.indices(count))

    def set_indexer(self, indexer):
        """Takes basically anything which is common to use for __getitem__."""
        match indexer:
            case None:
                self._indexer = (slice(None), slice(None))
            case int() as column:
                self.set_column_slice(column)
            case slice() as col_slice:
                self._indexer = (col_slice, slice(None))
            case row_slice, col_slice:
                self.set_column_slice(col_slice)
                self.set_row_slice(row_slice)
            case _:
                raise TypeError(indexer)

    def get_column_slice(self) -> slice:
        match self._indexer:
            case None | (_, None):
                return slice(None)
            case (_, slice() as col_slice):
                return col_slice
            case _:
                raise TypeError(self._indexer)

    def get_row_slice(self) -> slice:
        match self._indexer:
            case None | (None, _):
                return slice(None)
            case (slice() as row_slice, _):
                return row_slice
            case _:
                raise TypeError(self._indexer)

    def set_column_slice(
        self, value: slice | int | tuple[int | None, int | None, int | None] | None
    ):
        """Throw anything at this method in order to set the column slice."""
        match value:
            case slice() as col_slice:
                sl = col_slice
            case int() as col:
                sl = slice(col, col + 1)
            case None:
                sl = slice(None)
            case (
                int() | None as start,
                int() | None as stop,
                int() | None as step,
            ):
                sl = slice(start, stop, step)
            case _:
                raise TypeError(value)
        self._indexer = (self.get_row_slice(), sl)

    def set_row_slice(
        self, value: slice | int | tuple[int | None, int | None, int | None] | None
    ):
        """Throw anything at this method in order to set the row slice."""
        match value:
            case slice() as row_slice:
                sl = row_slice
            case int() as row:
                sl = slice(row, row + 1)
            case None:
                sl = slice(None)
            case (
                int() | None as start,
                int() | None as stop,
                int() | None as step,
            ):
                sl = slice(start, stop, step)
            case _:
                raise TypeError(value)
        self._indexer = (sl, self.get_column_slice())

    def get_row_range(self, parent: core.ModelIndex | None = None) -> range:
        """Return a range for the row slice with valid start / stop / step values.

        Arguments:
            parent: source parent index to get the range for (default: root)
        """
        source = self.sourceModel()
        row_count = 0 if source is None else source.rowCount(parent or core.ModelIndex())
        return range(*self.get_row_slice().indices(row_count))

    def get_column_range(self) -> range:
        """Return a range for the column slice with valid start / stop / step values."""
        source = self.sourceModel()
        col_count = 0 if source is None else source.columnCount()
        return range(*self.get_column_slice().indices(col_count))

    def position_in_column_slice(self, col: int) -> int:
        """Can be interpreted as slice.index(col) if slice would be a list."""
        return self.get_column_range().index(col)

    def position_in_row_slice(
        self, row: int, parent: core.ModelIndex | None = None
    ) -> int:
        """Can be interpreted as slice.index(row) if slice would be a list."""
        return self.get_row_range(parent).index(row)

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

    column_slice = core.Property(
        list,
        get_column_tuple,
        set_column_slice,
        doc="Column slice to include for the proxy",
    )
    row_slice = core.Property(
        list,
        get_row_tuple,
        set_column_slice,
        doc="Row slice to include for the proxy",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    data = dict(
        first=["John", "Mary"],
        last=["Doe", "Bo"],
        height=[5.5, 6.0],
        weight=[130, 150],
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier[-1].change_flags(enabled=False)
    model.insertColumn(0, [gui.StandardItem("new"), gui.StandardItem("new")])
    table.show()
    with app.debug_mode():
        app.exec()
