from __future__ import annotations

from collections.abc import Callable
import functools
import logging
import operator

from typing import TYPE_CHECKING, Any, Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import datatypes, helpers


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

    def filter(self) -> custom_models.SliceFilterProxyModel:
        """Filter subsection to display."""
        from prettyqt import custom_models

        proxy = custom_models.SliceFilterProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def highlight_current(
        self, mode="column"
    ) -> custom_models.SliceHighlightCurrentProxyModel:
        """Filter subsection to display."""
        from prettyqt import custom_models

        proxy = custom_models.SliceHighlightCurrentProxyModel(
            indexer=self._indexer, parent=self._widget, mode=mode
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def modify(
        self,
        fn: Callable[[Any], Any],
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> custom_models.SliceValueTransformationProxyModel:
        """Conditionally apply modifications to given area."""
        from prettyqt import custom_models

        proxy = custom_models.SliceValueTransformationProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.add_transformer(fn, role, selector, selector_role)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def change_flags(
        self,
        selectable: bool | None = None,
        editable: bool | None = None,
        drag_enabled: bool | None = None,
        drop_enabled: bool | None = None,
        user_checkable: bool | None = None,
        enabled: bool | None = None,
        auto_tristate: bool | None = None,
        never_has_children: bool | None = None,
        user_tristate: bool | None = None,
    ) -> custom_models.SliceChangeFlagsProxyModel:
        """Change Item flags for given slice.

        For makin an area checkable, usually set_checkable should be preferred
        since it keeps track of checked items and triggers a callback on checkstate
        change.
        """
        from prettyqt import custom_models

        proxy = custom_models.SliceChangeFlagsProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        flags = dict(
            selectable=selectable,
            editable=editable,
            drag_enabled=drag_enabled,
            drop_enabled=drop_enabled,
            user_checkable=user_checkable,
            enabled=enabled,
            auto_tristate=auto_tristate,
            never_has_children=never_has_children,
            user_tristate=user_tristate,
        )
        flags_to_add = [constants.ITEM_FLAG[k] for k, v in flags.items() if v is True]
        flags_to_remove = [constants.ITEM_FLAG[k] for k, v in flags.items() if v is False]
        if flags_to_add:
            proxy.set_flags_to_add(functools.reduce(operator.ior, flags_to_add))
        if flags_to_remove:
            proxy.set_flags_to_remove(functools.reduce(operator.ior, flags_to_remove))
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def set_checkable(
        self,
        callback: Callable[[core.ModelIndex], Any] | None = None,
        tree: bool = False,
    ) -> (
        custom_models.SliceCheckableProxyModel
        | custom_models.SliceCheckableTreeProxyModel
    ):
        """Make given area checkable and trigger a callback on checkstate change.

        For trees, set tree=True. That way checkboxes change to tristate and
        propagate changes to parents and children.
        """
        from prettyqt import custom_models

        if tree:
            proxy = custom_models.SliceCheckableTreeProxyModel(
                indexer=self._indexer, parent=self._widget
            )
        else:
            proxy = custom_models.SliceCheckableProxyModel(
                indexer=self._indexer, parent=self._widget
            )
        if callback:
            proxy.checkstate_changed.connect(callback)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def change_icon_size(
        self, size: datatypes.SizeType
    ) -> custom_models.SliceChangeIconSizeProxyModel:
        from prettyqt import custom_models

        size = datatypes.to_size(size)
        proxy = custom_models.SliceChangeIconSizeProxyModel(
            indexer=self._indexer, size=size, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def style(
        self,
        foreground: datatypes.ColorType | gui.QBrush | None = None,
        background: datatypes.ColorType | gui.QBrush | None = None,
        font: str | gui.QFont | None = None,
        alignment: constants.AlignmentFlag | constants.AlignmentStr | None = None,
    ) -> custom_models.SliceAppearanceProxyModel:
        """Apply styling to given area."""
        from prettyqt import custom_models

        proxy = custom_models.SliceAppearanceProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        proxy.set_foreground(foreground)
        proxy.set_background(background)
        proxy.set_font(font)
        proxy.set_alignment(alignment)
        self._widget.set_model(proxy)
        return proxy

    def color_values(
        self,
        low_color: datatypes.ColorType = "green",
        high_color: datatypes.ColorType = "red",
    ) -> custom_models.SliceColorValuesProxyModel:
        """Make given area read-only."""
        from prettyqt import custom_models

        proxy = custom_models.SliceColorValuesProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.set_low_color(low_color)
        proxy.set_high_color(high_color)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy


class Proxyfier:
    def __init__(self, widget: widgets.QWidget):
        self._widget = widget
        self._wrapper = None

    def __getitem__(self, value: slice) -> ProxyWrapper:
        logger.debug(f"Building {value!r} ProxyModel for {self._widget!r}")
        self._wrapper = ProxyWrapper(indexer=value, widget=self._widget, proxifier=self)
        return self._wrapper

    def __getattr__(self, name: str):
        indexer = (slice(None, None, None), slice(None, None, None))
        self._wrapper = ProxyWrapper(indexer=indexer, widget=self._widget, proxifier=self)
        if hasattr(self._wrapper, name):
            return getattr(self._wrapper, name)
        else:
            raise AttributeError(name)

    def transpose(self) -> core.TransposeProxyModel:
        """Wraps model in a Proxy which transposes rows/columns."""
        proxy = core.TransposeProxyModel(parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def flatten(self) -> custom_models.FlattenedTreeProxyModel:
        """Wraps model in a Proxy which flattens tree structures."""
        # ss = """QTreeView::branch{border-image: url(none.png);}"""
        # self._widget.set_stylesheet(ss)
        from prettyqt import custom_models

        proxy = custom_models.FlattenedTreeProxyModel(parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def melt(
        self, id_columns: list[int], var_name: str = "Variable", value_name: str = "Value"
    ) -> custom_models.MeltProxyModel:
        """Wraps model in a Proxy which unpivots the table to a long format."""
        from prettyqt import custom_models

        proxy = custom_models.MeltProxyModel(
            id_columns=id_columns,
            var_name=var_name,
            value_name=value_name,
            parent=self._widget,
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def reorder_columns(self, order: list[int]) -> custom_models.ColumnOrderProxyModel:
        from prettyqt import custom_models

        proxy = custom_models.ColumnOrderProxyModel(order=order, parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def to_list(self) -> custom_models.TableToListProxyModel:
        """Wraps model in a Proxy which converts table to a tree."""
        from prettyqt import custom_models

        proxy = custom_models.TableToListProxyModel(parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def add_column(
        self,
        header: str,
        formatter: str,
        flags: constants.ItemFlag = constants.IS_ENABLED | constants.IS_SELECTABLE,
    ) -> custom_models.ColumnJoinerProxyModel:
        """Add a new column with given header to the table.

        Column content can be defined by a formatter.
        Example: "{2} - {4}" would result in
        <displayRole of column 2> - <displayRole of column4>
        """
        from prettyqt import custom_models

        proxy = custom_models.ColumnJoinerProxyModel(parent=self._widget)
        proxy.add_mapping(header=header, formatter=formatter, flags=flags)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def change_headers(
        self,
        headers: list[Any] | dict[int, Any],
        orientation: constants.Orientation
        | constants.OrientationStr = constants.HORIZONTAL,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> custom_models.ChangeHeadersProxyModel:
        proxy = custom_models.ChangeHeadersProxyModel(
            headers=headers, role=role, orientation=orientation, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def set_sort_filter_proxy(self, **kwargs) -> core.SortFilterProxyModel:
        proxy = core.SortFilterProxyModel(parent=self._widget, **kwargs)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def get_proxy(self, proxy: ProxyStr, **kwargs) -> core.QAbstractProxyModel:
        Klass = helpers.get_class_for_id(core.AbstractProxyModelMixin, proxy)
        proxy_instance = Klass(parent=self._widget, **kwargs)
        proxy_instance.setSourceModel(self._widget.model())
        self._widget.set_model(proxy_instance)
        return proxy_instance


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()

    table = debugging.example_table()
    table.proxifier[0].change_flags(selectable=False, enabled=False)
    table.show()
    with app.debug_mode():
        app.exec()
