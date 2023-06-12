from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any, Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import helpers

logger = logging.getLogger(__name__)


ProxyStr = Literal[
    "fuzzy",
    "transpose",
    "sort_filter",
    "identity",
    "value_transformation",
    "range_filter",
    "checkable",
    "subset",
    "flatten_tree",
    "table_to_list",
    "predicate_filter",
    "size_limiter",
    "subsequence",
    "appearance",
    "column_join",
    "read_only",
    "highlight_current",
]


class Proxyfier:
    def __init__(self, model):
        self._model = model

    def __getitem__(self, index):
        parent = self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")

        from prettyqt import custom_models

        match index:
            case (arg_1, arg_2):
                kwargs = dict(row_filter=arg_1, column_filter=arg_2, parent=parent)
            case _:
                kwargs = dict(row_filter=index, column_filter=None, parent=parent)
        proxy = proxy = custom_models.SubsetFilterProxyModel(**kwargs)
        proxy.setSourceModel(self._model)
        return proxy

    def transpose(
        self, parent: widgets.QWidget | None = None
    ) -> core.TransposeProxyModel:
        # PySide6 needs widget parent here
        parent = parent or self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")
        proxy = core.TransposeProxyModel(parent=parent)
        proxy.setSourceModel(self._model)
        return proxy

    def modify(
        self,
        fn: Callable[[Any], Any],
        column: int | None = None,
        row: int | None = None,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        parent: widgets.QWidget | None = None,
    ):
        parent = parent or self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")

        from prettyqt import custom_models

        proxy = custom_models.ValueTransformationProxyModel(parent=parent)
        proxy.add_transformer(fn, column, row, role, selector, selector_role)
        proxy.setSourceModel(self._model)
        return proxy

    def get_proxy(self, proxy: ProxyStr, parent: widgets.QWidget | None = None, **kwargs):
        parent = parent or self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")
        Klass = helpers.get_class_for_id(core.AbstractProxyModelMixin, proxy)
        proxy_instance = Klass(parent=parent, **kwargs)
        proxy_instance.setSourceModel(self._model)
        return proxy_instance


if __name__ == "__main__":
    app = widgets.app()

    test = widgets.PlainTextEdit()
    for i in range(200):
        test.append_text(str(i))
    test.show()
    with app.debug_mode():
        app.sleep(2)
        print(test.selecter[20:50])
        app.main_loop()
