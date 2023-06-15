from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any, Literal, TYPE_CHECKING

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import colors, helpers

if TYPE_CHECKING:
    from prettyqt import custom_models


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


class ProxyWrapper:
    def __init__(self, index, model: core.QAbstractItemModel, proxifier: Proxyfier):
        self._index = index
        self.proxifier = proxifier
        self._model = model

    def filter(self):
        from prettyqt import custom_models

        parent = self._model.parent()
        match self._index:
            case (arg_1, arg_2):
                kwargs = dict(row_filter=arg_1, column_filter=arg_2, parent=parent)
            case _:
                kwargs = dict(row_filter=self._index, column_filter=None, parent=parent)
        proxy = custom_models.SubsetFilterProxyModel(**kwargs)
        proxy.setSourceModel(self._model)
        return proxy

    def style(self, value="red", role=constants.BACKGROUND_ROLE, **kwargs):
        from prettyqt import custom_models

        match role:
            case constants.BACKGROUND_ROLE | constants.FOREGROUND_ROLE:
                value = colors.get_color(value).as_qt()
            case constants.FONT_ROLE:
                kwargs = {helpers.to_lower_camel(k): v for k, v in kwargs.items()}
                value = gui.QFont(value, **kwargs)
            case constants.ALIGNMENT_ROLE:
                pass
        parent = self._model.parent()
        proxy = custom_models.AppearanceProxyModel(parent=parent)
        proxy.setSourceModel(self._model)
        proxy.set_data(self._index, value, role)
        return proxy


class Proxyfier:
    def __init__(self, model):
        self._model = model
        self._wrapper = None

    def __getitem__(self, value: slice) -> ProxyWrapper:
        if self._model.parent() is None:
            raise ValueError("needs parent!")
        logger.debug(f"Building {value!r} ProxyModel for {self._model!r}")
        self._wrapper = ProxyWrapper(value, self._model, self)
        return self._wrapper

    def transpose(
        self, parent: widgets.QWidget | None = None
    ) -> core.TransposeProxyModel:
        return self.get_proxy("transpose", parent)

    def flatten(
        self, parent: widgets.QWidget | None = None
    ) -> custom_models.FlattenedTreeProxyModel:
        return self.get_proxy("flatten_tree", parent)

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
        # PySide6 needs widget parent here
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
