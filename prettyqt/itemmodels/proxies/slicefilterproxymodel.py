from __future__ import annotations

from prettyqt import constants, core, itemmodels


class SliceFilterProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model to filter an item view based on python slicing syntax.

    Since slicing operations are bijective, this model can filter without
    looping through rows or columns. Thus, this should perform much better than a
    SortFilterProxyModel with a column filter. (O(1) instead of O(n))

    ### Example

    To filter out every second row, and cut off the the first two columns:

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier[::2, 2:].filter()
    table.show()
    # or
    indexer = (slice(None, None, 2), slice(2, None))
    proxy = itemmodels.SliceFilterProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "slice_filter"
    ICON = "mdi.table-filter"

    def rowCount(self, index: core.ModelIndex | None = None) -> int:
        rowcount = super().rowCount()
        # TODO: not sure if slice.stop = 0 is covered correctly?
        return min(rowcount, self.get_row_slice().stop or rowcount)

    def columnCount(self, index: core.ModelIndex | None = None) -> int:
        colcount = super().columnCount()
        return min(colcount, self.get_column_slice().stop or colcount)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        """Map header data to proxy by calculating position from slice values.

        source pos = slice start + proxy pos * slice step)
        """
        is_horizontal = orientation == constants.HORIZONTAL
        rng = self.get_column_range() if is_horizontal else self.get_row_range()
        pos = rng.start + section * rng.step
        return super().headerData(pos, orientation, role)

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
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

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.ModelIndex:
        """Map index to source by calculating position from slice values.

        source pos = slice start + proxy pos * slice step)
        """
        source = self.sourceModel()
        if source is None or not proxy_idx.isValid():
            return core.ModelIndex()
        col_range = self.get_column_range()
        row_range = self.get_row_range()
        col_pos = col_range.start + (col_range.step * proxy_idx.column())
        row_pos = row_range.start + (row_range.step * proxy_idx.row())
        return source.index(row_pos, col_pos)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        """Map index from source by calculating position based on slice values.

        proxy pos = source pos - slice start / slice step
        """
        if self.sourceModel() is None or not source_index.isValid():
            return core.ModelIndex()
        row_pos = self.position_in_row_slice(source_index.row())
        col_pos = self.position_in_column_slice(source_index.column())
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
        app.exec()
