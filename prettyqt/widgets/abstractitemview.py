from __future__ import annotations

from collections.abc import Generator, Sequence
import functools
import importlib.util
import logging

from typing import Any, Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict, classhelpers, datatypes, listdelegators


DelegateStr = Literal[
    "widget",
    "editor",
    "html",
    "button",
    "no_focus",
    "render_link",
    "star",
    "radio",
    "progress_bar",
]

logger = logging.getLogger(__name__)

EditTriggerStr = Literal[
    "none",
    "current_changed",
    "double_clicked",
    "selected_clicked",
    "edit_key_pressed",
    "any_key_pressed",
    "all",
]

EDIT_TRIGGERS: bidict[EditTriggerStr, widgets.QAbstractItemView.EditTrigger] = bidict(
    none=widgets.QAbstractItemView.EditTrigger.NoEditTriggers,
    current_changed=widgets.QAbstractItemView.EditTrigger.CurrentChanged,
    double_clicked=widgets.QAbstractItemView.EditTrigger.DoubleClicked,
    selected_clicked=widgets.QAbstractItemView.EditTrigger.SelectedClicked,
    edit_key_pressed=widgets.QAbstractItemView.EditTrigger.EditKeyPressed,
    any_key_pressed=widgets.QAbstractItemView.EditTrigger.AnyKeyPressed,
    all=widgets.QAbstractItemView.EditTrigger.AllEditTriggers,
)

SelectionBehaviourStr = Literal["rows", "columns", "items"]

SELECTION_BEHAVIOR: bidict[
    SelectionBehaviourStr, widgets.QAbstractItemView.SelectionBehavior
] = bidict(
    rows=widgets.QAbstractItemView.SelectionBehavior.SelectRows,
    columns=widgets.QAbstractItemView.SelectionBehavior.SelectColumns,
    items=widgets.QAbstractItemView.SelectionBehavior.SelectItems,
)

SelectionModeStr = Literal["single", "extended", "multi", "none"]

SELECTION_MODE: bidict[
    SelectionModeStr, widgets.QAbstractItemView.SelectionMode
] = bidict(
    single=widgets.QAbstractItemView.SelectionMode.SingleSelection,
    extended=widgets.QAbstractItemView.SelectionMode.ExtendedSelection,
    multi=widgets.QAbstractItemView.SelectionMode.MultiSelection,
    none=widgets.QAbstractItemView.SelectionMode.NoSelection,
)

ScrollModeStr = Literal["item", "pixel"]

SCROLL_MODE: bidict[ScrollModeStr, widgets.QAbstractItemView.ScrollMode] = bidict(
    item=widgets.QAbstractItemView.ScrollMode.ScrollPerItem,
    pixel=widgets.QAbstractItemView.ScrollMode.ScrollPerPixel,
)


ScrollHintStr = Literal[
    "ensure_visible", "position_at_top", "position_at_bottom", "position_at_center"
]

SCROLL_HINT: bidict[ScrollHintStr, widgets.QAbstractItemView.ScrollHint] = bidict(
    ensure_visible=widgets.QAbstractItemView.ScrollHint.EnsureVisible,
    position_at_top=widgets.QAbstractItemView.ScrollHint.PositionAtTop,
    position_at_bottom=widgets.QAbstractItemView.ScrollHint.PositionAtBottom,
    position_at_center=widgets.QAbstractItemView.ScrollHint.PositionAtCenter,
)

DragDropModeStr = Literal["none", "drag", "drop", "drag_drop", "internal_move"]

DRAG_DROP_MODE: bidict[DragDropModeStr, widgets.QAbstractItemView.DragDropMode] = bidict(
    none=widgets.QAbstractItemView.DragDropMode.NoDragDrop,
    drag=widgets.QAbstractItemView.DragDropMode.DragOnly,
    drop=widgets.QAbstractItemView.DragDropMode.DropOnly,
    drag_drop=widgets.QAbstractItemView.DragDropMode.DragDrop,
    internal_move=widgets.QAbstractItemView.DragDropMode.InternalMove,
)


DropIndicatorPositionStr = Literal["on_item", "above_item", "below_item", "on_viewport"]

DROP_INDICATOR_POSITION: bidict[
    DropIndicatorPositionStr, widgets.QAbstractItemView.DropIndicatorPosition
] = bidict(
    on_item=widgets.QAbstractItemView.DropIndicatorPosition.OnItem,
    above_item=widgets.QAbstractItemView.DropIndicatorPosition.AboveItem,
    below_item=widgets.QAbstractItemView.DropIndicatorPosition.BelowItem,
    on_viewport=widgets.QAbstractItemView.DropIndicatorPosition.OnViewport,
)


StateStr = Literal[
    "none",
    "dragging",
    "drag_selecting",
    "editing",
    "expanding",
    "collapsing",
    "animating",
]

STATE: bidict[StateStr, widgets.QAbstractItemView.State] = bidict(
    none=widgets.QAbstractItemView.State.NoState,
    dragging=widgets.QAbstractItemView.State.DraggingState,
    drag_selecting=widgets.QAbstractItemView.State.DragSelectingState,
    editing=widgets.QAbstractItemView.State.EditingState,
    expanding=widgets.QAbstractItemView.State.ExpandingState,
    collapsing=widgets.QAbstractItemView.State.CollapsingState,
    animating=widgets.QAbstractItemView.State.AnimatingState,
)


class AbstractItemViewMixin(widgets.AbstractScrollAreaMixin):
    model_changed = core.Signal(core.QAbstractItemModel)

    def __init__(
        self,
        *args,
        horizontal_scroll_mode="pixel",
        vertical_scroll_mode="pixel",
        **kwargs,
    ):
        super().__init__(
            *args,
            horizontal_scroll_mode=horizontal_scroll_mode,
            vertical_scroll_mode=vertical_scroll_mode,
            **kwargs,
        )
        from prettyqt.utils import proxifier

        self.proxifier = proxifier.Proxifier(self)

    def __len__(self) -> int:
        return model.rowCount() if (model := self.model()) is not None else 0

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "dragDropMode": DRAG_DROP_MODE,
            "horizontalScrollMode": SCROLL_MODE,
            "verticalScrollMode": SCROLL_MODE,
            "selectionMode": SELECTION_MODE,
            "selectionBehavior": SELECTION_BEHAVIOR,
            "defaultDropAction": constants.DROP_ACTION,
            "textElideMode": constants.TEXT_ELIDE_MODE,
            "editTriggers": EDIT_TRIGGERS,
        }
        return maps

    def selectAll(self):
        """Override, we dont want to selectAll for too many items bc of performance."""
        if self.model() is None:
            return
        if self.model().rowCount() * self.model().columnCount() > 1_000_000:
            logger.warning("Too many cells to select.")
            return
        super().selectAll()

    def set_model(self, model: core.QAbstractItemModel | None):
        """Set the model of this View."""
        # Delete old selection model explicitely, seems to help with memory usage.
        old_model = self.model()
        old_sel_model = self.selectionModel()
        if old_model is not None or model is not None:
            self.setModel(model)
            if model is not None:
                # always set a parent. PySide6 needs one for proxying.
                model.setParent(self)
                self.setSelectionModel(core.ItemSelectionModel(model))
            self.model_changed.emit(model)
        # if old_model:
        #     old_model.deleteLater()
        #     del old_model
        if old_sel_model:
            old_sel_model.deleteLater()
            del old_sel_model
        return model

    def set_model_for(self, data: Any):
        """Set model for given data type.

        Pass any data structure and an appropriate model will be chosen automatically.

        Args:
            data: data to choose model for.
        """
        # we import to collect the models
        from prettyqt import itemmodels  # noqa: F401

        # TODO: probably better to check models from external modules later
        # so we dont have to import everything even if not needed.
        if importlib.util.find_spec("pandas") is not None:
            from prettyqt.qtpandas import pandasmodels  # noqa: F401

        for Klass in classhelpers.get_subclasses(core.QAbstractItemModel):
            if (
                "supports" in Klass.__dict__
                and callable(Klass.supports)
                and Klass.supports(data)
                and Klass.__name__ != "PythonObjectTreeModel"
            ):
                logger.debug(f"found model for data structure {data!r}")
                break
        else:
            raise TypeError("No suiting model found.")
        model = Klass(data, parent=self)
        self.set_model(model)

    def get_model(self, skip_proxies: bool = False) -> core.QAbstractItemModel:
        """Get current model of the ItemView.

        Arguments:
            skip_proxies: Whether to get current model or the non-proxy sourceModel.
        """
        model = self.model()
        if skip_proxies:
            while isinstance(model, core.QAbstractProxyModel):
                model = model.sourceModel()
        return model

    def get_models(
        self, proxies_only: bool = False
    ) -> listdelegators.ListDelegator[core.QAbstractProxyModel]:
        """Get a list of all (proxy) models connected to this view.

        Arguments:
            proxies_only: whether the non-proxy sourceModel should be included.
        """
        model = self.model()
        models = []
        while isinstance(model, core.QAbstractProxyModel):
            models.append(model)
            model = model.sourceModel()
        if (not proxies_only) and model is not None:
            models.append(model)
        return listdelegators.ListDelegator(models)

    def set_current_index(
        self,
        index: core.QModelIndex | tuple | None,
        operation: Literal["select", "deselect", "toggle"] = "select",
        clear: bool = True,
        current: bool = False,
        expand: Literal["rows", "columns"] | None = None,
    ):
        """Set current index.

        Arguments:
            index: Index to set.
            operation: Whether to select, deselect or toggle the current state.
            clear: Clear Whether to clear previously selected indexes.
            current: Current selection will be updated.
            expand: Whether to expand selection to whole column / row.
        """
        match index:
            case None:
                self.selectionModel().setCurrentIndex(
                    index, core.ItemSelectionModel.SelectionFlag.Clear
                )
                return
            case tuple():
                index = self.model().index(*index)
            case core.QModelIndex():
                pass
            case _:
                raise ValueError(index)
        match operation:
            case "select":
                flag = core.ItemSelectionModel.SelectionFlag.Select
            case "deselect":
                flag = core.ItemSelectionModel.SelectionFlag.Deselect
            case "toggle":
                flag = core.ItemSelectionModel.SelectionFlag.Toggle
            case _:
                raise ValueError(operation)
        if clear:
            flag |= core.ItemSelectionModel.SelectionFlag.Clear
        if current:
            flag |= core.ItemSelectionModel.SelectionFlag.Current
        match expand:
            case "rows":
                flag |= core.ItemSelectionModel.SelectionFlag.Rows
            case "columns":
                flag |= core.ItemSelectionModel.SelectionFlag.Columns
            case None:
                pass
            case _:
                raise ValueError(expand)
        self.selectionModel().setCurrentIndex(index, flag)

    def select_index(
        self,
        index: core.QModelIndex | tuple | None,
        operation: Literal["select", "deselect", "toggle"] = "select",
        clear: bool = True,
        current: bool = False,
        expand: Literal["rows", "columns"] | None = None,
    ):
        # index = self.model().index(self._selected_index)
        match index:
            case None:
                self.selectionModel().setCurrentIndex(
                    core.ModelIndex(), core.ItemSelectionModel.SelectionFlag.Clear
                )
                return
            case tuple():
                index = self.model().index(*index)
            case core.QModelIndex():
                pass
            case _:
                raise ValueError(index)
        match operation:
            case "select":
                flag = core.ItemSelectionModel.SelectionFlag.Select
            case "deselect":
                flag = core.ItemSelectionModel.SelectionFlag.Deselect
            case "toggle":
                flag = core.ItemSelectionModel.SelectionFlag.Toggle
            case _:
                raise ValueError(operation)
        if clear:
            flag |= core.ItemSelectionModel.SelectionFlag.Clear
        if current:
            flag |= core.ItemSelectionModel.SelectionFlag.Current
        match expand:
            case "rows":
                flag |= core.ItemSelectionModel.SelectionFlag.Rows
            case "columns":
                flag |= core.ItemSelectionModel.SelectionFlag.Columns
            case None:
                pass
            case _:
                raise ValueError(expand)
        self.selectionModel().select(index, flag)

    # def move_selection(self, row_offset: int = 0, column_offset: int = 0):
    #     """Move selection by an offset."""
    #     for index in self.selectedIndexes():
    #         new_idx = self.model().index(
    #             index.row() + row_offset, index.column() + column_offset, index.parent()
    #         )
    #         if new_idx.isValid():
    #             self.set_current_index(new_idx, current=True, expand="rows")

    def move_row_selection(self, dy: int):
        for row in self.selected_rows():
            new_idx = self.model().index(row + dy, 0)
            if new_idx.isValid():
                self.set_current_index(new_idx, current=True, expand="rows")

    def set_delegate(
        self,
        delegate: widgets.QAbstractItemDelegate | DelegateStr | None,
        *,
        column: int | Sequence | None = None,
        row: int | Sequence | None = None,
        persistent: bool = False,
        **kwargs,
    ):
        """Set a item delegate for the view.

        Arguments:
            delegate: Delegate to set. Can also be the id of the delegate.
            column: Column the delegate should be set for.
            row: Row the column should be set for.
            persistent: If True, open persistent editors for given area.
            kwargs: Keyword args to pass to the Delegate ctor if delegate is set by id.
        """
        match delegate:
            case widgets.QAbstractItemDelegate():
                dlg = delegate
            # case "editor":
            #     delegate = itemdelegates.EditorDelegate(parent=self, **kwargs)
            # case "widget":
            #     delegate = itemdelegates.WidgetDelegate(parent=self, **kwargs)
            # case "html":
            #     delegate = itemdelegates.HtmlItemDelegate(parent=self, **kwargs)
            # case "button":
            #     delegate = itemdelegates.ButtonDelegate(parent=self, **kwargs)
            case str():
                Klass = classhelpers.get_class_for_id(
                    widgets.StyledItemDelegate, delegate
                )
                dlg = Klass(parent=self, **kwargs)
            case None:
                dlg = widgets.StyledItemDelegate()
            case _:
                raise ValueError(delegate)
        match column, row:
            case int(), int():
                raise ValueError("Only set column or row, not both.")
            case Sequence(), None:
                for i in column:
                    self.set_delegate(delegate, column=i, row=row, persistent=persistent)
            case int(), None:
                self.setItemDelegateForColumn(column, dlg)
                if persistent:
                    model = self.model()
                    for i in range(model.rowCount()):
                        index = model.index(i, column)
                        self.openPersistentEditor(index)
            case None, Sequence():
                for i in row:
                    self.set_delegate(
                        delegate, column=column, row=i, persistent=persistent
                    )
            case None, int():
                self.setItemDelegateForRow(row, dlg)
                if persistent:
                    model = self.model()
                    for i in range(model.columnCount()):
                        self.openPersistentEditor(model.index(row, i))
            case None, None:
                self.setItemDelegate(dlg)
                if persistent:
                    model = self.model()
                    for i in range(model.rowCount()):
                        for j in range(model.columnCount()):
                            self.openPersistentEditor(model.index(i, j))
        return dlg

    def toggle_select_all(self):
        """Select all items from list (deselect when all selected)."""
        if self.selectionModel() is None:
            return
        if self.selectionModel().hasSelection():
            self.clearSelection()
        else:
            self.selectAll()

    def set_table_color(self, color: str):
        with self.edit_stylesheet() as ss:
            ss.QHeaderView.section.backgroundColor.setValue(color)

    def current_index(self) -> core.QModelIndex | None:
        if (model := self.selectionModel()) is not None:
            return model.currentIndex()
        return None

    def current_data(self, role=constants.USER_ROLE):
        if (model := self.selectionModel()) is not None:
            idx = model.currentIndex()
            return idx.data(role)

    def current_row(self) -> int | None:
        if (model := self.selectionModel()) is not None:
            return model.currentIndex().row()
        return None

    def current_column(self) -> int | None:
        if (model := self.selectionModel()) is not None:
            return model.currentIndex().column()
        return None

    def selected_indexes(self) -> listdelegators.ListDelegator[core.QModelIndex]:
        """Return list of selected indexes in first row."""
        indexes = (x for x in self.selectedIndexes() if x.column() == 0)
        indexes = sorted(indexes, key=lambda x: x.row())
        return listdelegators.ListDelegator(indexes)

    def selected_names(self) -> Generator[Any, None, None]:
        """Return generator yielding item names."""
        return (x.data(constants.NAME_ROLE) for x in self.selected_indexes())

    def selected_rows(self) -> Generator[int, None, None]:
        """Return generator yielding row nums."""
        return (x.row() for x in self.selected_indexes())

    def selected_data(self, role=constants.USER_ROLE) -> Generator[Any, None, None]:
        """Return generator yielding selected userData.

        Arguments:
            role: ItemRole to return data for.
        """
        return (x.data(role) for x in self.selected_indexes())

    def setup_dragdrop_move(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.DragDropMode.DragDrop)
        self.setDefaultDropAction(constants.MOVE_ACTION)
        self.setDropIndicatorShown(True)

    def set_edit_triggers(self, *triggers: EditTriggerStr | None):
        items = ["none" if t is None else t for t in triggers]
        flags = EDIT_TRIGGERS.merge_flags(items)
        self.setEditTriggers(flags)

    def get_edit_triggers(self) -> list[EditTriggerStr]:
        return EDIT_TRIGGERS.get_list(self.editTriggers())

    def set_selection_behavior(
        self,
        behavior: SelectionBehaviourStr | widgets.QAbstractItemView.SelectionBehavior,
    ):
        """Set selection behavior for given item view.

        Arguments:
            behavior: Selection behavior
        """
        self.setSelectionBehavior(SELECTION_BEHAVIOR.get_enum_value(behavior))

    def get_selection_behavior(self) -> SelectionBehaviourStr:
        """Return current selection behavior.

        Returns:
            selection behavior
        """
        return SELECTION_BEHAVIOR.inverse[self.selectionBehavior()]

    def get_drop_indicator_position(self) -> DropIndicatorPositionStr:
        """Return position of the drop indicator in relation to the closest item."""
        return DROP_INDICATOR_POSITION.inverse[self.dropIndicatorPosition()]

    def set_drag_drop_mode(
        self, mode: DragDropModeStr | widgets.QAbstractItemView.DragDropMode
    ):
        """Set drag-drop mode for given item view.

        Args:
            mode: drag-drop mode to use
        """
        self.setDragDropMode(DRAG_DROP_MODE.get_enum_value(mode))

    def get_drag_drop_mode(self) -> DragDropModeStr:
        """Return current drag-drop mode."""
        return DRAG_DROP_MODE.inverse[self.dragDropMode()]

    def set_state(self, state: StateStr | widgets.QAbstractItemView.State):
        """Set state for given item view.

        Args:
            state: state to use
        """
        self.setState(STATE.get_enum_value(state))

    def get_state(self) -> StateStr:
        """Return current state."""
        return STATE.inverse[self.state()]

    def set_selection_mode(
        self, mode: SelectionModeStr | widgets.QAbstractItemView.SelectionMode | None
    ):
        """Set selection mode for given item view.

        Args:
            mode: selection mode to use
        """
        if mode is None:
            mode = "none"
        self.setSelectionMode(SELECTION_MODE.get_enum_value(mode))

    def get_selection_mode(self) -> SelectionModeStr:
        """Return current selection mode."""
        return SELECTION_MODE.inverse[self.selectionMode()]

    def set_scroll_mode(self, mode: ScrollModeStr | widgets.QAbstractItemView.ScrollMode):
        """Set the scroll mode for both directions.

        Args:
            mode: mode to set
        """
        self.setHorizontalScrollMode(SCROLL_MODE.get_enum_value(mode))
        self.setVerticalScrollMode(SCROLL_MODE.get_enum_value(mode))

    def set_horizontal_scroll_mode(
        self, mode: ScrollModeStr | widgets.QAbstractItemView.ScrollMode
    ):
        """Set the horizontal scroll mode.

        Args:
            mode: mode to set
        """
        self.setHorizontalScrollMode(SCROLL_MODE.get_enum_value(mode))

    def get_horizontal_scroll_mode(self) -> ScrollModeStr:
        """Return current horizontal scroll mode."""
        return SCROLL_MODE.inverse[self.horizontalScrollMode()]

    def set_vertical_scroll_mode(
        self, mode: ScrollModeStr | widgets.QAbstractItemView.ScrollMode
    ):
        """Set the vertical scroll mode.

        Args:
            mode: mode to set
        """
        self.setVerticalScrollMode(SCROLL_MODE.get_enum_value(mode))

    def get_vertical_scroll_mode(self) -> ScrollModeStr:
        """Return current vertical scroll mode."""
        return SCROLL_MODE.inverse[self.verticalScrollMode()]

    def num_selected(self) -> int:
        """Return amount of selected rows.

        Returns:
            amount of selected rows
        """
        if (model := self.selectionModel()) is not None:
            return len(model.selectedRows())
        return 0

    def jump_to_column(self, col_num: int):
        """Make sure column at given index is visible.

        scrolls to column at given index

        Args:
            col_num: column to scroll to
        """
        if (model := self.model()) is not None:
            idx = model.index(0, col_num)
            self.scrollTo(idx)

    def scroll_to_top(self):
        """Override to use abstractitemview-way of scrolling to top."""
        self.scrollToTop()

    def scroll_to_bottom(self):
        """Override to use abstractitemview-way of scrolling to bottom."""
        self.scrollToBottom()

    def select_last_row(self):
        idx = self.model().createIndex(self.model().rowCount() - 1, 0)
        self.setCurrentIndex(idx)

    def select_first_row(self):
        idx = self.model().index(0, 0)
        self.set_current_index(idx, current=True, expand="rows")

    def scroll_to(
        self,
        index: core.QModelIndex,
        mode: ScrollHintStr | widgets.QAbstractItemView.ScrollHint = "ensure_visible",
    ):
        self.scrollTo(index, SCROLL_HINT.get_enum_value(mode))

    def highlight_when_inactive(self):
        """Highlight items when widget does not have focus."""
        p = self.get_palette()
        p.highlight_inactive()
        self.setPalette(p)

    def set_icon_size(self, size: datatypes.SizeType):
        self.setIconSize(datatypes.to_size(size))

    def get_size_hint_for_column(self, col: int, row_limit: int = 25) -> int:
        """Get a size hint for given column by finding widest cell.

        Arguments:
            col: columnt to get size hint for.
            row_limit: number of rows to check.
        """
        to_check = min(row_limit, self.model().rowCount())
        return max(
            self.sizeHintForIndex(self.model().index(row, col)).width()
            for row in range(to_check)
        )

    def sync_with(
        self,
        table_to_sync: widgets.QAbstractItemView,
        orientation: constants.OrientationStr | constants.Orientation,
    ) -> list[core.QMetaObject.Connection]:
        orientation = constants.ORIENTATION.get_enum_value(orientation)
        """Sync ItemView cell widths and scrollbars with another ItemView.

        Arguments:
            table_to_sync: Table to sync with
            orientation: Whether to sync horizontal or vertical orientation.
        """

        def _table_resized(col, _, new_size, table, orientation):
            if orientation == constants.HORIZONTAL:
                table.setColumnWidth(col, new_size)
            else:
                table.setRowHeight(col, new_size)

        _table_1_resized = functools.partial(
            _table_resized, table=self, orientation=orientation
        )
        _table_2_resized = functools.partial(
            _table_resized, table=table_to_sync, orientation=orientation
        )
        if orientation == constants.VERTICAL:
            h1 = self.v_scrollbar.valueChanged.connect(table_to_sync.v_scrollbar.setValue)
            h2 = table_to_sync.v_scrollbar.valueChanged.connect(self.v_scrollbar.setValue)
            h3 = self.v_header.sectionResized.connect(_table_2_resized)
            h4 = table_to_sync.v_header.sectionResized.connect(_table_1_resized)
        else:
            h1 = self.h_scrollbar.valueChanged.connect(table_to_sync.h_scrollbar.setValue)
            h2 = table_to_sync.h_scrollbar.valueChanged.connect(self.h_scrollbar.setValue)
            h3 = self.h_header.sectionResized.connect(_table_2_resized)
            h4 = table_to_sync.h_header.sectionResized.connect(_table_1_resized)
        return [h1, h2, h3, h4]

    def get_visible_section_span(
        self, orientation: constants.OrientationStr | constants.Orientation
    ) -> tuple[int, int]:
        """Get range of visible sections.

        Arguments:
            orientation: Whether to get section span for horizontal or vertical header.
        """
        orientation = constants.ORIENTATION.get_enum_value(orientation)
        top_left = core.QPoint(0, 0)
        bottom_right = self.viewport().rect().bottomRight()
        if orientation == constants.HORIZONTAL:
            start = self.indexAt(top_left).column()
            count = self.model().columnCount()
            end = self.indexAt(bottom_right).column()
        else:
            start = self.indexAt(top_left).row()
            count = self.model().rowCount()
            end = self.indexAt(bottom_right).row()
        if count == 0:
            return (-1, -1)
        end = count if end == -1 else end + 1
        return (start, end)


class AbstractItemView(AbstractItemViewMixin, widgets.QAbstractItemView):
    pass


if __name__ == "__main__":
    import pandas as pd

    df = pd.DataFrame(dict(a=[1]))
    app = widgets.app()
    table = widgets.TableView()
    table.set_model_for(df)
    table.show()
    app.exec()
