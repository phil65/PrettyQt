from __future__ import annotations

import logging

from prettyqt import constants, core


logger = logging.getLogger(__name__)


class MeltProxyModel(core.AbstractProxyModel):
    """Proxy model to unpivot a table from wide format to long format.

    Works same way as [pandas.melt](https://shorturl.at/bhGI3).

    === "Without proxy"

        ```py
        app = widgets.app()
        data = dict(
            first=["John", "Mary"],
            last=["Doe", "Bo"],
            height=[5.5, 6.0],
            weight=[130, 150],
        )
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        # table.proxifier.melt(id_columns=[0, 1])
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/meltproxymodel_before.png)
        </figure>

    === "With proxy"

        ```py
        app = widgets.app()
        data = dict(
            first=["John", "Mary"],
            last=["Doe", "Bo"],
            height=[5.5, 6.0],
            weight=[130, 150],
        )
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.melt(id_columns=[0, 1])
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/meltproxymodel_after.png)
        </figure>

    ```py
    table.proxifier.melt(id_columns=[0, 1])
    # equals
    proxy = itemmodels.MeltProxyModel(id_columns=[0, 1])
    proxy.set_source_model(table.model())
    table.set_model(proxy)
    ```
    """

    ID = "melt"
    ICON = "mdi6.table-pivot"

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
        return 0 <= column < self.columnCount() - 2

    def is_variable_column(self, column: int) -> bool:
        return column == self.columnCount() - 2

    def is_value_column(self, column: int) -> bool:
        return column == self.columnCount() - 1

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None

        source = self.sourceModel()
        row, column = index.row(), index.column()
        source_row_count = source.rowCount()

        # Handle variable column
        if self.is_variable_column(column):
            if role == constants.DISPLAY_ROLE:
                col = row // source_row_count
                return source.headerData(self.value_columns[col], constants.HORIZONTAL)
            return None

        # Handle value column
        if self.is_value_column(column):
            source_col = self.value_columns[row // source_row_count]
            source_row = row % source_row_count
            source_index = source.index(source_row, source_col)
            return source.data(source_index, role)

        # Handle ID columns
        source_col = self.get_source_column_for_proxy_column(column)
        source_row = row % source_row_count
        source_index = source.index(source_row, source_col)
        return source.data(source_index, role)

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
        if self.is_value_column(section):
            return self._value_name or "Value"
        section = self.get_source_column_for_proxy_column(section)
        return self.sourceModel().headerData(section, orientation, role)

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        if parent and parent.isValid():
            return core.ModelIndex()

        if not (0 <= row < self.rowCount() and 0 <= column < self.columnCount()):
            return core.ModelIndex()

        return self.createIndex(row, column)

    def parent(self, index: core.ModelIndex):
        if not self.is_source_column(index.column()):
            return core.ModelIndex()
        return self.sourceModel().parent(index)

    def get_source_column_for_proxy_column(self, column: int) -> int:
        return self._id_columns.index(column)

    def get_proxy_column_for_source_column(self, column: int) -> int:
        return column - sum(column > col for col in self._id_columns)

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if source is None or not proxy_index.isValid():
            return core.ModelIndex()
        row, column = proxy_index.row(), proxy_index.column()
        row_count = source.rowCount()
        if self.is_variable_column(column):
            return core.ModelIndex()
        if self.is_value_column(column):
            source_col = self.value_columns[row // row_count]
            source_row = row % row_count
            return source.index(source_row, source_col, core.ModelIndex())
        source_col = self.get_source_column_for_proxy_column(column)
        source_row = row % row_count
        return source.index(source_row, source_col)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if not source_index.isValid():
            return core.ModelIndex()

        source = self.sourceModel()
        source_row = source_index.row()
        source_col = source_index.column()

        # Handle ID columns
        if source_col in self._id_columns:
            proxy_col = self._id_columns.index(source_col)
            base_row = source_row
            for val_col in self.value_columns:
                if val_col < source_col:
                    base_row += source.rowCount()
            return self.createIndex(base_row, proxy_col)

        # Handle value columns
        if source_col in self.value_columns:
            value_col_idx = self.value_columns.index(source_col)
            proxy_row = source_row + (value_col_idx * source.rowCount())
            return self.createIndex(proxy_row, self.columnCount() - 1)

        return core.ModelIndex()

    def get_id_columns(self) -> list[int]:
        """Get list of identifier columns."""
        return self._id_columns

    def set_id_columns(self, columns: list[int]):
        """Set identifier variable columns."""
        with self.reset_model():
            self._id_columns = columns

    def get_var_name(self) -> str:
        """Get variable column header."""
        return self._var_name

    def set_var_name(self, name: str):
        """Set header for variable column."""
        self._var_name = name
        section = self.columnCount() - 2
        self.headerDataChanged.emit(constants.HORIZONTAL, section, section)

    def get_value_name(self) -> str:
        """Get value column header."""
        return self._value_name

    def set_value_name(self, name: str):
        """Set header for value column."""
        self._value_name = name
        section = self.columnCount() - 1
        self.headerDataChanged.emit(constants.HORIZONTAL, section, section)

    id_columns = core.Property(
        list,
        get_id_columns,
        set_id_columns,
        doc="Columns to use as identifier variables",
    )
    var_name = core.Property(
        str,
        get_var_name,
        set_var_name,
        doc="Header for variable column",
    )
    value_name = core.Property(
        str,
        get_value_name,
        set_value_name,
        doc="Header for value column",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app(style="Windows")
    data = dict(
        first=["John", "Mary"],
        last=["Doe", "Bo"],
        height=[5.5, 6.0],
        weight=[130, 150],
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.setWindowTitle("MeltProxyModel example")
    table.set_icon("mdi6.table-pivot")
    table.show()
    table.resize(600, 130)
    table.h_header.resize_sections("stretch")
    table.proxifier.melt(id_columns=[0, 1])
    with app.debug_mode():
        app.exec()
