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
    def __init__(self, indexer, widget: core.QAbstractItemModel, proxifier: Proxyfier):
        if widget.model() is None:
            raise RuntimeError("Need a model in order to proxify.")
        # PySide6 shows empty tables when no parent is set.
        if widget.model().parent() is None:
            raise RuntimeError("Setting proxy without parent.")
        self._indexer = indexer
        self.proxifier = proxifier
        self._widget = widget

    def filter(self) -> custom_models.SubsetFilterProxyModel:
        from prettyqt import custom_models

        match self._indexer:
            case (arg_1, arg_2):
                kwargs = dict(row_filter=arg_1, column_filter=arg_2, parent=self._widget)
            case _:
                kwargs = dict(
                    row_filter=self._indexer, column_filter=None, parent=self._widget
                )
        proxy = custom_models.SubsetFilterProxyModel(**kwargs)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def modify(
        self,
        fn: Callable[[Any], Any],
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> custom_models.ValueTransformationProxyModel:
        from prettyqt import custom_models

        proxy = custom_models.ValueTransformationProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.add_transformer(fn, role, selector, selector_role)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def set_read_only(self) -> custom_models.ReadOnlyProxyModel:
        from prettyqt import custom_models

        proxy = custom_models.ReadOnlyProxyModel(index=self._indexer, parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def set_checkable(self) -> custom_models.CheckableProxyModel:
        from prettyqt import custom_models

        proxy = custom_models.CheckableProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
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
        proxy = custom_models.AppearanceProxyModel(parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        # TODO: set_data is probably not the most efficient way to do this.
        proxy.set_data(self._indexer, value, role)
        self._widget.set_model(proxy)
        return proxy


class Proxyfier:
    def __init__(self, widget):
        self._widget = widget
        self._wrapper = None

    def __getitem__(self, value: slice) -> ProxyWrapper:
        logger.debug(f"Building {value!r} ProxyModel for {self._widget!r}")
        self._wrapper = ProxyWrapper(indexer=value, widget=self._widget, proxifier=self)
        return self._wrapper

    def transpose(self) -> core.TransposeProxyModel:
        return self.get_proxy("transpose")

    def flatten(self) -> custom_models.FlattenedTreeProxyModel:
        return self.get_proxy("flatten_tree")

    def get_proxy(self, proxy: ProxyStr, **kwargs):
        Klass = helpers.get_class_for_id(core.AbstractProxyModelMixin, proxy)
        proxy_instance = Klass(parent=self._widget, **kwargs)
        proxy_instance.setSourceModel(self._widget.model())
        self._widget.set_model(proxy_instance)
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
