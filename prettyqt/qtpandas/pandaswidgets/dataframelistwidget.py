from __future__ import annotations

import numpy as np
import pandas as pd

from prettyqt import constants, core, custom_models, widgets
from prettyqt.qtpandas import pandasmodels


class RowsColumn(custom_models.ColumnItem):
    name = "Rows"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return core.Locale().toString(len(item.index))
            case constants.SORT_ROLE:
                return len(item.index)


class ColumnsColumn(custom_models.ColumnItem):
    name = "Columns"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return core.Locale().toString(len(item.columns))
            case constants.SORT_ROLE:
                return len(item.columns)


class IndexDescriptionColumn(custom_models.ColumnItem):
    name = "Index"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                if isinstance(item.index, pd.MultiIndex):
                    return f"MultiIndex ({len(item.index.levels)})"
                return str(item.index.name)


class DataFrameListModel(custom_models.ColumnTableModel):
    COLUMNS = [RowsColumn, ColumnsColumn, IndexDescriptionColumn]

    def __init__(self, dfs, parent=None):
        super().__init__(dfs, self.COLUMNS, parent=parent)


class DataFrameListWidget(widgets.TableView):
    def __init__(
        self,
        object_name: str = "pandas_df_manager",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        model = DataFrameListModel([])
        self.set_model(model)
        self.set_selection_behavior("rows")

    def add_df(self, df: pd.DataFrame):
        self.model().add(df)

    def _on_current_change(self, new, old):
        role = new.model().Roles.ColumnNameRole
        column_name = new.data(role)
        df = new.data(constants.USER_ROLE)
        model = pandasmodels.PandasCategoryListModel(df, column_name)
        self.category_table.set_model(model)


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("Fusion")
    i = 5
    tuples = [("bar", "one", "q"), ("bar", "two", "q")] * i
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    df = pd.DataFrame(np.random.randn(i * 2, i * 2), index=index, columns=index)
    df.attrs = {"test": "test"}
    widget = DataFrameListWidget()
    widget.add_df(df)
    widget.show()
    app.exec()
