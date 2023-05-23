from __future__ import annotations

from prettyqt import core


class TableToListProxyModel(core.IdentityProxyModel):
    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if self.sourceModel() is None else 1

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if source is None:
            return 0
        return source.rowCount() * source.columnCount()

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.Modelindex:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if row < 0 or column < 0 or source is None:
            return core.ModelIndex()
        source_parent = self.mapToSource(parent)
        colcount = source.columnCount()
        source_index = source.index(row // colcount, row % colcount, source_parent)
        return self.mapFromSource(source_index)

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.Modelindex:
        source = self.sourceModel()
        if source is None or not proxy_idx.isValid():
            return core.ModelIndex()
        row = proxy_idx.row()
        colcount = source.columnCount()
        return source.index(row // colcount, row % colcount)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if source is None or not source_index.isValid():
            return core.ModelIndex()
        r = source_index.row() * source.columnCount() + source_index.column()
        return self.createIndex(r, 0, source_index.internalPointer())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    proxy = TableToListProxyModel()
