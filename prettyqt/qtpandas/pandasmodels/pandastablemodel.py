from __future__ import annotations

import logging
import enum
from typing import Any

import numpy as np
import pandas as pd

from prettyqt import constants, core

logger = logging.getLogger(__name__)


class DataTableModel(core.AbstractTableModel):
    class Roles(enum.IntEnum):
        """Role names."""

        DTypeRole = constants.USER_ROLE + 4555
        ColumnNameRole = constants.USER_ROLE + 4556

    def __init__(self, df: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.df = df

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        pass

    def columnCount(self, parent: core.ModelIndex | None = None):
        if self.df is None:
            return 0
        return 1 if type(self.df) == pd.Series else len(self.df.columns)

    def rowCount(self, parent: core.ModelIndex | None = None):
        return len(self.df.index) if self.df is not None else 0

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                cell = self.df.iat[index.row(), index.column()]
                return "" if pd.isnull(cell) else cell
            case constants.TOOLTIP_ROLE:
                row = index.row()
                col = index.column()
                cell = self.df.iat[row, col]

                # NaN case
                return "NaN" if pd.isnull(cell) else str(cell)

            case self.Roles.DTypeRole:
                return self.df.iloc[:, index.column()].dtype
            case constants.USER_ROLE:
                return self.df.iloc[index.row(), index.column()]
            case self.Roles.ColumnNameRole:
                return self.df.iloc[:, index.column()].name

    def flags(self, index: core.ModelIndex):
        return constants.IS_EDITABLE | constants.IS_ENABLED | constants.IS_SELECTABLE

    #     return cur_flags if self.is_read_only else cur_flags | constants.IS_EDITABLE

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


class DataTableWithHeaderModel(DataTableModel):
    def __init__(self, *args, **kwargs):
        self._multiindex_separator = " | "
        super().__init__(*args, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, pd.DataFrame)

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
                if isinstance(header, tuple | list):
                    return self._multiindex_separator.join(str(i) for i in header)
                return str(header)
                # label = helpers.format_name(self.df.columns[section])
                # return f"{label}\n{self.df.iloc[:, section].dtype}"
            # case constants.DECORATION_ROLE, constants.HORIZONTAL if self.show_icons:
            #     dtype = self.df.iloc[:, section].dtype
            #     return icons.icon_for_dtype(dtype)
            case _, _:
                return None

    def set_multiindex_separator(self, separator: str):
        self._multiindex_separator = separator

    def get_multiindex_separator(self) -> str:
        return self._multiindex_separator

    _multiindex_separator = core.Property(
        str, get_multiindex_separator, set_multiindex_separator
    )


class VerticalHeaderModel(core.AbstractTableModel):
    def __init__(self, df: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.df = df

    def columnCount(self, parent: core.ModelIndex | None = None):
        return 0 if self.df is None else self.df.index.nlevels

    def rowCount(self, parent: core.ModelIndex | None = None):
        return 0 if self.df is None else self.df.index.shape[0]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE | constants.TOOLTIP_ROLE:
                row = index.row()
                col = index.column()
                if isinstance(self.df.index, pd.MultiIndex):
                    return str(self.df.index.values[row][col])
                else:
                    return str(self.df.index.values[row])

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match role, orientation:
            case constants.DISPLAY_ROLE | constants.TOOLTIP_ROLE, constants.HORIZONTAL:
                if isinstance(self.df.index, pd.MultiIndex):
                    return str(self.df.index.names[section])
                else:
                    return str(self.df.index.name)


class HorizontalHeaderModel(core.AbstractTableModel):
    def __init__(self, df: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.df = df

    def columnCount(self, parent: core.ModelIndex | None = None):
        return 0 if self.df is None else self.df.columns.shape[0]

    def rowCount(self, parent: core.ModelIndex | None = None):
        return 0 if self.df is None else self.df.columns.nlevels

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE | constants.TOOLTIP_ROLE:
                row = index.row()
                col = index.column()
                if isinstance(self.df.columns, pd.MultiIndex):
                    return str(self.df.columns.values[col][row])
                else:
                    return str(self.df.columns.values[col])
            case constants.ALIGNMENT_ROLE:
                return constants.ALIGN_CENTER

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role, orientation:
            case constants.DISPLAY_ROLE | constants.TOOLTIP_ROLE, constants.VERTICAL:
                if isinstance(self.df.columns, pd.MultiIndex):
                    return str(self.df.columns.names[section])
                else:
                    return str(self.df.columns.name)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    # Prepare data
    tuples = [
        ("bar", "one", "q"),
        ("bar", "two", "q"),
        ("baz", "one", "q"),
        ("baz", "two", "q"),
        ("foo", "one", "q"),
        ("foo", "two", "q"),
    ] * 10
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    df = pd.DataFrame(np.random.randn(60, 60), index=index, columns=index)
    table = widgets.TableView()
    table.show()
    model = DataTableWithHeaderModel(df, parent=table)
    model = model.proxifier[6:7, ::2].style("red", role=constants.FOREGROUND_ROLE)
    model = model.proxifier[1:4, ::2].style(
        "Courier", role=constants.FONT_ROLE, point_size=30
    )
    # model = model.proxifier[1:4, ::2].filter()
    table.set_model(model)
    print(table.get_models())
    # table.set_model(table.model().proxifier.get_proxy("color_values", parent=table))
    # model = model.proxifier.get_proxy("read_only")
    table.set_delegate("variant")

    app.main_loop()
