from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core
from prettyqt.itemmodels.proxies.flatproxymodel import FlatProxyModel


logger = logging.getLogger(__name__)


class UnmeltProxyModel(FlatProxyModel):
    """Proxy model to pivot a table from long format to wide format.

    Reverses the MeltProxyModel operation.

    === "Without proxy"

        ```py
        app = widgets.app()
        data = {
            "ID": ["A", "A", "B", "B"] * 2,
            "Variable": ["height", "weight"] * 4,
            "Value": [5.5, 130, 6.0, 150, 5.7, 140, 5.9, 145],
        }
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.show()
        ```

    === "With proxy"

        ```py
        app = widgets.app()
        data = {
            "ID": ["A", "A", "B", "B"] * 2,
            "Variable": ["height", "weight"] * 4,
            "Value": [5.5, 130, 6.0, 150, 5.7, 140, 5.9, 145],
        }
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.unmelt(id_columns=[0], variable_column=1, value_column=2)
        table.show()
        ```
    """

    ID = "unmelt"
    ICON = "mdi6.table-pivot"

    def __init__(
        self,
        id_columns: list[int],
        variable_column: int,
        value_column: int,
        **kwargs,
    ):
        """Initialize UnmeltProxyModel.

        Args:
            id_columns: List of column indices that identify unique rows
            variable_column: Column index containing variable names
            value_column: Column index containing values
            kwargs: Additional keyword arguments.
        """
        self._id_columns = id_columns
        self._variable_column = variable_column
        self._value_column = value_column
        self._unique_vars: list[str] = []
        self._unique_ids: list[tuple] = []
        # (id tuple, variable name) -> source row
        self._lookup: dict[tuple[tuple, str], int] = {}
        # id tuple -> first source row with these ids
        self._id_rows: dict[tuple, int] = {}
        super().__init__(**kwargs)

    def _get_ids(self, source_row: int) -> tuple:
        source = self.sourceModel()
        return tuple(source.index(source_row, col).data() for col in self._id_columns)

    def _update_cache(self):
        """Update internal cache of unique variables and IDs."""
        self._lookup.clear()
        self._id_rows.clear()
        source = self.sourceModel()
        if source is None:
            self._unique_vars, self._unique_ids = [], []
            return
        variables: dict[str, None] = {}
        for row in range(source.rowCount()):
            var = str(source.index(row, self._variable_column).data())
            ids = self._get_ids(row)
            variables[var] = None
            self._id_rows.setdefault(ids, row)
            self._lookup.setdefault((ids, var), row)
        self._unique_vars = sorted(variables)
        # keep order of first appearance (ids may not be sortable)
        self._unique_ids = list(self._id_rows)

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of rows in the model."""
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._unique_ids)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of columns in the model."""
        parent = parent or core.ModelIndex()
        if parent.isValid() or self.sourceModel() is None:
            return 0
        return len(self._id_columns) + len(self._unique_vars)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return header data for given section and orientation."""
        if orientation != constants.HORIZONTAL or role != constants.DISPLAY_ROLE:
            return None
        if section < len(self._id_columns):
            # Return original header for ID columns
            return self.sourceModel().headerData(
                self._id_columns[section], constants.HORIZONTAL, role
            )
        # Return variable name for value columns
        var_idx = section - len(self._id_columns)
        return self._unique_vars[var_idx] if var_idx < len(self._unique_vars) else None

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return data for given index and role."""
        source_index = self.mapToSource(index)
        return source_index.data(role) if source_index.isValid() else None

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        """Map proxy index to source index."""
        if not proxy_index.isValid() or self.sourceModel() is None:
            return core.ModelIndex()
        row, col = proxy_index.row(), proxy_index.column()
        ids = self._unique_ids[row]
        if col < len(self._id_columns):
            source_row = self._id_rows[ids]
            return self.sourceModel().index(source_row, self._id_columns[col])
        var_name = self._unique_vars[col - len(self._id_columns)]
        if (source_row := self._lookup.get((ids, var_name))) is None:
            return core.ModelIndex()
        return self.sourceModel().index(source_row, self._value_column)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        """Map source index to proxy index."""
        if not source_index.isValid() or source_index.parent().isValid():
            return core.ModelIndex()
        source_row, source_col = source_index.row(), source_index.column()
        ids = self._get_ids(source_row)
        if ids not in self._id_rows:
            return core.ModelIndex()
        proxy_row = self._unique_ids.index(ids)
        if source_col in self._id_columns:
            return self.index(proxy_row, self._id_columns.index(source_col))
        if source_col == self._value_column:
            var = str(self.sourceModel().index(source_row, self._variable_column).data())
            proxy_col = len(self._id_columns) + self._unique_vars.index(var)
            return self.index(proxy_row, proxy_col)
        return core.ModelIndex()

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        source_index = self.mapToSource(index)
        if not source_index.isValid():
            return constants.NO_FLAGS if index.isValid() else super().flags(index)
        return self.sourceModel().flags(source_index)


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app(style="Windows")
    data = {
        "ID": ["A", "A", "B", "B"] * 2,
        "Variable": ["height", "weight"] * 4,
        "Value": [5.5, 130, 6.0, 150, 5.7, 140, 5.9, 145],
    }
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.setWindowTitle("UnmeltProxyModel example")
    table.set_icon("mdi6.table-pivot")
    table.show()
    table.resize(600, 130)
    table.h_header.resize_sections("stretch")
    table.proxifier.unmelt(id_columns=[0], variable_column=1, value_column=2)
    with app.debug_mode():
        app.exec()
