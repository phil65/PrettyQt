from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core


logger = logging.getLogger(__name__)


class UnmeltProxyModel(core.AbstractProxyModel):
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
        super().__init__(**kwargs)
        self._id_columns = id_columns
        self._variable_column = variable_column
        self._value_column = value_column
        self._unique_vars: list[str] = []
        self._unique_ids: list[tuple] = []

    def _update_cache(self):
        """Update internal cache of unique variables and IDs."""
        source = self.sourceModel()
        if source is None:
            return

        # Get unique variables
        variables = set()
        for row in range(source.rowCount()):
            idx = source.index(row, self._variable_column)
            var = str(source.data(idx, constants.DISPLAY_ROLE))
            variables.add(var)
        self._unique_vars = sorted(variables)

        # Get unique ID combinations
        id_combinations = set()
        for row in range(source.rowCount()):
            id_values = []
            for col in self._id_columns:
                idx = source.index(row, col)
                value = source.data(idx, constants.DISPLAY_ROLE)
                id_values.append(value)
            id_combinations.add(tuple(id_values))
        self._unique_ids = sorted(id_combinations)

    def sourceModelReset(self):
        """Handle source model reset."""
        self._update_cache()
        super().sourceModelReset()

    def setSourceModel(self, model):
        """Set source model and update cache."""
        result = super().setSourceModel(model)
        self._update_cache()
        return result

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of rows in the model."""
        return len(self._unique_ids)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of columns in the model."""
        return len(self._id_columns) + len(self._unique_vars)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return header data for given section and orientation."""
        if orientation != constants.HORIZONTAL or role != constants.DISPLAY_ROLE:
            return super().headerData(section, orientation, role)

        if section < len(self._id_columns):
            # Return original header for ID columns
            return self.sourceModel().headerData(
                self._id_columns[section], constants.HORIZONTAL, role
            )
        # Return variable name for value columns
        var_idx = section - len(self._id_columns)
        return self._unique_vars[var_idx]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return data for given index and role."""
        if not index.isValid():
            return None

        source = self.sourceModel()
        row, col = index.row(), index.column()

        # Handle ID columns
        if col < len(self._id_columns):
            id_values = self._unique_ids[row]
            return id_values[col]

        # Handle value columns
        var_name = self._unique_vars[col - len(self._id_columns)]
        id_values = self._unique_ids[row]

        # Find matching row in source model
        for source_row in range(source.rowCount()):
            # Check if ID values match
            matches = True
            for i, id_col in enumerate(self._id_columns):
                idx = source.index(source_row, id_col)
                if source.data(idx, constants.DISPLAY_ROLE) != id_values[i]:
                    matches = False
                    break

            # Check if variable matches
            if matches:
                var_idx = source.index(source_row, self._variable_column)
                if source.data(var_idx, constants.DISPLAY_ROLE) == var_name:
                    value_idx = source.index(source_row, self._value_column)
                    return source.data(value_idx, role)

        return None

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        """Map proxy index to source index."""
        if not proxy_index.isValid():
            return core.ModelIndex()

        row, col = proxy_index.row(), proxy_index.column()

        # ID columns map directly
        if col < len(self._id_columns):
            id_values = self._unique_ids[row]
            # Find matching row in source
            for source_row in range(self.sourceModel().rowCount()):
                matches = True
                for i, id_col in enumerate(self._id_columns):
                    idx = self.sourceModel().index(source_row, id_col)
                    if self.sourceModel().data(idx) != id_values[i]:
                        matches = False
                        break
                if matches:
                    return self.sourceModel().index(source_row, self._id_columns[col])

        return core.ModelIndex()

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        """Map source index to proxy index."""
        if not source_index.isValid():
            return core.ModelIndex()

        source_row, source_col = source_index.row(), source_index.column()

        # Handle ID columns
        if source_col in self._id_columns:
            # Get ID values for this row
            id_values = []
            for col in self._id_columns:
                idx = self.sourceModel().index(source_row, col)
                id_values.append(self.sourceModel().data(idx))
            id_tuple = tuple(id_values)

            try:
                proxy_row = self._unique_ids.index(id_tuple)
                proxy_col = self._id_columns.index(source_col)
                return self.createIndex(proxy_row, proxy_col)
            except ValueError:
                return core.ModelIndex()

        return core.ModelIndex()


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
