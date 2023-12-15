from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from prettyqt import core


logger = logging.getLogger(__name__)


class PredicateFilterProxyModel(core.SortFilterProxyModel):
    """A simple filter proxy model with settable filter predicates.

    ### Example:
    ```py
    proxy = PredicateFilterProxyModel()
    proxy.add_filter(lambda value: value < 1)
    ```
    """

    ID = "predicate_filter"

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._filters: list[Callable[[Any], bool]] = []

    def clear_filters(self):
        self._filters = []
        self.invalidateFilter()

    def add_filter(self, predicate: Callable[[Any], bool]):
        self._filters.append(predicate)
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        source = self.sourceModel()
        col = self.filterKeyColumn()
        role = self.filterRole()
        index = source.index(row, col, parent)
        data = source.data(index, role)

        def apply(f: Callable):
            try:
                return f(data)
            except (TypeError, ValueError):
                return False

        return all(apply(f) for f in self._filters)


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.itemmodels import JsonModel

    app = widgets.app()
    dist = [
        dict(
            assss=2,
            bffff={
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

    _source_model = JsonModel(dist)
    model = PredicateFilterProxyModel()
    model.setFilterKeyColumn(1)
    model.setSourceModel(_source_model)
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
