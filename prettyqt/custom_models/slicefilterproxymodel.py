from __future__ import annotations

from prettyqt import constants, core, custom_models


class SliceFilterProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "slice_filter"

    def rowCount(self, index=None):
        rowcount = super().rowCount()
        return min(rowcount, self.get_row_slice().stop or rowcount)

    def columnCount(self, index=None):
        colcount = super().columnCount()
        return min(colcount, self.get_column_slice().stop or colcount)

    def headerData(self, section, orientation, role=None):
        if orientation == constants.HORIZONTAL:
            rng = self.get_column_range()
        else:
            rng = self.get_row_range()
        pos = rng.start + section * rng.step
        return super().headerData(pos, orientation, role)

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.Modelindex:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if row < 0 or column < 0 or source is None:
            return core.ModelIndex()
        source_parent = self.mapToSource(parent)
        col_range = self.get_column_range()
        row_range = self.get_row_range()
        col_pos = col_range.start + (col_range.step * column)
        row_pos = row_range.start + (row_range.step * row)
        source_index = source.index(row_pos, col_pos, source_parent)
        return self.mapFromSource(source_index)

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.Modelindex:
        source = self.sourceModel()
        if source is None or not proxy_idx.isValid():
            return core.ModelIndex()
        col_range = self.get_column_range()
        row_range = self.get_row_range()
        col_pos = col_range.start + (col_range.step * proxy_idx.column())
        row_pos = row_range.start + (row_range.step * proxy_idx.row())
        return source.index(row_pos, col_pos)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if (
            source is None
            or not source_index.isValid()
            # or not self.indexer_contains(source_index)
        ):
            return core.ModelIndex()
        row, col = source_index.row(), source_index.column()
        row_pos = self.position_in_row_slice(row)
        col_pos = self.position_in_column_slice(col)
        return self.createIndex(row_pos, col_pos, source_index.internalPointer())


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    table = debugging.example_table()
    model = SliceFilterProxyModel(parent=table)
    model.set_column_slice(slice(1, 4))
    model.setSourceModel(table.model())
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
