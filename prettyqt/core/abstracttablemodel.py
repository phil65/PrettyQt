from __future__ import annotations

from typing import overload

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import helpers, listdelegators


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
    ) -> listdelegators.BaseListDelegator[QtCore.QModelIndex]:
        ...

    def __getitem__(
        self, index: tuple[int | slice, int | slice]
    ) -> QtCore.QModelIndex | listdelegators.BaseListDelegator[QtCore.QModelIndex]:
        match index:
            case int() as row, int() as col:
                return self.index(row, col)
            case (row, col):
                indexes = [
                    self.index(i, j)
                    for i, j in helpers.yield_positions(
                        row, col, self.rowCount(), self.columnCount()
                    )
                ]
                return listdelegators.BaseListDelegator(indexes)
            case _:
                raise TypeError(index)

    def set_data(
        self, index: tuple[int | slice, int | slice], value, role=constants.EDIT_ROLE
    ):
        match index:
            case core.ModelIndex():
                self.setData(index, value, role)
            case (row, col):
                for i, j in helpers.yield_positions(
                    row, col, self.rowCount(), self.columnCount()
                ):
                    self.setData(self.index(i, j), value, role)
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
                stop = x_range.stop or self.columnCount()
                colrange = range(x_range.start or 0, stop, x_range.step or 1)
            case int():
                colrange = range(x_range, x_range + 1)

        match y_range:
            case None:
                rowrange = range(self.rowCount())
            case slice():
                stop = y_range.stop or self.rowCount()
                rowrange = range(y_range.start or 0, stop, y_range.step or 1)
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
