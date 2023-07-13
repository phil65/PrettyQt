from __future__ import annotations

import enum
import logging

from typing import Any

import polars as pl

from prettyqt import constants, core


logger = logging.getLogger(__name__)


class PolarsDataFrameModel(core.AbstractTableModel):
    """Model to display polars DataFrames."""

    SUPPORTS = pl.DataFrame

    class Roles(enum.IntEnum):
        """Role names."""

        DTypeRole = constants.USER_ROLE + 4555
        ColumnNameRole = constants.USER_ROLE + 4556

    def __init__(self, df: pl.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.df = df

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, pl.DataFrame)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role, orientation:
            case constants.ALIGNMENT_ROLE, constants.HORIZONTAL:
                return constants.ALIGN_CENTER | constants.ALIGN_BOTTOM
            case constants.DISPLAY_ROLE, constants.HORIZONTAL:
                header = self.df.columns[section]
                return str(header)
            case _, _:
                return None

    def columnCount(self, parent: core.ModelIndex | None = None):
        if self.df is None:
            return 0
        return len(self.df.columns)

    def rowCount(self, parent: core.ModelIndex | None = None):
        return len(self.df) if self.df is not None else 0

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                cell = self.df[index.row(), index.column()]
                return str(cell)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        return constants.IS_EDITABLE | constants.IS_ENABLED | constants.IS_SELECTABLE

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                row = index.row()
                col = index.column()
                try:
                    self.df.iat[row, col] = value
                except Exception as e:
                    logger.exception(e)
                    return False
                else:
                    self.dataChanged.emit(index, index)
                    return True
        return False

    def sort(self, ncol: int, order: constants.SortOrder):
        is_ascending = order == constants.ASCENDING
        with self.change_layout():
            self.df = self.df.sort_values(
                by=self.df.columns[ncol], ascending=is_ascending
            )
        self.update_all()


if __name__ == "__main__":
    from datetime import datetime

    from prettyqt import widgets

    app = widgets.app()
    df = pl.DataFrame(
        {
            "integer": [1, 2, 3],
            "date": [
                datetime(2022, 1, 1),
                datetime(2022, 1, 2),
                datetime(2022, 1, 3),
            ],
            "float": [4.0, 5.0, 6.0],
        }
    )
    table = widgets.TableView()
    table.show()
    model = PolarsDataFrameModel(df, parent=table)
    table.set_model(model)
    table.set_delegate("editor")

    app.exec()
