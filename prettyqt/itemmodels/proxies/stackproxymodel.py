from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core


logger = logging.getLogger(__name__)


class StackProxyModel(core.AbstractProxyModel):
    """Proxy model to stack columns into rows.

    Transforms wide format with multiple columns into long format
    by stacking columns vertically. Similar to pandas.DataFrame.stack().

    === "Without proxy"

        ```py
        app = widgets.app()
        data = {
            ("Sales", "2020"): [100, 200],
            ("Sales", "2021"): [150, 250],
            ("Costs", "2020"): [80, 160],
            ("Costs", "2021"): [90, 180],
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
            ("Sales", "2020"): [100, 200],
            ("Sales", "2021"): [150, 250],
            ("Costs", "2020"): [80, 160],
            ("Costs", "2021"): [90, 180],
        }
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.stack()
        table.show()
        ```
    """

    ID = "stack"
    ICON = "mdi6.table-pivot"

    def __init__(self, level: int | None = None, **kwargs: Any):
        """Initialize StackProxyModel.

        Args:
            level: If headers are multi-level, which level to stack by.
                  None means stack all columns.
            kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self._level = level

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of rows in stacked format."""
        source = self.sourceModel()
        if not source:
            return 0
        return source.rowCount() * source.columnCount()

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of columns (always 2 - index and values)."""
        return 2

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return data for given index and role."""
        if not index.isValid():
            return None

        source = self.sourceModel()
        total_cols = source.columnCount()

        # Calculate original row and column
        source_row = index.row() // total_cols
        source_col = index.row() % total_cols

        # First column shows the header name
        if index.column() == 0:
            return source.headerData(source_col, constants.HORIZONTAL, role)

        # Second column shows the value
        source_index = source.index(source_row, source_col)
        return source.data(source_index, role)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return header data."""
        if orientation != constants.HORIZONTAL or role != constants.DISPLAY_ROLE:
            return None

        return ["Variable", "Value"][section]

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        """Map proxy index to source index."""
        if not proxy_index.isValid() or proxy_index.column() != 1:
            return core.ModelIndex()

        source = self.sourceModel()
        total_cols = source.columnCount()

        source_row = proxy_index.row() // total_cols
        source_col = proxy_index.row() % total_cols

        return source.index(source_row, source_col)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        """Map source index to proxy index."""
        if not source_index.isValid():
            return core.ModelIndex()

        proxy_row = (
            source_index.row() * self.sourceModel().columnCount() + source_index.column()
        )
        return self.index(proxy_row, 1)


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app(style="Windows")
    data = {
        ("Sales", "2020"): [100, 200],
        ("Sales", "2021"): [150, 250],
        ("Costs", "2020"): [80, 160],
        ("Costs", "2021"): [90, 180],
    }
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.setWindowTitle("StackProxyModel example")
    table.set_icon("mdi6.table-pivot")
    table.show()
    table.resize(600, 400)
    table.h_header.resize_sections("stretch")

    # Stack columns into rows
    table.proxifier.stack()

    with app.debug_mode():
        app.exec()
