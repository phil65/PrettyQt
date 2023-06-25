from __future__ import annotations

import logging
from typing import Literal

import pandas as pd
import numpy as np
from prettyqt import constants, core

logger = logging.getLogger(__name__)


FilterModeStr = Literal["startswith", "containts", "match"]


class BasePandasIndexFilterProxyModel(core.IdentityProxyModel):
    """Base Proxy to filter a pandas dataframe based on an calculated index.

    Mappings in both directions are calculated then with numpy methods.

    Very fast filter model compared to row-based SortFilterProxyModel approach.
    Doesnt need a copy of whole dataframe, only mapping indexes are built.

    There are lot of use cases though where the better option probably is to not
    use any proxy model at all, but just work on a copy of the dataframe.

    Note: Dataframe proxies cant be chained right now.
    """

    def __init__(self, **kwargs):
        self._filter_index = None
        self._source_to_proxy = None
        self._proxy_to_source = None
        self._row_count = 0
        super().__init__(**kwargs)

    def setSourceModel(self, model):
        super().setSourceModel(model)
        self._reset_filter_index(True)
        self._update_mapping()

    def _update_mapping(self):
        with self.reset_model():
            self._row_count = self._filter_index.sum()
            self._source_to_proxy = np.cumsum(self._filter_index) - 1
            self._proxy_to_source = np.where(self._filter_index == True)[0]  # noqa: E712

    def _reset_filter_index(self, init_value: bool):
        rowcount = self.sourceModel().rowCount()
        self._filter_index = np.full(rowcount, init_value, dtype=bool)

    def rowCount(self, index: core.ModelIndex | None = None):
        return self._row_count

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        """Map header data to proxy by using proxy-to-source-map."""
        if orientation == constants.HORIZONTAL:
            return super().headerData(section, orientation, role)
        return super().headerData(self._proxy_to_source[section], orientation, role)

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if row < 0 or column < 0 or source is None or row >= self._row_count:
            return core.ModelIndex()
        source_parent = self.mapToSource(parent)
        row_pos = int(self._proxy_to_source[row])
        source_index = source.index(row_pos, column, source_parent)
        return self.mapFromSource(source_index)

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.ModelIndex:
        """Map index to source by using proxy-to-source map."""
        source = self.sourceModel()
        if (
            source is None
            or not proxy_idx.isValid()
            or proxy_idx.row() >= self._row_count
        ):
            return core.ModelIndex()
        row_pos = int(self._proxy_to_source[proxy_idx.row()])
        return source.index(row_pos, proxy_idx.column())

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if self.sourceModel() is None or not source_index.isValid():
            return core.ModelIndex()
        row_pos = int(self._source_to_proxy[source_index.row()])
        return self.createIndex(
            row_pos, source_index.column(), source_index.internalPointer()
        )


class PandasStringColumnFilterProxyModel(BasePandasIndexFilterProxyModel):
    """Basically filters a dataframe based on df.iloc[:, column].str.somemethod(term)."""

    ID = "pandas_str_filter"

    def __init__(self, **kwargs):
        self._filter_column = 0
        self._filter_mode = "startswith"
        self._case_sensitive = True
        self._flags = 0
        self._search_term = ""
        self._na_value = False
        super().__init__(**kwargs)

    def set_search_term(self, search_term: str):
        self._search_term = search_term
        if not self._search_term:
            self._reset_filter_index(init_value=True)
            self._update_mapping()
            return
        df = self.get_source_model(skip_proxies=True).df
        match self.filter_mode:
            case "startswith":
                self._filter_index = df.iloc[:, self._filter_column].str.startswith(
                    self._search_term, na=self._na_value
                )
            case "contains":
                self._filter_index = df.iloc[:, self._filter_column].str.contains(
                    self._search_term,
                    case=self._case_sensitive,
                    flags=self._flags,
                    na=self._na_value,
                )
            case "match":
                self._filter_index = df.iloc[:, self._filter_column].str.match(
                    self._search_term,
                    case=self._case_sensitive,
                    flags=self._flags,
                    na=self._na_value,
                )
        self._filter_index = self._filter_index.to_numpy()
        # this is needed for new StringDtype, otherwise much slower.
        if self._filter_index.dtype == object:
            self._filter_index = self._filter_index.astype(bool)
        self._update_mapping()

    def get_search_term(self) -> str:
        return self._search_term

    def set_filter_column(self, column: int):
        self._filter_column = column

    def get_filter_column(self) -> int:
        return self._filter_column

    def set_filter_mode(self, mode: FilterModeStr):
        self._filter_mode = mode

    def get_filter_mode(self) -> FilterModeStr:
        return self._filter_mode

    def set_case_sensitive(self, mode: bool):
        self._case_sensitive = mode

    def is_case_sensitive(self) -> bool:
        return self._case_sensitive

    def set_flags(self, flags: int):
        self._flags = flags

    def get_flags(self) -> int:
        return self._flags

    def set_na_value(self, value: bool):
        self._na_value = value

    def get_na_value(self) -> bool:
        return self._na_value

    search_term = core.Property(str, get_search_term, set_search_term)
    filter_column = core.Property(int, get_filter_column, set_filter_column)
    filter_mode = core.Property(str, get_filter_mode, set_filter_mode)
    case_sensitive = core.Property(bool, is_case_sensitive, set_case_sensitive)
    re_flags = core.Property(int, get_flags, set_flags)
    na_value = core.Property(bool, get_na_value, set_na_value)


class PandasEvalFilterProxyModel(BasePandasIndexFilterProxyModel):
    ID = "pandas_eval_filter"

    def __init__(self, **kwargs):
        self._expression = ""
        super().__init__(**kwargs)

    def set_expression(self, expression: str):
        self._expression = expression
        if not self._expression:
            self._reset_filter_index(True)
            self._update_mapping()
        try:
            self._filter_index = df.eval(self._expression)
            self._filter_index = self._filter_index.to_numpy()
            # df.eval doesnt neccessarily return a bool index. If not, show nothing.
            if self._filter_index.dtype != bool:
                self._reset_filter_index(False)
        except Exception:
            self._reset_filter_index(False)
        self._update_mapping()

    def get_expression(self) -> str:
        return self._expression

    expression = core.Property(str, get_expression, set_expression)


class PandasMultiStringColumnFilterModel(BasePandasIndexFilterProxyModel):
    def __init__(self, **kwargs):
        self._filters: dict[str, str] = {}
        super().__init__(**kwargs)

    def set_filters(self, filters: dict[str, str]):
        self._filters = filters
        df = self.get_source_model(skip_proxies=True).df
        # workaround-ish way to implement "startswith" as an expression
        filters = [f"('{v}' <= `{k}` <= '{v}~')" for k, v in self._filters.items()]
        expr = " & ".join(filters)
        try:
            self._filter_index = df.eval(expr)
            self._filter_index = self._filter_index.to_numpy()
            if self._filter_index.dtype != bool:
                self._filter_index = self._filter_index.astype(bool)
        except Exception:
            self._reset_filter_index(False)
        self._update_mapping()

    def get_filters(self) -> dict[str, str]:
        return self._filters

    filters = core.Property(dict, get_filters, set_filters)


if __name__ == "__main__":
    from prettyqt import debugging, widgets
    from prettyqt.qtpandas import pandasmodels

    app = widgets.app()
    a = pd.Series(["a", "bc", "c", "d", "aa"] * 100000, dtype=pd.StringDtype())
    b = pd.Series(["a", "b", "c", "fjkdsj", "fdf"] * 100000, dtype=pd.StringDtype())
    df = pd.DataFrame(dict(a=a, b=b))
    model = pandasmodels.DataTableWithHeaderModel(df)
    proxy = PandasStringColumnFilterProxyModel(parent=model)
    proxy.setSourceModel(model)
    w = debugging.proxy_comparer(proxy)
    w.show()
    with app.debug_mode():
        app.exec()

