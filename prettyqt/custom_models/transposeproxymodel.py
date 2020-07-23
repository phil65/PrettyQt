# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core


class TransposeProxyModel(core.AbstractProxyModel):
    def __init__(self, source_model):
        super().__init__()
        self._source_model = source_model
        self.setSourceModel(source_model)

    def setSourceModel(self, source_model: QtCore.QAbstractItemModel):
        self._source_model = source_model
        super().setSourceModel(source_model)

    def mapFromSource(self, source_index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        return self.index(source_index.column(), source_index.row())

    def mapToSource(self, proxy_index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        return self._source_model.index(proxy_index.column(), proxy_index.row())

    def index(self, row: int, column: int, parent=None) -> QtCore.QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: QtCore.QModelIndex):
        return None

    def rowCount(self, parent=core.ModelIndex()) -> int:
        return self._source_model.columnCount(parent)

    def columnCount(self, parent=core.ModelIndex()) -> int:
        return self._source_model.rowCount(parent)

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return False
        return self._source_model.data(self.mapFromSource(index), role)

    def headerData(self, section: int, orientation, role):
        return self._source_model.headerData(section, orientation, role)
