from __future__ import annotations

import numpy as np
import pandas as pd

from prettyqt import constants, widgets
from prettyqt.qtpandas import pandaswidgets


class DataFrameManagerWidget(widgets.Splitter):
    def __init__(self, object_name: str = "pandas_df_manager", **kwargs):
        super().__init__(object_name=object_name, **kwargs)
        self.dataframe_list = pandaswidgets.DataFrameListWidget()
        self.dataframe_editor = pandaswidgets.DataFrameWidget()
        self.dataframe_list.selectionModel().currentRowChanged.connect(
            self._on_current_change
        )
        self.add(self.dataframe_list)
        widget = widgets.Widget()
        widget.set_layout("horizontal")
        widget.box.add(self.dataframe_editor)
        self.add(widget)

    def add_df(self, df: pd.DataFrame):
        self.dataframe_list.add_df(df)

    def _on_current_change(self, new, old):
        df = new.data(constants.USER_ROLE)
        self.dataframe_editor.set_df(df)


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
    df2 = pd.DataFrame(np.random.randn(8, 8), index=index, columns=index)
    df.attrs = {"test": "test"}
    with app.debug_mode():
        widget = DataFrameManagerWidget()
        widget.add_df(df)
        widget.add_df(df2)
        widget.show()
        app.exec()
