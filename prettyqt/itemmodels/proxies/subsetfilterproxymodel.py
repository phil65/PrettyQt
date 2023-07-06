from __future__ import annotations

from collections.abc import Callable, Container

from prettyqt import core
from prettyqt.utils import get_repr, helpers


class SubsetFilterProxyModel(core.SortFilterProxyModel):
    """A FilterProxyModel to filter based on slices, ranges, indexes or Callables.

    ### Example

    ```py
    proxy = itemmodels.SubsetFilterProxyModel()
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

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
                return helpers.is_in_slice(self.column_filter, source_column)
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
                return helpers.is_in_slice(self.row_filter, source_row)
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
