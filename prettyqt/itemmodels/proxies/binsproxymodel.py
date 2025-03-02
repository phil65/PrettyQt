from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from prettyqt import constants, core


if TYPE_CHECKING:
    from collections.abc import Sequence


logger = logging.getLogger(__name__)


class BinsProxyModel(core.AbstractProxyModel):
    """Proxy model to convert continuous data into categorical bins.

    === "Without proxy"

        ```py
        app = widgets.app()
        data = {
            "Name": ["John", "Alice", "Bob", "Carol", "Dave"],
            "Age": [22, 35, 44, 58, 65],
            "Income": [30000, 45000, 55000, 65000, 70000],
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
            "Age": [22, 35, 44, 58, 65],
            "Income": [30000, 45000, 55000, 65000, 70000],
        }
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.bins(
            column=1,  # Age column
            bins=[0, 30, 50, 70],  # Bin edges
            labels=["Young", "Middle", "Senior"]  # Labels for bins
        )
        table.show()
        ```
    """

    ID = "bins"
    ICON = "mdi6.chart-histogram"

    def __init__(
        self,
        column: int,
        bins: Sequence[float | int],
        labels: Sequence[str] | None = None,
        right: bool = True,
        **kwargs: Any,
    ):
        """Initialize BinsProxyModel.

        Args:
            column: Column index to bin
            bins: Bin edges (including leftmost and rightmost)
            labels: Labels for bins (length should be len(bins)-1)
            right: Whether bins includes the rightmost edge
            kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        self._column = column
        self._bins = list(bins)
        self._labels = list(labels) if labels is not None else None
        self._right = right

        if labels is not None and len(labels) != len(bins) - 1:
            msg = "Number of labels must be equal to number of bins - 1"
            raise ValueError(msg)

    def _get_bin(self, value: float | None) -> int | None:
        """Get bin index for value."""
        if value is None:
            return None

        for i, edge in enumerate(self._bins[1:], 1):
            if self._right:
                if value <= edge:
                    return i - 1
            elif value < edge:
                return i - 1
        return len(self._bins) - 2

    def _get_bin_label(self, bin_idx: int | None) -> str:
        """Get label for bin index."""
        if bin_idx is None:
            return ""

        if self._labels:
            return self._labels[bin_idx]

        # Create default label using bin edges
        left = self._bins[bin_idx]
        right = self._bins[bin_idx + 1]
        return f"[{left}, {right}{'[' if not self._right else ']'}"

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

        source_data = self.sourceModel().data(index, constants.EDIT_ROLE)

        try:
            value = float(source_data)
        except (ValueError, TypeError):
            return self.sourceModel().data(index, role)

        bin_idx = self._get_bin(value)

        if role == constants.DISPLAY_ROLE:
            return self._get_bin_label(bin_idx)
        if role == constants.EDIT_ROLE:
            return bin_idx

        return self.sourceModel().data(index, role)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> Any:
        """Return header data (same as source)."""
        return self.sourceModel().headerData(section, orientation, role)

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
        """Get column to bin."""
        return self._column

    def set_column(self, column: int):
        """Set column to bin."""
        with self.reset_model():
            self._column = column

    def get_bins(self) -> list[float]:
        """Get bin edges."""
        return self._bins

    def set_bins(self, bins: Sequence[float]):
        """Set bin edges."""
        with self.reset_model():
            self._bins = list(bins)

    def get_labels(self) -> list[str] | None:
        """Get bin labels."""
        return self._labels

    def set_labels(self, labels: Sequence[str] | None):
        """Set bin labels."""
        with self.reset_model():
            self._labels = list(labels) if labels is not None else None

    column = core.Property(
        int,
        get_column,
        set_column,
        doc="Column to bin",
    )
    bins = core.Property(
        list,
        get_bins,
        set_bins,
        doc="Bin edges",
    )
    labels = core.Property(
        list,
        get_labels,
        set_labels,
        doc="Bin labels",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app(style="Windows")
    data = {
        "Name": ["John", "Alice", "Bob", "Carol", "Dave"],
        "Age": [22, 35, 44, 58, 65],
        "Income": [30000, 45000, 55000, 65000, 70000],
    }
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.setWindowTitle("BinsProxyModel example")
    table.set_icon("mdi6.chart-histogram")
    table.show()
    table.resize(600, 200)
    table.h_header.resize_sections("stretch")

    # Convert Age into categories
    table.proxifier.bins(
        column=1,  # Age column
        bins=[0, 30, 50, 70],  # Bin edges
        labels=["Young", "Middle", "Senior"],  # Labels for bins
    )

    with app.debug_mode():
        app.exec()
