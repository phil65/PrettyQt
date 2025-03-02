from __future__ import annotations

import logging
from typing import Any, Literal

import numpy as np

from prettyqt import constants, core


logger = logging.getLogger(__name__)


RankMethod = Literal["average", "min", "max", "dense", "ordinal"]


class RankProxyModel(core.AbstractProxyModel):
    """Proxy model to compute numerical ranks for values.

    === "Without proxy"

        ```py
        app = widgets.app()
        data = {
            "Name": ["John", "Alice", "Bob", "Carol", "Dave"],
            "Score": [85, 92, 78, 92, 88],
            "Time": [120, 95, 150, 95, 110],
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
            "Name": ["John", "Alice", "Bob", "Carol", "Dave"],
            "Score": [85, 92, 78, 92, 88],
            "Time": [120, 95, 150, 95, 110],
        }
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.rank(
            column=1,  # Score column
            method="dense",  # ranking method
            ascending=False  # higher is better
        )
        table.show()
        ```
    """

    ID = "rank"
    ICON = "mdi6.order-numeric-ascending"

    def __init__(
        self,
        column: int,
        method: RankMethod = "average",
        ascending: bool = True,
        na_option: Literal["keep", "top", "bottom"] = "keep",
        **kwargs,
    ):
        """Initialize RankProxyModel.

        Args:
            column: Column to rank
            method: How to assign rank to equal values
                'average': average rank of the group
                'min': lowest rank in the group
                'max': highest rank in the group
                'dense': like 'min', but rank always increases by 1
                'ordinal': all values get unique rank
            ascending: Whether to rank in ascending order
            na_option: How to handle NA values
                'keep': keep NA values as NA
                'top': assign lowest rank to NA
                'bottom': assign highest rank to NA
            kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        self._column = column
        self._method = method
        self._ascending = ascending
        self._na_option = na_option
        # Cache for ranks since calculation is fast but not instant
        self._ranks: dict[int, float | None] = {}

    def _calculate_ranks(self) -> None:
        """Calculate ranks for current data."""
        source = self.sourceModel()
        if not source:
            return

        # Get values and their indices
        values = []
        indices = []
        na_indices = []

        for row in range(source.rowCount()):
            idx = source.index(row, self._column)
            val = source.data(idx, constants.EDIT_ROLE)
            try:
                val = float(val)
                values.append(val)
                indices.append(row)
            except (ValueError, TypeError):
                na_indices.append(row)

        if not values:
            return

        # Convert to numpy array for efficient ranking
        arr = np.array(values)
        if not self._ascending:
            arr = -arr

        # Calculate ranks
        if self._method == "ordinal":
            ranks = np.argsort(arr).argsort() + 1
        else:
            ties = {
                "average": "average",
                "min": "min",
                "max": "max",
                "dense": "dense",
            }[self._method]
            ranks = np.array(list(range(1, len(arr) + 1)), dtype=float)

            # Handle ties
            unique_values = np.unique(arr)
            for value in unique_values:
                mask = arr == value
                if ties == "average":
                    rank = ranks[mask].mean()
                elif ties == "min":
                    rank = ranks[mask].min()
                elif ties == "max":
                    rank = ranks[mask].max()
                elif ties == "dense":
                    rank = np.where(arr < value)[0].size + 1
                ranks[mask] = rank

        # Store ranks in cache
        self._ranks.clear()
        for idx, rank in zip(indices, ranks):
            self._ranks[idx] = rank

        # Handle NA values
        if na_indices:
            if self._na_option == "top":
                na_rank = 0
            elif self._na_option == "bottom":
                na_rank = len(values) + 1
            else:  # "keep"
                na_rank = None

            for idx in na_indices:
                self._ranks[idx] = na_rank

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of columns (same as source)."""
        return self.sourceModel().columnCount() if self.sourceModel() else 0

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Return number of rows (same as source)."""
        return self.sourceModel().rowCount() if self.sourceModel() else 0

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return data for given index and role."""
        if not index.isValid():
            return None

        # Only modify the specified column
        if index.column() != self._column:
            return self.sourceModel().data(index, role)

        # Calculate ranks if needed
        if not self._ranks:
            self._calculate_ranks()

        rank = self._ranks.get(index.row())

        if role == constants.DISPLAY_ROLE:
            return str(int(rank)) if rank is not None else ""
        if role == constants.EDIT_ROLE:
            return rank

        return self.sourceModel().data(index, role)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return header data (same as source)."""
        return self.sourceModel().headerData(section, orientation, role)

    def setSourceModel(self, model: core.QAbstractItemModel) -> None:
        """Set source model and clear cache."""
        super().setSourceModel(model)
        self._ranks.clear()

    def sourceDataChanged(
        self,
        top_left: core.ModelIndex,
        bottom_right: core.ModelIndex,
        roles: list[constants.ItemDataRole],
    ) -> None:
        """Handle source data changes."""
        # Only recalculate if the ranked column was changed
        if top_left.column() <= self._column <= bottom_right.column():
            self._ranks.clear()
        super().sourceDataChanged(top_left, bottom_right, roles)

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        """Map proxy index to source index (direct mapping)."""
        if not proxy_index.isValid():
            return core.ModelIndex()
        return self.sourceModel().index(proxy_index.row(), proxy_index.column())

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        """Map source index to proxy index (direct mapping)."""
        if not source_index.isValid():
            return core.ModelIndex()
        return self.index(source_index.row(), source_index.column())

    def get_column(self) -> int:
        """Get column to rank."""
        return self._column

    def set_column(self, column: int):
        """Set column to rank."""
        with self.reset_model():
            self._column = column
            self._ranks.clear()

    def get_method(self) -> RankMethod:
        """Get ranking method."""
        return self._method

    def set_method(self, method: RankMethod):
        """Set ranking method."""
        with self.reset_model():
            self._method = method
            self._ranks.clear()

    def get_ascending(self) -> bool:
        """Get sort order."""
        return self._ascending

    def set_ascending(self, ascending: bool):
        """Set sort order."""
        with self.reset_model():
            self._ascending = ascending
            self._ranks.clear()

    column = core.Property(
        int,
        get_column,
        set_column,
        doc="Column to rank",
    )
    method = core.Property(
        str,
        get_method,
        set_method,
        doc="Ranking method",
    )
    ascending = core.Property(
        bool,
        get_ascending,
        set_ascending,
        doc="Sort order",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app(style="Windows")
    data = {
        "Name": ["John", "Alice", "Bob", "Carol", "Dave"],
        "Score": [85, 92, 78, 92, 88],
        "Time": [120, 95, 150, 95, 110],
    }
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.setWindowTitle("RankProxyModel example")
    table.set_icon("mdi6.order-numeric-ascending")
    table.show()
    table.resize(600, 200)
    table.h_header.resize_sections("stretch")

    # Rank scores (higher is better)
    table.proxifier.rank(
        column=1,  # Score column
        method="dense",  # ranking method
        ascending=False,  # higher is better
    )

    with app.debug_mode():
        app.exec()
