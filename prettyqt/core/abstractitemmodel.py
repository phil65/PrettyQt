# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib
from typing import Optional

from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractItemModel.__bases__ = (core.Object,)


class AbstractItemModel(QtCore.QAbstractItemModel):

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.rowCount()} children"

    def __len__(self) -> int:
        """return amount of rows
        """
        return self.rowCount()

    def rows(self) -> int:
        return self.rowCount()

    def columns(self) -> int:
        return self.columnCount()

    @contextlib.contextmanager
    def change_layout(self):
        """content manager to change the layout

        wraps calls with correct signals
        emitted at beginning: layoutAboutToBeChanged
        emitted at end: layoutChanged

        """
        self.layoutAboutToBeChanged.emit()
        yield None
        self.layoutChanged.emit()

    @contextlib.contextmanager
    def reset_model(self):
        """content manager to reset the model

        wraps calls with correct signals
        emitted at beginning: beginResetModel
        emitted at end: endResetModel

        """
        self.beginResetModel()
        yield None
        self.endResetModel()

    def update_row(self, row: int):
        start_index = self.index(row, 0)
        end_index = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(start_index, end_index)

    @contextlib.contextmanager
    def remove_rows(self,
                    first: Optional[int] = None,
                    last: Optional[int] = None,
                    parent: Optional[QtCore.QModelIndex] = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveRows(parent, first, last)
        yield None
        self.endRemoveRows()

    @contextlib.contextmanager
    def remove_columns(self,
                       first: Optional[int] = None,
                       last: Optional[int] = None,
                       parent: Optional[QtCore.QModelIndex] = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveColumns(parent, first, last)
        yield None
        self.endRemoveColumns()

    @contextlib.contextmanager
    def insert_rows(self,
                    first: Optional[int] = None,
                    last: Optional[int] = None,
                    parent: Optional[QtCore.QModelIndex] = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginInsertRows(parent, first, last)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def append_rows(self,
                    num_rows: int,
                    parent: Optional[QtCore.QModelIndex] = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        self.beginInsertRows(parent, self.rowCount(), self.rowCount() + num_rows - 1)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_columns(self,
                       first: Optional[int] = None,
                       last: Optional[int] = None,
                       parent: Optional[QtCore.QModelIndex] = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginInsertColumns(parent, first, last)
        yield None
        self.endInsertColumns()
