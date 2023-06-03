from __future__ import annotations

import logging

from prettyqt import constants, core

logger = logging.getLogger(__name__)


class DataFrameEvalFilterProxyModel(core.SortFilterProxyModel):
    """A simple filter proxy model for pandas models.

    Example:
        >>> proxy = DataFrameEvalFilterProxyModel()
        >>> proxy.set_filter("A < B")
    """

    ID = "pandas_eval_filter"

    def __init__(self, **kwargs):
        self.filter_series = None
        self._filter_expr = ""
        super().__init__(**kwargs)

    def setSourceModel(self, model):
        """Connect/disconnect signals to invalidate this model on source model change."""
        if (curr_model := self.sourceModel()) is not None:
            curr_model.dataChanged.disconnect(self._on_reset)
            curr_model.rowsInserted.disconnect(self._on_reset)
            curr_model.rowsRemoved.disconnect(self._on_reset)
            curr_model.rowsMoved.disconnect(self._on_reset)

        with self.reset_model():
            super().setSourceModel(model)

        model.dataChanged.connect(self._on_reset)
        model.rowsInserted.connect(self._on_reset)
        model.rowsRemoved.connect(self._on_reset)
        model.rowsMoved.connect(self._on_reset)

    def _on_reset(self):
        """Here we build the filter index. On exception we set to False."""
        try:
            self.filter_series = self.sourceModel().df.eval(self._filter_expr)
        except Exception:
            self.filter_series = False
        self.invalidate()

    def set_filter(self, search_term: str):
        self._filter_expr = search_term
        self._on_reset()

    def get_filter(self) -> str:
        return self._filter_expr

    def filterAcceptsRow(self, source_row: int, parent: core.ModelIndex) -> bool:
        if not self._filter_expr:
            return True
        if self.filter_series is False:
            # invalid filter expression, show nothing.
            return False
        return self.filter_series[source_row] if self.filter_series is not None else True

    filter_expression = core.Property(str, get_filter, set_filter, user=True)


class DataFrameSearchFilterProxyModel(DataFrameEvalFilterProxyModel):
    """This one only works for str columns.

    Not as flexible, (always-case-sensitive, -1 for filterKeyColumn not working.)
    but probably faster than SortFilterProxyModel. Needs benchmarking.
    Fastest would be to circumvent the row-based filter approach,
    but doing it this way saves memory as we dont need a copy of the whole dataframe.
    """

    ID = "pandas_search_filter"

    def _on_reset(self):
        try:
            ncol = self.filterKeyColumn()
            colname = self.sourceModel().headerData(ncol, constants.HORIZONTAL)
            # it would also be possible to use str accessor for this expression,
            # but that requires engine=python (and perhaps str dtype).
            expr = f"'{self._filter_expr}' <= `{colname}` <= '{self._filter_expr}~'"
            self.filter_series = self.sourceModel().df.eval(expr)
        except Exception:
            self.filter_series = False
        self.invalidate()


if __name__ == "__main__":
    import pandas as pd

    from prettyqt import widgets
    from prettyqt.qtpandas import pandasmodels

    app = widgets.app()

    df = pd.DataFrame(dict(a=[40, 224, 1], b=["1abc", "2", "3"], c=[1, 2, 3]))

    table = widgets.TableView()
    table.set_delegate("variant")
    model = pandasmodels.DataTableWithHeaderModel(df, parent=table)
    proxy = DataFrameSearchFilterProxyModel(parent=table)
    proxy.setFilterKeyColumn(1)
    proxy.setSourceModel(model)
    table.set_model(proxy)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    lineedit = widgets.LineEdit()
    lineedit.value_changed.connect(proxy.set_filter)
    widget.box.add(table)
    widget.box.add(lineedit)
    widget.show()
    with app.debug_mode():
        app.main_loop()
