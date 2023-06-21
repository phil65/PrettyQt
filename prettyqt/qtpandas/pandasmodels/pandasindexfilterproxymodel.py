from __future__ import annotations

import logging
from typing import Literal

import pandas as pd
import numpy as np
from prettyqt import constants, core

logger = logging.getLogger(__name__)


FilterModeStr = Literal["startswith", "containts", "match"]


class BasePandasIndexFilterModel(core.IdentityProxyModel):
    """Base Proxy to filter a pandas dataframe based on an calculated index.

    Mappings in both directions are calculated then with numpy methods.

    Very fast filter model compared to row-based SortFilterProxyModel approach.
    Doesnt need a copy of whole dataframe, only mapping indexes are built.
    """

    def __init__(self, **kwargs):
        self._filter_index = None
        self._source_to_proxy = None
        self._proxy_to_source = None
        super().__init__(**kwargs)

    def setSourceModel(self, model):
        self._filter_index = np.full(model.rowCount(), True, dtype=bool)
        self._source_to_proxy = np.cumsum(self._filter_index)
        self._proxy_to_source = np.where(self._filter_index == True)[0]  # noqa: E712
        super().setSourceModel(model)

    def _build_filter_index(self):
        return NotImplemented

    def set_search_term(self, search_term):
        self._search_term = search_term
        if self._search_term:
            self._build_filter_index()
        else:
            self._filter_index = np.full(len(df), True, dtype=bool)
        with self.reset_model():
            self._source_to_proxy = np.cumsum(self._filter_index) - 1
            self._proxy_to_source = np.where(self._filter_index == True)[0]  # noqa: E712
            self.update_all()

    def rowCount(self, index=None):
        return self._filter_index.sum()

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        """Map header data to proxy by calculating position based on filter array."""
        if orientation == constants.HORIZONTAL:
            return super().headerData(section, orientation, role)
        return super().headerData(self._proxy_to_source[section], orientation, role)

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.Modelindex:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if row < 0 or column < 0 or source is None or row >= self.rowCount():
            return core.ModelIndex()
        source_parent = self.mapToSource(parent)
        row_pos = int(self._proxy_to_source[row])
        source_index = source.index(row_pos, column, source_parent)
        return self.mapFromSource(source_index)

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.Modelindex:
        """Map index to source by calculating position from our index array."""
        source = self.sourceModel()
        if (
            source is None
            or not proxy_idx.isValid()
            or proxy_idx.row() >= self.rowCount()
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


class PandasStringColumnFilterModel(BasePandasIndexFilterModel):
    """Basically filters a dataframe based on df.iloc[:, column].str.somemethod(term)."""

    ID = "pandas_str_filter"

    def __init__(self, **kwargs):
        self._filter_column = 0
        self._filter_mode = "startswith"
        self._case_sensitive = True
        self._flags = 0
        self._na_value = False
        super().__init__(**kwargs)

    def _build_filter_index(self):
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

    filter_column = core.Property(int, get_filter_column, set_filter_column)
    filter_mode = core.Property(str, get_filter_mode, set_filter_mode)
    case_sensitive = core.Property(bool, is_case_sensitive, set_case_sensitive)
    re_flags = core.Property(int, get_flags, set_flags)
    na_value = core.Property(bool, get_na_value, set_na_value)


class PandasEvalFilterModel(BasePandasIndexFilterModel):
    ID = "pandas_eval_filter"

    def _build_filter_index(self):
        df = self.sourceModel().df
        try:
            self._filter_index = df.eval(self._search_term)
            self._filter_index = self._filter_index.to_numpy()
            if self._filter_index.dtype != bool:
                self._filter_index = np.full(len(df), False, dtype=bool)
        except Exception:
            self._filter_index = np.full(len(df), False, dtype=bool)


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.qtpandas import pandasmodels

    app = widgets.app()
    a = pd.Series(["a", "bc", "c", "d", "aa"] * 10000, dtype=pd.StringDtype())
    b = pd.Series(["a", "b", "c", "fjkdsj", "fdf"] * 10000, dtype=pd.StringDtype())
    df = pd.DataFrame(dict(a=a, b=b))
    model = pandasmodels.DataTableWithHeaderModel(df)
    table = widgets.TableView()
    lineedit = widgets.LineEdit()
    container = widgets.Widget()
    layout = container.set_layout("vertical")
    layout.add(lineedit)
    layout.add(table)
    proxy = PandasStringColumnFilterModel(parent=table)
    proxy.filter_mode = "startswith"
    lineedit.value_changed.connect(proxy.set_search_term)
    proxy.setSourceModel(model)
    table.set_model(proxy)
    container.show()
    with app.debug_mode():
        app.main_loop()
