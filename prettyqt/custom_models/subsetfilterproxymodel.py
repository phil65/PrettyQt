from __future__ import annotations

from collections.abc import Callable, Container

from prettyqt import core
from prettyqt.utils import get_repr


def is_in_slice(a_slice: slice | range, idx: int) -> bool:
    start = a_slice.start or 0
    if idx < start or (a_slice.stop is not None and idx >= a_slice.stop):
        return False
    step = a_slice.step or 1
    return (idx - start) % step == 0


class SubsetFilterProxyModel(core.SortFilterProxyModel):
    ID = "subset"

    def __init__(
        self,
        row_filter: slice | range | int | Container[int] | Callable | None,
        column_filter: slice | range | int | Container[int] | Callable | None,
        **kwargs,
    ):
        self.row_filter = row_filter
        self.column_filter = column_filter
        super().__init__(**kwargs)

    def __repr__(self):
        return get_repr(self, self.row_filter, self.column_filter)

    def filterAcceptsColumn(self, source_column: int, parent: core.ModelIndex) -> bool:
        match self.column_filter:
            case slice() | range():
                return is_in_slice(self.column_filter, source_column)
            case int():
                return source_column == self.column_filter
            case Container():
                return source_column in self.column_filter
            case Callable():
                return self.column_filter(source_column)
            case None:
                return True
            case _:
                raise ValueError(self.column_filter)

    def filterAcceptsRow(self, source_row: int, parent: core.ModelIndex) -> bool:
        match self.row_filter:
            case slice() | range():
                return is_in_slice(self.row_filter, source_row)
            case int():
                return source_row == self.row_filter
            case Container():
                return source_row in self.row_filter
            case Callable():
                return self.row_filter(source_row)
            case None:
                return True
            case _:
                raise ValueError(self.row_filter)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    proxy = SubsetFilterProxyModel(1, 2)
