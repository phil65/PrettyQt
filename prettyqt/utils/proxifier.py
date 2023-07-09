from __future__ import annotations

from collections.abc import Callable
import functools
import logging
import operator

from typing import TYPE_CHECKING, Any, Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import classhelpers, datatypes


if TYPE_CHECKING:
    from prettyqt import itemmodels


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


class Sliced:
    def __init__(self, indexer, widget: widgets.QAbstractItemView, proxifier: Proxifier):
        if widget.model() is None:
            raise RuntimeError("Need a model in order to proxify.")
        # PySide6 shows empty tables when no parent is set.
        if widget.model().parent() is None:
            widget.model().setParent(widget)
        self._indexer = indexer
        self.proxifier = proxifier
        self._widget = widget

    def filter(self) -> itemmodels.SliceFilterProxyModel:
        """Filter subsection to display.

        Wraps current model with a SliceFilterProxyModel.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceFilterProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def highlight_current(
        self, mode="column"
    ) -> itemmodels.SliceHighlightCurrentProxyModel:
        """Filter subsection to display.

        Wraps current model with a SliceHighlightCurrentProxyModel.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceHighlightCurrentProxyModel(
            indexer=self._indexer, parent=self._widget, mode=mode
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        self._widget.selectionModel().currentChanged.connect(proxy.highlight_index)
        return proxy

    def modify(
        self,
        fn: Callable[[Any], Any],
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> itemmodels.SliceValueTransformationProxyModel:
        """Conditionally apply modifications to given area.

        Wraps current model with a SliceValueTransformationProxyModel.

        Arguments:
            fn: Callable to use for modifying.
            role: role to modify
            selector: Callable to filter cells which should be modified.
            selector_role: data role the selector callable should get as an argument.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceValueTransformationProxyModel(
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
    ) -> itemmodels.SliceChangeFlagsProxyModel:
        """Change Item flags for given slice.

        For makin an area checkable, usually set_checkable should be preferred
        since it keeps track of checked items and triggers a callback on checkstate
        change.

        Arguments:
            selectable: Changes the ItemIsSelectable Flag
            editable: Changes the ItemIsEnabled Flag
            drag_enabled: Changes the ItemIsDragEnabed Flag
            drop_enabled: Changes the ItemIsDropEnabled Flag
            user_checkable: Changes the ItemIsUserCheckable Flag
            enabled: Changes the ItemIsEnabled Flag
            auto_tristate: Changes the ItemIsAutoTristate Flag
            never_has_children: Changes the ItemNeverHasChildren Flag
            user_tristate: Changes the ItemIsUserTristate Flag
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceChangeFlagsProxyModel(
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

    def set_format(
        self,
        int_format: str | None = None,
        float_format: str | None = None,
        datetime_format: str | None = None,
        date_format: str | None = None,
        time_format: str | None = None,
    ) -> itemmodels.SliceDisplayTextProxyModel:
        """Format non-str values returned by DisplayRole.

        Wraps current model with a SliceDisplayTextProxyModel.

        Arguments:
            int_format: Format to use for int values
            float_format: Format to use for float values
            datetime_format: Format to use for QDateTime / datetime.datetime objects.
            date_format: Format to use for QDate / datetime.date objects
            time_format: Format to use for QTime / datetime.time objects.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceDisplayTextProxyModel(
            int_format=int_format or "{:.4f}",
            float_format=float_format or "{:.4f}",
            datetime_format=datetime_format or "%m/%d/%Y, %H:%M:%S",
            date_format=date_format or "%m/%d/%Y",
            time_format=time_format or "%H:%M:%S",
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def set_checkable(
        self,
        callback: Callable[[core.ModelIndex], Any] | None = None,
        tree: bool = False,
    ) -> itemmodels.SliceCheckableProxyModel | itemmodels.SliceCheckableTreeProxyModel:
        """Make given area checkable and trigger a callback on checkstate change.

        For trees, set tree=True. That way checkboxes change to tristate and
        propagate changes to parents and children.

        Arguments:
            callback: Callback to trigger when checkstate changes.
            tree: Whether the underlying model is a tree.
        """
        from prettyqt import itemmodels

        if tree:
            proxy = itemmodels.SliceCheckableTreeProxyModel(
                indexer=self._indexer, parent=self._widget
            )
        else:
            proxy = itemmodels.SliceCheckableProxyModel(
                indexer=self._indexer, parent=self._widget
            )
        if callback:
            proxy.checkstate_changed.connect(callback)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def change_icon_size(
        self, size: datatypes.SizeType
    ) -> itemmodels.SliceChangeIconSizeProxyModel:
        """Change the size of pixmap / icon provided by decoration role.

        Wraps current model with a  SliceChangeIconSizeProxyModel.

        Arguments:
            size: New size for decoration role.
        """
        from prettyqt import itemmodels

        size = datatypes.to_size(size)
        proxy = itemmodels.SliceChangeIconSizeProxyModel(
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
    ) -> itemmodels.SliceAppearanceProxyModel:
        """Apply styling to given area.

        Wraps current model with a SliceAppearanceProxyModel.

            foreground: Color / Brush to use for foreground role.
            background: Color / Brush to use for background role.
            font: Font to use for font role.
            alignment: Alignment to use for alignment role.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceAppearanceProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.setSourceModel(self._widget.model())
        proxy.set_foreground(foreground)
        proxy.set_background(background)
        proxy.set_font(font)
        proxy.set_alignment(alignment)
        self._widget.set_model(proxy)
        return proxy

    def map_role(
        self,
        from_: constants.ItemDataRole,
        to: constants.ItemDataRole,
        converter: Callable | None = None,
    ) -> itemmodels.MapRoleProxyMpodel:
        """Map ItemDataRole to another role for data().

        Wraps model with a MapRoleProxyMpodel.

        Arguments:
            from_: role to map from
            to: role to map to
            converter: modify mapped values with callable
        """
        from prettyqt import itemmodels

        proxy = itemmodels.MapRoleProxyMpodel(
            indexer=self._indexer,
            parent=self._widget,
            mapping={from_: to},
            converter=converter,
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def color_values(
        self,
        low_color: datatypes.ColorType = "green",
        high_color: datatypes.ColorType = "red",
    ) -> itemmodels.SliceColorValuesProxyModel:
        """Color numerical values.

        Wraps model with a SliceColorValuesProxyModel.

        Arguments:
            low_color: color to use for "low" values
            high_color: color to use for "high" values
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceColorValuesProxyModel(
            indexer=self._indexer, parent=self._widget
        )
        proxy.set_low_color(low_color)
        proxy.set_high_color(high_color)
        self._widget.set_model(proxy)
        return proxy

    def color_categories(
        self,
    ) -> itemmodels.SliceColorCategoriesProxyModel:
        """Color numerical values.

        Wraps model with a SliceColorCategoriesProxyModel.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.SliceColorCategoriesProxyModel(
            indexer=self._indexer, parent=self._widget, source_model=self._widget.model()
        )
        self._widget.set_model(proxy)
        return proxy


class Proxifier:
    def __init__(self, widget: widgets.QAbstractItemView):
        self._widget = widget
        self._wrapper = None

    def __getitem__(self, value: slice) -> Sliced:
        """Return a Sliced Object."""
        logger.debug(f"Building {value!r} ProxyModel for {self._widget!r}")
        self._wrapper = Sliced(indexer=value, widget=self._widget, proxifier=self)
        return self._wrapper

    def __getattr__(self, name: str):
        indexer = (slice(None, None, None), slice(None, None, None))
        self._wrapper = Sliced(indexer=indexer, widget=self._widget, proxifier=self)
        if hasattr(self._wrapper, name):
            return getattr(self._wrapper, name)
        else:
            raise AttributeError(name)

    def transpose(self) -> core.TransposeProxyModel:
        """Transpose rows/columns.

        Wraps current model with a TransposeProxyModel.
        """
        proxy = core.TransposeProxyModel(parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def flatten(
        self, show_path: bool = False, leaves_only: bool = False
    ) -> itemmodels.FlattenTreeProxyModel:
        """Wraps model in a Proxy which flattens tree to one column.

        Arguments:
            show_path: Whether the first column should show the full tree path.
            leaves_only: whether the proxied model should return only tree leaves.

        """
        # ss = """QTreeView::branch{border-image: url(none.png);}"""
        # self._widget.set_stylesheet(ss)
        from prettyqt import itemmodels

        proxy = itemmodels.FlattenTreeProxyModel(
            parent=self._widget, show_path=show_path, leaves_only=leaves_only
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def melt(
        self, id_columns: list[int], var_name: str = "Variable", value_name: str = "Value"
    ) -> itemmodels.MeltProxyModel:
        """Wraps model in a Proxy which unpivots the table to a long format.

        Arguments:
            id_columns: Identifier variables
            var_name: header to use for variable column
            value_name: header to use for value_name
        """
        from prettyqt import itemmodels

        proxy = itemmodels.MeltProxyModel(
            id_columns=id_columns,
            var_name=var_name,
            value_name=value_name,
            parent=self._widget,
        )
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def reorder_columns(self, order: list[int]) -> itemmodels.ColumnOrderProxyModel:
        """Reorder columns to given order.

        Wraps current model with a ColumnOrderProxyModel which rearranges columns to given
        order.

        Arguments:
            order: list of indexes. Does not need to include all column indexes,
                  missing ones will be hidden.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.ColumnOrderProxyModel(order=order, parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def to_list(self) -> itemmodels.TableToListProxyModel:
        """Convert table to a list.

        Wraps model with a TableToListProxyModel which reshapes table to one column
        by concatenating the seperatate columns into a one-columned list.
        """
        from prettyqt import itemmodels

        proxy = itemmodels.TableToListProxyModel(parent=self._widget)
        proxy.setSourceModel(self._widget.model())
        self._widget.set_model(proxy)
        return proxy

    def add_column(
        self,
        header: str,
        formatter: str,
        flags: constants.ItemFlag | None = None,
    ) -> itemmodels.ColumnJoinerProxyModel:
        """Add a new column with given header to the table.

        Column content can be defined by a formatter.

        Arguments:
            header: Title for section header
            formatter: String formatter (Example: "{2} - {4}" would result in
                       <displayRole of column 2> - <displayRole of column4>
            flags: ItemFlags for new column (default: Enabled and selectable)
        """
        from prettyqt import itemmodels

        proxy = itemmodels.ColumnJoinerProxyModel(parent=self._widget)
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
    ) -> itemmodels.ChangeHeadersProxyModel:
        """Change headers of source model.

        Wraps current model with a ChangeHeadersProxyModel.

        Arguments:
            headers: new headers to use
            orientation: orientation of the header which should be modified.
            role: Header role to change
        """
        from prettyqt import itemmodels

        proxy = itemmodels.ChangeHeadersProxyModel(
            header=headers, role=role, orientation=orientation, parent=self._widget
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
        Klass = classhelpers.get_class_for_id(core.AbstractProxyModelMixin, proxy)
        proxy_instance = Klass(parent=self._widget, **kwargs)
        proxy_instance.setSourceModel(self._widget.model())
        self._widget.set_model(proxy_instance)
        return proxy_instance

    def map_to(
        self,
        index_or_selection: core.ModelIndex | core.QItemSelection,
        target: widgets.QAbstractItemView | core.QAbstractItemModel,
    ) -> core.ModelIndex | core.QItemSelection:
        """Map index or selection to given target.

        Arguments:
            index_or_selection: What should be mapped.
            target: Either an ItemView or a (proxy) model which is linked to our current
                    model.
        """
        if isinstance(target, widgets.QAbstractItemView):
            target = target.model()
        mapper = itemmodels.ProxyMapper(self._widget.model(), target)
        match index_or_selection:
            case core.ModelIndex():
                return mapper.map_index(source=0, target=1, index=index_or_selection)
            case core.QItemSelection():
                return mapper.map_selection(
                    source=0, target=1, selection=index_or_selection
                )
            case _:
                raise TypeError(index_or_selection)

    def map_from(
        self,
        index_or_selection: core.ModelIndex | core.QItemSelection,
        source: widgets.QAbstractItemView | core.QAbstractItemModel,
    ) -> core.ModelIndex | core.QItemSelection:
        """Map index or selection from given source.

        Arguments:
            index_or_selection: What should be mapped.
            source: Either an ItemView or a (proxy) model which is linked to our current
                    model.
        """
        if isinstance(source, widgets.QAbstractItemView):
            source = source.model()
        mapper = itemmodels.ProxyMapper(self._widget.model(), source)
        match index_or_selection:
            case core.ModelIndex():
                return mapper.map_index(source=1, target=0, index=index_or_selection)
            case core.QItemSelection():
                return mapper.map_selection(
                    source=1, target=0, selection=index_or_selection
                )
            case _:
                raise TypeError(index_or_selection)

    def sync_current_selection_with(
        self,
        target: widgets.QAbstractItemView | core.QAbstractItemModel,
    ):
        """Map index or selection from given source.

        Arguments:
            target: Either an ItemView or a (proxy) model which is linked to our current
                    model.
        """
        if isinstance(target, widgets.QAbstractItemView):
            target = target.model()
        itemmodels.ProxyMapper(self._widget.model(), target)


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()

    table = debugging.example_table()
    table.proxifier[0].change_flags(selectable=False, enabled=False)
    table.show()
    with app.debug_mode():
        app.exec()
