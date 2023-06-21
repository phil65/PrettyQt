from __future__ import annotations

import numpy as np
import pandas as pd

from prettyqt import constants, core, widgets
from prettyqt.qtpandas import pandaswidgets, pandasmodels


class DataFrameWidget(widgets.MainWindow):
    current_index_changed = core.Signal(core.ModelIndex)
    current_row_changed = core.Signal(int)

    def __init__(
        self,
        df: pd.DataFrame | None = None,
        object_name: str = "pandas_window",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)

        self.index_table = widgets.TableView(selection_behavior="rows")
        self.column_table = widgets.TableView(selection_behavior="rows")
        model = pandasmodels.PandasIndexListModel(df)
        self.index_table.set_model(model)
        model = pandasmodels.PandasColumnListModel(df)
        self.column_table.set_model(model)
        self.column_table.selectionModel().currentChanged.connect(self._on_current_change)

        self.data_table = pandaswidgets.DataFrameViewer(df)
        self.set_central_widget(self.data_table)

        self.category_table = widgets.TableView(selection_behavior="rows")

        self.attrs_table = widgets.TreeView(
            selection_behavior="rows", root_is_decorated=False
        )
        if df is not None:
            self.attrs_table.set_model(df.attrs)
            self.attrs_table.show_root(False)

        self.add_dockwidget(self.index_table, window_title="Index list")
        self.add_dockwidget(self.column_table, window_title="Column list")
        self.add_dockwidget(self.category_table, window_title="Category list")
        self.add_dockwidget(self.attrs_table, window_title="MetaData")

    def set_df(self, df: pd.DataFrame):
        if df is not None:
            self.attrs_table.set_model(df.attrs)
            self.attrs_table.show_root(False)
        self.data_table.set_df(df)
        model = pandasmodels.PandasIndexListModel(df)
        self.index_table.set_model(model)
        model = pandasmodels.PandasColumnListModel(df)
        self.column_table.set_model(model)
        self.category_table.set_model(None)

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
    widget = DataFrameWidget(df)
    widget.show()
    app.exec()
