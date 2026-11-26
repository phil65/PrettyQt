from __future__ import annotations

import logging
from typing import Any, Literal

from prettyqt import constants, core


logger = logging.getLogger(__name__)


RankMethod = Literal["average", "min", "max", "dense", "ordinal"]


class RankProxyModel(core.IdentityProxyModel):
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
        # attributes need to exist before super().__init__, since a source_model kwarg
        # calls setSourceModel during init.
        self._column = column
        self._method = method
        self._ascending = ascending
        self._na_option = na_option
        # Cache for ranks, keyed by source parent and row. None means "invalid".
        self._ranks: dict[tuple, dict[int, float | None]] = {}
        super().__init__(**kwargs)

    def _clear_cache(self, *_args):
        self._ranks.clear()

    def setSourceModel(self, model: core.QAbstractItemModel | None) -> None:
        """Set source model and clear cache."""
        if (old := self.sourceModel()) is not None:
            for signal in self._cache_signals(old):
                signal.disconnect(self._clear_cache)
        super().setSourceModel(model)
        self._clear_cache()
        if model is not None:
            for signal in self._cache_signals(model):
                signal.connect(self._clear_cache)

    @staticmethod
    def _cache_signals(model: core.QAbstractItemModel):
        return [
            model.dataChanged,
            model.rowsInserted,
            model.rowsRemoved,
            model.rowsMoved,
            model.modelReset,
            model.layoutChanged,
        ]

    def _calculate_ranks(self, parent: core.ModelIndex) -> dict[int, float | None]:
        """Calculate ranks for the rows below given source parent."""
        source = self.sourceModel()
        values: dict[int, float] = {}
        na_rows: list[int] = []
        for row in range(source.rowCount(parent)):
            val = source.index(row, self._column, parent).data(constants.EDIT_ROLE)
            try:
                values[row] = float(val)
            except ValueError, TypeError:
                na_rows.append(row)
        ranks: dict[int, float | None] = {}
        rows = sorted(values, key=values.__getitem__, reverse=not self._ascending)
        position = 0
        dense_rank = 0
        while position < len(rows):
            # find group of equal values
            end = position
            while end + 1 < len(rows) and values[rows[end + 1]] == values[rows[position]]:
                end += 1
            dense_rank += 1
            first, last = position + 1, end + 1  # 1-based ranks of the group
            for offset, row in enumerate(rows[position : end + 1]):
                match self._method:
                    case "average":
                        ranks[row] = (first + last) / 2
                    case "min":
                        ranks[row] = first
                    case "max":
                        ranks[row] = last
                    case "dense":
                        ranks[row] = dense_rank
                    case "ordinal":
                        ranks[row] = first + offset
                    case _:
                        raise ValueError(self._method)
            position = end + 1
        match self._na_option:
            case "top":
                na_rank = 0
            case "bottom":
                na_rank = len(values) + 1
            case _:
                na_rank = None
        for row in na_rows:
            ranks[row] = na_rank
        return ranks

    def _get_rank(self, source_index: core.ModelIndex) -> float | None:
        parent = source_index.parent()
        key = (
            (parent.row(), parent.column(), parent.internalId())
            if parent.isValid()
            else ()
        )
        if key not in self._ranks:
            self._ranks[key] = self._calculate_ranks(parent)
        return self._ranks[key].get(source_index.row())

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return data for given index and role."""
        if not index.isValid():
            return None
        if index.column() != self._column or role not in (
            constants.DISPLAY_ROLE,
            constants.EDIT_ROLE,
        ):
            return super().data(index, role)
        rank = self._get_rank(self.mapToSource(index))
        if role == constants.EDIT_ROLE:
            return rank
        if rank is None:
            return ""
        return str(int(rank)) if float(rank).is_integer() else str(rank)

    def get_column(self) -> int:
        """Get column to rank."""
        return self._column

    def set_column(self, column: int):
        """Set column to rank."""
        with self.reset_model():
            self._column = column
            self._clear_cache()

    def get_method(self) -> RankMethod:
        """Get ranking method."""
        return self._method

    def set_method(self, method: RankMethod):
        """Set ranking method."""
        with self.reset_model():
            self._method = method
            self._clear_cache()

    def get_ascending(self) -> bool:
        """Get sort order."""
        return self._ascending

    def set_ascending(self, ascending: bool):
        """Set sort order."""
        with self.reset_model():
            self._ascending = ascending
            self._clear_cache()

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
