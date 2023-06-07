from __future__ import annotations

from typing import overload

from prettyqt import constants, core
from prettyqt.qt import QtCore


class AbstractTableModelMixin(core.AbstractItemModelMixin):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED
        | constants.IS_ENABLED
        | constants.IS_SELECTABLE
        | constants.NO_CHILDREN
    )

    @overload
    def __getitem__(self, index: tuple[int, int]) -> QtCore.QModelIndex:
        ...

    @overload
    def __getitem__(
        self, index: tuple[slice, int] | tuple[int, slice] | tuple[slice, slice]
    ) -> list[QtCore.QModelIndex]:
        ...

    def __getitem__(
        self, index: tuple[int | slice, int | slice]
    ) -> QtCore.QModelIndex | list[QtCore.QModelIndex]:
        match index:
            case slice() as row, slice() as col:
                rowcount = self.rowCount() if row.stop is None else row.stop
                colcount = self.columnCount() if col.stop is None else col.stop
                rowvalues = list(range(rowcount)[row])
                colvalues = list(range(colcount)[col])
                return [self.index(i, j) for i in rowvalues for j in colvalues]
            case slice() as row, int() as col:
                count = self.rowCount() if row.stop is None else row.stop
                values = list(range(count)[row])
                return [self.index(i, col) for i in values]
            case int() as row, slice() as col:
                count = self.columnCount() if col.stop is None else col.stop
                values = list(range(count)[col])
                return [self.index(row, i) for i in values]
            case int() as row, int() as col:
                return self.index(row, col)
            case _:
                raise TypeError(index)

    def to_dataframe(
        self,
        include_index: bool = False,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        x_range: slice | int | None = None,
        y_range: slice | int | None = None,
    ):
        match x_range:
            case None:
                colrange = range(self.columnCount())
            case slice():
                colrange = range(
                    x_range.start or 0,
                    x_range.stop or self.columnCount(),
                    x_range.step or 1,
                )
            case int():
                colrange = range(x_range, x_range + 1)

        match y_range:
            case None:
                rowrange = range(self.rowCount())
            case slice():
                rowrange = range(
                    y_range.start or 0,
                    y_range.stop or self.rowCount(),
                    y_range.step or 1,
                )
            case int():
                rowrange = range(y_range, y_range + 1)

        data = [[self.index(i, j).data(role) for j in colrange] for i in rowrange]
        h_header = [self.headerData(i, constants.HORIZONTAL) for i in colrange]
        v_header = (
            [self.headerData(i, constants.VERTICAL) for i in rowrange]
            if include_index
            else None
        )
        import pandas as pd

        return pd.DataFrame(data=data, columns=h_header, index=v_header)


class AbstractTableModel(AbstractTableModelMixin, QtCore.QAbstractTableModel):
    pass
