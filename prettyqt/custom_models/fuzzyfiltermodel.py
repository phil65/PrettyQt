from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import fuzzy


class FuzzyFilterModel(core.SortFilterProxyModel):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._search_term = ""

    def filterAcceptsRow(self, source_row: int, source_index: core.ModelIndex):
        column = self.filterKeyColumn()
        idx = self.sourceModel().index(source_row, column, source_index)
        text = self.sourceModel().data(idx)
        if self._search_term == "":
            return True
        return fuzzy.fuzzy_match_simple(
            self._search_term, text, case_sensitive=self.is_filter_case_sensitive()
        )

    def set_search_term(self, search_term: str):
        self._search_term = search_term
        self.invalidate()
        self.sort(0, constants.DESCENDING)


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    app = widgets.app()
    dist = [
        dict(
            a=2,
            b={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "xxx",
            },
        ),
        6,
        "jkjk",
    ]
    source_model = JsonModel(dist)
    model = FuzzyFilterModel()
    model.setFilterKeyColumn(1)
    # model.set_search_term("tj")
    model.setSourceModel(source_model)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    lineedit = widgets.LineEdit()
    lineedit.value_changed.connect(model.set_search_term)
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    widget.box.add(lineedit)
    widget.box.add(table)
    widget.show()
    app.main_loop()
