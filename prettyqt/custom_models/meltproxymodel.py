from __future__ import annotations

from prettyqt import constants, core


class MeltProxyModel(core.AbstractProxyModel):
    ID = "melt"

    def __init__(
        self,
        id_columns: list[int],
        var_name: str = "Variable",
        value_name: str = "Value",
        **kwargs,
    ):
        self._id_columns = id_columns
        self._var_name = var_name
        self._value_name = value_name
        super().__init__(**kwargs)

    @property
    def value_columns(self) -> list[int]:
        colcount = self.sourceModel().columnCount()
        return [i for i in range(colcount) if i not in self._id_columns]

    def rowCount(self, index: core.ModelIndex | None = None) -> int:
        return self.sourceModel().rowCount() * len(self.value_columns)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if self.sourceModel() is None else len(self._id_columns) + 2

    def is_source_column(self, column: int) -> bool:
        return column < self.columnCount() - 2

    def is_variable_column(self, column: int) -> bool:
        return column == self.columnCount() - 2

    def is_value_column(self, column: int) -> bool:
        return column == self.columnCount() - 1

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        column = index.column()
        if self.is_variable_column(column) and role == constants.DISPLAY_ROLE:
            col = index.row() // self.sourceModel().rowCount()
            return self.sourceModel().headerData(
                self.value_columns[col], constants.HORIZONTAL
            )
        return super().data(index, role)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if orientation != constants.HORIZONTAL:
            return str(section)
        if self.is_variable_column(section):
            return self._var_name or "Variable"
        elif self.is_value_column(section):
            return self._value_name or "Value"
        else:
            section = self.get_source_column_for_proxy_column(section)
            return self.sourceModel().headerData(section, orientation, role)

    def index(self, row: int, column: int, parent: core.ModelIndex):
        if column in self._id_columns:
            col_pos = self.get_source_column_for_proxy_column(column)
            row_pos = row % self.sourceModel().rowCount()
            return self.sourceModel().index(row_pos, col_pos, parent)
        else:
            return self.createIndex(row, column, core.ModelIndex())

    def parent(self, index: core.ModelIndex):
        if not self.is_source_column(index.column()):
            return core.ModelIndex()
        return self.sourceModel().parent(index)

    def get_source_column_for_proxy_column(self, column: int) -> int:
        return self._id_columns.index(column)

    def get_proxy_column_for_source_column(self, column: int) -> int:
        return column - sum(column > col for col in self._id_columns)

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        if not proxy_index.isValid():
            return core.ModelIndex()
        column = proxy_index.column()
        row_count = self.sourceModel().rowCount()
        if self.is_variable_column(column):
            return core.ModelIndex()
        elif self.is_value_column(column):
            col = self.value_columns[proxy_index.row() // row_count]
            row = proxy_index.row() % row_count
            return self.sourceModel().index(row, col, core.ModelIndex())
        else:
            col = self.get_source_column_for_proxy_column(column)
            row = proxy_index.row() % row_count
            return self.sourceModel().index(row, col)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        # TODO: this is still broken.
        row, col = source_index.row(), source_index.column()
        if col in self._id_columns:
            row_pos = row if row < self.sourceModel().rowCount() else row / 2
            # col_pos = self.get_proxy_column_for_source_column(col)
            col_pos = col
            return self.sourceModel().index(row_pos, col_pos, core.ModelIndex())
        else:
            return core.ModelIndex()

    def get_id_columns(self) -> list[int]:
        return self._id_columns

    def set_id_columns(self, columns: list[int]):
        self._id_columns = columns

    def get_var_name(self) -> str:
        return self._var_name

    def set_var_name(self, name: str):
        self._var_name = name

    def get_value_name(self) -> str:
        return self._value_name

    def set_value_name(self, name: str):
        self._value_name = name

    id_columns = core.Property(list, get_id_columns, set_id_columns)
    var_name = core.Property(str, get_var_name, set_var_name)
    value_name = core.Property(str, get_value_name, set_value_name)


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
