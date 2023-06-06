from __future__ import annotations

from collections.abc import Generator
import functools
import importlib.util
import logging
from typing import Any, Literal, overload

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes, helpers

DelegateStr = Literal[
    "widget",
    "variant",
    "html",
    "button",
    "no_focus",
    "render_link",
    "star",
    "radio",
    "progress_bar",
]

logger = logging.getLogger(__name__)

EDIT_TRIGGERS = bidict(
    none=QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers,
    current_changed=QtWidgets.QAbstractItemView.EditTrigger.CurrentChanged,
    double_clicked=QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked,
    selected_clicked=QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked,
    edit_key_pressed=QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed,
    any_key_pressed=QtWidgets.QAbstractItemView.EditTrigger.AnyKeyPressed,
    all=QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers,
)

EditTriggerStr = Literal[
    "none",
    "current_changed",
    "double_clicked",
    "selected_clicked",
    "edit_key_pressed",
    "any_key_pressed",
    "all",
]

SELECTION_BEHAVIOR = bidict(
    rows=QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows,
    columns=QtWidgets.QAbstractItemView.SelectionBehavior.SelectColumns,
    items=QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems,
)

SelectionBehaviourStr = Literal["rows", "columns", "items"]

SELECTION_MODE = bidict(
    single=QtWidgets.QAbstractItemView.SelectionMode.SingleSelection,
    extended=QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection,
    multi=QtWidgets.QAbstractItemView.SelectionMode.MultiSelection,
    none=QtWidgets.QAbstractItemView.SelectionMode.NoSelection,
)

SelectionModeStr = Literal["single", "extended", "multi", "none"]

SCROLL_MODE = bidict(
    item=QtWidgets.QAbstractItemView.ScrollMode.ScrollPerItem,
    pixel=QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel,
)

ScrollModeStr = Literal["item", "pixel"]

SCROLL_HINT = bidict(
    ensure_visible=QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible,
    position_at_top=QtWidgets.QAbstractItemView.ScrollHint.PositionAtTop,
    position_at_bottom=QtWidgets.QAbstractItemView.ScrollHint.PositionAtBottom,
    position_at_center=QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter,
)

ScrollHintStr = Literal[
    "ensure_visible", "position_at_top", "position_at_bottom", "position_at_center"
]

DRAG_DROP_MODE = bidict(
    none=QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop,
    drag=QtWidgets.QAbstractItemView.DragDropMode.DragOnly,
    drop=QtWidgets.QAbstractItemView.DragDropMode.DropOnly,
    drag_drop=QtWidgets.QAbstractItemView.DragDropMode.DragDrop,
    internal_move=QtWidgets.QAbstractItemView.DragDropMode.InternalMove,
)

DragDropModeStr = Literal["none", "drag", "drop", "drag_drop", "internal_move"]


DROP_INDICATOR_POSITION = bidict(
    on_item=QtWidgets.QAbstractItemView.DropIndicatorPosition.OnItem,
    above_item=QtWidgets.QAbstractItemView.DropIndicatorPosition.AboveItem,
    below_item=QtWidgets.QAbstractItemView.DropIndicatorPosition.BelowItem,
    on_viewport=QtWidgets.QAbstractItemView.DropIndicatorPosition.OnViewport,
)

DropIndicatorPositionStr = Literal["on_item", "above_item", "below_item", "on_viewport"]

STATE = bidict(
    none=QtWidgets.QAbstractItemView.State.NoState,
    dragging=QtWidgets.QAbstractItemView.State.DraggingState,
    drag_selecting=QtWidgets.QAbstractItemView.State.DragSelectingState,
    editing=QtWidgets.QAbstractItemView.State.EditingState,
    expanding=QtWidgets.QAbstractItemView.State.ExpandingState,
    collapsing=QtWidgets.QAbstractItemView.State.CollapsingState,
    animating=QtWidgets.QAbstractItemView.State.AnimatingState,
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


class AbstractItemViewMixin(widgets.AbstractScrollAreaMixin):
    model_changed = core.Signal(QtCore.QAbstractItemModel)

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
            "textElideMode": constants.ELIDE_MODE,
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

    @overload
    def set_model(
        self, model: list | dict | QtCore.QAbstractItemModel
    ) -> QtCore.QAbstractItemModel:
        ...

    @overload
    def set_model(self, model: None) -> None:
        ...

    def set_model(
        self, model: QtCore.QAbstractItemModel | list | dict | None
    ) -> QtCore.QAbstractItemModel | None:
        """Set the model of this View.

        In addition to QAbstractItemModels, you can also pass some basic datastructures.
        An appropriate model will be chosen automatically then.
        """
        from prettyqt import custom_models

        match model:
            case dict():
                model = custom_models.JsonModel(model, parent=self)
            case [dict(), *_]:
                model = custom_models.MappingModel(model)
            case [str(), *_]:
                model = core.StringListModel(model)
            case QtCore.QAbstractItemModel() | None:
                pass
            case _:
                if importlib.util.find_spec("pandas") is None:
                    raise ImportError("Install pandas for DataFrame support")
                from prettyqt.qtpandas import pandasmodels
                import pandas as pd

                if not isinstance(model, pd.DataFrame):
                    raise ValueError(model)
                model = pandasmodels.DataTableWithHeaderModel(model)
        # Delete old selection model explicitely, seems to help with memory usage.
        old_model = self.model()
        old_sel_model = self.selectionModel()
        if old_model is not None or model is not None:
            self.setModel(model)
            self.model_changed.emit(model)
            self.setSelectionModel(core.ItemSelectionModel(model))
        # if old_model:
        #     old_model.deleteLater()
        #     del old_model
        if old_sel_model:
            old_sel_model.deleteLater()
            del old_sel_model
        return model

    def get_model(self, skip_proxies: bool = False) -> QtCore.QAbstractItemModel:
        model = self.model()
        if skip_proxies:
            while isinstance(model, QtCore.QAbstractProxyModel):
                model = model.sourceModel()
        return model

    def get_models(self, proxies_only: bool = False) -> list[QtCore.QAbstractProxyModel]:
        model = self.model()
        models = []
        while isinstance(model, QtCore.QAbstractProxyModel):
            models.append(model)
            model = model.sourceModel()
        if (not proxies_only) and model is not None:
            models.append(model)
        return models

    def set_current_index(
        self,
        index: QtCore.QModelIndex | tuple | None,
        operation: Literal["select", "deselect", "toggle"] = "select",
        clear: bool = True,
        current: bool = False,
        expand: Literal["rows", "columns"] | None = None,
    ):
        # index = self.model().index(self._selected_index)
        match index:
            case None:
                self.selectionModel().setCurrentIndex(
                    index, core.ItemSelectionModel.SelectionFlag.Clear
                )
                return
            case tuple():
                index = self.model().index(*index)
            case QtCore.QModelIndex():
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
        index: QtCore.QModelIndex | tuple | None,
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
            case QtCore.QModelIndex():
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

    def move_row_selection(self, dx: int) -> None:
        for row in self.selected_rows():
            new_idx = self.model().index(row + dx, 0)
            if new_idx.isValid():
                self.set_current_index(new_idx, current=True, expand="rows")

    def set_delegate(
        self,
        delegate: QtWidgets.QAbstractItemDelegate | DelegateStr,
        *,
        column: int | None = None,
        row: int | None = None,
        persistent: bool = False,
        **kwargs,
    ):
        # from prettyqt import custom_delegates

        match delegate:
            case QtWidgets.QAbstractItemDelegate():
                pass
            # case "variant":
            #     delegate = custom_delegates.VariantDelegate(parent=self, **kwargs)
            # case "widget":
            #     delegate = custom_delegates.WidgetDelegate(parent=self, **kwargs)
            # case "html":
            #     delegate = custom_delegates.HtmlItemDelegate(parent=self, **kwargs)
            # case "button":
            #     delegate = custom_delegates.ButtonDelegate(parent=self, **kwargs)
            case str():
                Klass = helpers.get_class_for_id(widgets.StyledItemDelegate, delegate)
                delegate = Klass(parent=self, **kwargs)
            # case str():
            #     if delegate in widgets.StyledItemDelegate._registry:
            #         Klass = widgets.StyledItemDelegate._registry[delegate]
            #         logger.debug(f"found delegate for id {delegate!r}")
            #         delegate = Klass(parent=self, **kwargs)
            #     else:
            #         raise ValueError(f"no delegate with id {delegate!r} registered.")
            case _:
                raise ValueError(delegate)
        match column, row:
            case int(), int():
                raise ValueError("Only set column or row, not both.")
            case int(), None:
                self.setItemDelegateForColumn(column, delegate)
                if persistent:
                    model = self.model()
                    for i in range(model.rowCount()):
                        index = model.index(i, column)
                        self.openPersistentEditor(index)
            case None, int():
                self.setItemDelegateForRow(row, delegate)
                if persistent:
                    model = self.model()
                    for i in range(model.columnCount()):
                        self.openPersistentEditor(model.index(row, i))
            case None, None:
                self.setItemDelegate(delegate)
                if persistent:
                    model = self.model()
                    for i in range(model.rowCount()):
                        for j in range(model.columnCount()):
                            self.openPersistentEditor(model.index(i, j))
        return delegate

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

    def current_index(self) -> QtCore.QModelIndex | None:
        if (model := self.selectionModel()) is not None:
            return model.currentIndex()

    def current_data(self, role=constants.USER_ROLE):
        if (model := self.selectionModel()) is not None:
            idx = model.currentIndex()
            return idx.data(role)

    def current_row(self) -> int | None:
        if (model := self.selectionModel()) is not None:
            return model.currentIndex().row()

    def current_column(self) -> int | None:
        if (model := self.selectionModel()) is not None:
            return model.currentIndex().column()

    def selected_indexes(self) -> list[QtCore.QModelIndex]:
        """Return list of selected indexes in first row."""
        indexes = (x for x in self.selectedIndexes() if x.column() == 0)
        return sorted(indexes, key=lambda x: x.row())

    def selected_names(self) -> Generator[Any, None, None]:
        """Return generator yielding item names."""
        return (x.data(constants.NAME_ROLE) for x in self.selected_indexes())

    def selected_rows(self) -> Generator[int, None, None]:
        """Return generator yielding row nums."""
        return (x.row() for x in self.selected_indexes())

    def selected_data(self, role=constants.USER_ROLE) -> Generator[Any, None, None]:
        """Return generator yielding selected userData."""
        return (x.data(role) for x in self.selected_indexes())

    def setup_dragdrop_move(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.DragDropMode.DragDrop)
        self.setDefaultDropAction(constants.MOVE_ACTION)
        self.setDropIndicatorShown(True)

    def set_edit_triggers(self, *triggers: EditTriggerStr | None):
        items = ["none" if t is None else t for t in triggers]
        for item in items:
            if item not in EDIT_TRIGGERS:
                raise InvalidParamError(item, EDIT_TRIGGERS)
        flags = EDIT_TRIGGERS.merge_flags(items)
        self.setEditTriggers(flags)

    def get_edit_triggers(self) -> list[EditTriggerStr]:
        return EDIT_TRIGGERS.get_list(self.editTriggers())

    def set_selection_behavior(self, behaviour: SelectionBehaviourStr):
        """Set selection behaviour for given item view.

        Args:
            behaviour: selection behaviour to use

        Raises:
            InvalidParamError: behaviour does not exist
        """
        if behaviour not in SELECTION_BEHAVIOR:
            raise InvalidParamError(behaviour, SELECTION_BEHAVIOR)
        self.setSelectionBehavior(SELECTION_BEHAVIOR[behaviour])

    def get_selection_behavior(self) -> SelectionBehaviourStr:
        """Return current selection behaviour.

        Returns:
            selection behaviour
        """
        return SELECTION_BEHAVIOR.inverse[self.selectionBehavior()]

    def get_drop_indicator_position(self) -> DropIndicatorPositionStr:
        """Return position of the drop indicator in relation to the closest item.

        Returns:
            drop indicator position
        """
        return DROP_INDICATOR_POSITION.inverse[self.dropIndicatorPosition()]

    def set_drag_drop_mode(self, mode: DragDropModeStr):
        """Set drag-drop mode for given item view.

        Args:
            mode: drag-drop mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in DRAG_DROP_MODE:
            raise InvalidParamError(mode, DRAG_DROP_MODE)
        self.setDragDropMode(DRAG_DROP_MODE[mode])

    def get_drag_drop_mode(self) -> DragDropModeStr:
        """Return current drag-drop mode.

        Returns:
            drag-drop mode
        """
        return DRAG_DROP_MODE.inverse[self.dragDropMode()]

    def set_state(self, state: StateStr):
        """Set state for given item view.

        Args:
            state: state to use

        Raises:
            InvalidParamError: state does not exist
        """
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        self.setState(STATE[state])

    def get_state(self) -> StateStr:
        """Return current state.

        Returns:
            state
        """
        return STATE.inverse[self.state()]

    def set_selection_mode(self, mode: SelectionModeStr | None):
        """Set selection mode for given item view.

        Args:
            mode: selection mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode is None:
            mode = "none"
        if mode not in SELECTION_MODE:
            raise InvalidParamError(mode, SELECTION_MODE)
        self.setSelectionMode(SELECTION_MODE[mode])

    def get_selection_mode(self) -> SelectionModeStr:
        """Return current selection mode.

        Returns:
            selection mode
        """
        return SELECTION_MODE.inverse[self.selectionMode()]

    def set_scroll_mode(self, mode: ScrollModeStr):
        """Set the scroll mode for both directions.

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid scroll mode
        """
        if mode not in SCROLL_MODE:
            raise InvalidParamError(mode, SCROLL_MODE)
        self.setHorizontalScrollMode(SCROLL_MODE[mode])
        self.setVerticalScrollMode(SCROLL_MODE[mode])

    def set_horizontal_scroll_mode(self, mode: ScrollModeStr):
        """Set the horizontal scroll mode.

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid scroll mode
        """
        if mode not in SCROLL_MODE:
            raise InvalidParamError(mode, SCROLL_MODE)
        self.setHorizontalScrollMode(SCROLL_MODE[mode])

    def get_horizontal_scroll_mode(self) -> ScrollModeStr:
        """Return current horizontal scroll mode.

        Returns:
            horizontal scroll mode
        """
        return SCROLL_MODE.inverse[self.horizontalScrollMode()]

    def set_vertical_scroll_mode(self, mode: ScrollModeStr):
        """Set the vertical scroll mode.

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid scroll mode
        """
        if mode not in SCROLL_MODE:
            raise InvalidParamError(mode, SCROLL_MODE)
        self.setVerticalScrollMode(SCROLL_MODE[mode])

    def get_vertical_scroll_mode(self) -> ScrollModeStr:
        """Return current vertical scroll mode.

        Returns:
            vertical scroll mode
        """
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
        self, index: QtCore.QModelIndex, mode: ScrollHintStr = "ensure_visible"
    ):
        if mode not in SCROLL_HINT:
            raise InvalidParamError(mode, SCROLL_HINT)
        self.scrollTo(index, SCROLL_HINT[mode])

    def highlight_when_inactive(self):
        """Highlight items when widget does not have focus."""
        p = self.get_palette()
        p.highlight_inactive()
        self.setPalette(p)

    def set_icon_size(self, size: int | datatypes.SizeType):
        if isinstance(size, tuple):
            size = QtCore.QSize(*size)
        elif isinstance(size, int):
            size = QtCore.QSize(size, size)
        self.setIconSize(size)

    def get_size_hint_for_column(self, col: int, limit_ms: int | None = None):
        to_check = min(25, self.model().rowCount())
        max_width = 0
        for row in range(to_check):
            v = self.sizeHintForIndex(self.model().index(row, col))
            max_width = max(max_width, v.width())
        return max_width

    def sync_with(
        self,
        table_to_sync: widgets.QAbstractItemView,
        orientation: constants.OrientationStr,
    ) -> list[core.QMetaObject.Connection]:
        def _table_resized(col, _, new_size, table, orientation):
            if orientation == "horizontal":
                table.setColumnWidth(col, new_size)
            else:
                table.setRowHeight(col, new_size)

        _table_1_resized = functools.partial(
            _table_resized, table=self, orientation=orientation
        )
        _table_2_resized = functools.partial(
            _table_resized, table=table_to_sync, orientation=orientation
        )
        if orientation == "vertical":
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


class AbstractItemView(AbstractItemViewMixin, QtWidgets.QAbstractItemView):
    pass
