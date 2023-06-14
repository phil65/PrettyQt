from __future__ import annotations

import numpy as np
import pandas as pd

from prettyqt import constants, custom_models, widgets
from prettyqt.qtpandas import pandasmodels


def index_description(index: pd.Index) -> str:
    if isinstance(index, pd.MultiIndex):
        return f"MultiIndex ({len(index.levels)})"
    return str(index.name)


def format_num(num: int) -> str:
    return format(num, ",")


# class RowsColumn(custom_models.ColumnItem):
#     name = "Rows"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return format_num(len(item.index))
#             case constants.SORT_ROLE:
#                 return len(item.index)


# class ColumnsColumn(custom_models.ColumnItem):
#     name = "Columns"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return format_num(len(item.columns))
#             case constants.SORT_ROLE:
#                 return len(item.columns)


# class IndexDescriptionColumn(custom_models.ColumnItem):
#     name = "Index"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return index_description(item.index)


COL_ROWS = custom_models.ColumnItem(
    name="Rows",
    doc="Rows",
    label=lambda item: format_num(len(item.index)),
    sort_value=lambda item: len(item.index),
)

COL_COLUMNS = custom_models.ColumnItem(
    name="Columns",
    doc="Columns",
    label=lambda item: format_num(len(item.columns)),
    sort_value=lambda item: len(item.columns),
)

COL_INDEX = custom_models.ColumnItem(
    name="Index",
    doc="Index",
    label=lambda item: index_description(item.index),
)

COLUMNS = [COL_ROWS, COL_COLUMNS, COL_INDEX]


class DataFrameListWidget(widgets.TableView):
    def __init__(
        self,
        object_name: str = "pandas_df_manager",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        model = custom_models.ColumnTableModel([], COLUMNS)
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
    tuples = [
        ("bar", "one", "q"),
        ("bar", "two", "q"),
        ("baz", "one", "q"),
        ("baz", "two", "q"),
        ("foo", "one", "q"),
        ("foo", "two", "q"),
        ("qux", "one", "q"),
        ("qux", "two", "q"),
    ]
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    df = pd.DataFrame(np.random.randn(8, 8), index=index, columns=index)
    df.attrs = {"test": "test"}
    widget = DataFrameListWidget()
    widget.show()
    app.main_loop()
