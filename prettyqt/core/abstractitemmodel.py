# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib
from typing import Optional

from qtpy import QtCore


class AbstractItemModel(QtCore.QAbstractItemModel):

    HEADER = []

    def headerData(self, offset: int, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.HEADER[offset]

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def rowCount(self, parent=None):
        return 0

    @contextlib.contextmanager
    def change_layout(self):
        self.layoutAboutToBeChanged.emit()
        yield None
        self.layoutChanged.emit()

    @contextlib.contextmanager
    def reset_model(self):
        self.beginResetModel()
        yield None
        self.endResetModel()

    @contextlib.contextmanager
    def remove_rows(self, first: Optional[int] = None,
                    last: Optional[int] = None, parent=None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveRows(parent, first, last)
        yield None
        self.endRemoveRows()

    @contextlib.contextmanager
    def remove_columns(self, first: Optional[int] = None,
                       last: Optional[int] = None, parent=None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveColumns(parent, first, last)
        yield None
        self.endRemoveColumns()

    @contextlib.contextmanager
    def insert_rows(self, first: Optional[int] = None,
                    last: Optional[int] = None, parent=None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginInsertRows(parent, first, last)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_columns(self, first: Optional[int] = None,
                       last: Optional[int] = None, parent=None):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginInsertColumns(parent, first, last)
        yield None
        self.endInsertColumns()
