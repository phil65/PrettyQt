# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core


class TransposeProxyModel(QtCore.QAbstractProxyModel):

    def __init__(self, source_model):
        super().__init__()
        self._source_model = None
        self.setSourceModel(source_model)

    def setSourceModel(self, source_model):
        self._source_model = source_model
        super().setSourceModel(source_model)

    def mapFromSource(self, source_index):
        return self.index(source_index.column(), source_index.row())

    def mapToSource(self, proxy_index):
        return self._source_model.index(proxy_index.column(), proxy_index.row())

    def index(self, row: int, column: int, parent=None) -> QtCore.QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index):
        return None

    def rowCount(self, parent=core.ModelIndex()) -> int:
        return self._source_model.columnCount(parent)

    def columnCount(self, parent=core.ModelIndex()) -> int:
        return self._source_model.rowCount(parent)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return False
        return self._source_model.data(self.mapFromSource(index), role)

    def headerData(self, section: int, orientation, role):
        return self._source_model.headerData(section, orientation, role)
