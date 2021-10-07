from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class TransposeProxyModel(core.AbstractProxyModel):
    def __init__(self, source_model: QtCore.QAbstractItemModel):
        super().__init__()
        self._source_model = source_model
        self.setSourceModel(source_model)

    def setSourceModel(self, source_model: QtCore.QAbstractItemModel):
        self._source_model = source_model
        super().setSourceModel(source_model)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        return self.index(source_index.column(), source_index.row())

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        return self._source_model.index(proxy_index.column(), proxy_index.row())

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: core.ModelIndex):  # type: ignore
        return None

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        if parent is None:
            parent = core.ModelIndex()
        return self._source_model.columnCount(parent)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        if parent is None:
            parent = core.ModelIndex()
        return self._source_model.rowCount(parent)

    def data(self, index: core.ModelIndex, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return False
        return self._source_model.data(self.mapFromSource(index), role)

    def headerData(self, section: int, orientation, role):  # type: ignore
        return self._source_model.headerData(section, orientation, role)
