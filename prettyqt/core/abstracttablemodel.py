from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class AbstractTableModelMixin(core.AbstractItemModelMixin):
    def __getitem__(
        self, index: tuple[int | slice, int | slice]
    ) -> QtCore.QModelIndex | list[QtCore.QModelIndex]:
        row, col = index
        match row, col:
            case slice(), slice():
                raise ValueError("Only one of indexes can be a slice")
            case slice(), int():
                count = self.rowCount() if row.stop is None else row.stop
                values = list(range(count)[row])
                return [self.index(i, col) for i in values]
            case int(), slice():
                count = self.columnCount() if col.stop is None else col.stop
                values = list(range(col.stop)[col])
                return [self.index(row, i) for i in values]
            case int(), int():
                return self.index(row, col)


class AbstractTableModel(AbstractTableModelMixin, QtCore.QAbstractTableModel):
    pass
