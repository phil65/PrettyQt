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
        self, index: tuple[slice, int] | tuple[int, slice]
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


class AbstractTableModel(AbstractTableModelMixin, QtCore.QAbstractTableModel):
    pass
