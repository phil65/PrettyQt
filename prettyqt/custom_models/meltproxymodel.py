from __future__ import annotations

from collections.abc import Sequence

from prettyqt import constants, core


class MeltProxyModel(core.AbstractProxyModel):
    def __init__(self, id_columns: Sequence[int], **kwargs):
        self.id_columns = id_columns
        self.var_name = None
        self.value_name = None
        super().__init__(**kwargs)

    @property
    def value_columns(self):
        return [
            i for i in range(self.sourceModel().columnCount()) if i not in self.id_columns
        ]

    def rowCount(self, index: core.ModelIndex | None = None):
        return self.sourceModel().rowCount() * len(self.value_columns)

    def columnCount(self, parent: core.ModelIndex | None = None):
        parent = parent or core.ModelIndex()
        return (
            0
            if self.sourceModel() is None
            else self.sourceModel().columnCount(parent) - len(self.id_columns) + 2
        )

    def is_source_column(self, column: int):
        return column < self.columnCount() - 2

    def is_variable_column(self, column: int):
        return column == self.columnCount() - 2

    def is_value_column(self, column: int):
        return column == self.columnCount() - 1

    def data(self, index, role):
        column = index.column()
        if self.is_source_column(column):
            return self.sourceModel().data(index, role)
        if self.is_variable_column(column) and role == constants.DISPLAY_ROLE:
            col = index.row() // self.sourceModel().rowCount()
            return self.sourceModel().headerData(
                self.value_columns[col], constants.HORIZONTAL
            )
        if self.is_value_column(column):
            col = index.row() // self.sourceModel().rowCount()
            row = index.row() % self.sourceModel().rowCount()
            index = self.sourceModel().index(row, self.value_columns[col])
            return index.data(role)

    def headerData(self, section: int, orientation, role=None):
        if orientation == constants.HORIZONTAL:
            if self.is_variable_column(section):
                return "Variable" if self.var_name is None else self.var_name
            elif self.is_value_column(section):
                return "Value" if self.value_name is None else self.value_name
            else:
                section = self.get_source_column_for_proxy_column(section)
                return self.sourceModel().headerData(section, orientation, role)
        else:
            return str(section)

    def index(self, row: int, column: int, parent: core.ModelIndex):
        if not self.is_source_column(column):
            return self.createIndex(row, column, core.ModelIndex())
        col_pos = self.get_source_column_for_proxy_column(column)
        # col_pos = column
        row_pos = row % self.sourceModel().rowCount()
        return self.sourceModel().index(row_pos, col_pos, parent)

    def parent(self, index: core.ModelIndex | None = None):
        if not self.is_source_column(index.column()):
            return core.ModelIndex()
        return self.sourceModel().parent(index)

    def get_source_column_for_proxy_column(self, column: int) -> int:
        return self.id_columns.index(column)

    def get_proxy_column_for_source_column(self, column: int) -> int:
        return column - sum(column > col for col in self.id_columns)

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        if not proxy_index.isValid():
            return core.ModelIndex()
        column = proxy_index.column()
        if not self.is_source_column(column):
            return core.ModelIndex()
        # col_pos = self.get_source_column_for_proxy_column(column)
        col_pos = column
        row_pos = proxy_index.row() % self.sourceModel().rowCount()
        return self.sourceModel().index(row_pos, col_pos, core.ModelIndex())

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if not self.is_source_column(source_index.column()):
            return core.ModelIndex()
        row, col = source_index.row(), source_index.column()
        row_pos = row if row < self.sourceModel().rowCount() else row / 2
        # col_pos = self.get_proxy_column_for_source_column(col)
        col_pos = col
        return self.sourceModel().index(row_pos, col_pos, core.ModelIndex())


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    table = debugging.example_table()
    model = MeltProxyModel(parent=table, id_columns=[0, 1])
    model.setSourceModel(table.model())
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
