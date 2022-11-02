from __future__ import annotations

from collections.abc import Generator
import logging
from typing import Any, Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, helpers, types


logger = logging.getLogger(__name__)

EDIT_TRIGGERS = bidict(
    none=QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers,
    double_click=QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked,
    edit_key=QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed,
)

EditTriggerStr = Literal["none", "double_click", "edit_key"]

SELECTION_BEHAVIOUR = bidict(
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

DragDropModeStr = Literal["none", "drag", "drop", "drag_drop", "internal"]

QtWidgets.QAbstractItemView.__bases__ = (widgets.AbstractScrollArea,)


class AbstractItemView(QtWidgets.QAbstractItemView):
    def __len__(self) -> int:
        if self.model() is not None:
            return self.model().rowCount()
        return 0

    def selectAll(self):
        """Override, we dont want to selectAll for too many items bc of performance."""
        if self.model() is None:
            return
        if self.model().rowCount() * self.model().columnCount() > 1_000_000:
            logger.warning("Too many cells to select.")
            return
        super().selectAll()

    def set_model(self, model: QtCore.QAbstractItemModel | None):
        """Delete old selection model explicitely, seems to help with memory usage."""
        old_model = self.model()
        old_sel_model = self.selectionModel()
        if old_model is not None or model is not None:
            self.setModel(model)  # type: ignore
        # if old_model:
        #     old_model.deleteLater()
        #     del old_model
        if old_sel_model:
            old_sel_model.deleteLater()
            del old_sel_model

    def set_delegate(
        self,
        delegate: QtWidgets.QItemDelegate,
        column: int | None = None,
        row: int | None = None,
        persistent: bool = False,
    ):
        if column is not None:
            self.setItemDelegateForColumn(column, delegate)
            if persistent:
                model = self.model()
                for i in range(0, model.rowCount()):
                    self.openPersistentEditor(model.index(i, column))
        elif row is not None:
            self.setItemDelegateForRow(row, delegate)
            if persistent:
                model = self.model()
                for i in range(0, model.columnCount()):
                    self.openPersistentEditor(model.index(row, i))
        else:
            self.setItemDelegate(delegate)

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
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex()

    def current_data(self):
        if self.selectionModel() is None:
            return None
        idx = self.selectionModel().currentIndex()
        return idx.data(constants.USER_ROLE)  # type: ignore

    def current_row(self) -> int | None:
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex().row()

    def current_column(self) -> int | None:
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex().column()

    def selected_indexes(self) -> list[QtCore.QModelIndex]:
        """Returns list of selected indexes in first row."""
        indexes = (x for x in self.selectedIndexes() if x.column() == 0)  # type: ignore
        return sorted(indexes, key=lambda x: x.row())  # type: ignore

    def selected_names(self) -> Generator[Any, None, None]:
        """Returns generator yielding item names."""
        return (x.data(constants.NAME_ROLE) for x in self.selected_indexes())

    def selected_rows(self) -> Generator[int, None, None]:
        """Returns generator yielding row nums."""
        return (x.row() for x in self.selected_indexes())

    def selected_data(self) -> Generator[Any, None, None]:
        """Returns generator yielding selected userData."""
        return (
            x.data(constants.USER_ROLE) for x in self.selected_indexes()  # type: ignore
        )

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
        flags = helpers.merge_flags(items, EDIT_TRIGGERS)
        self.setEditTriggers(flags)

    def get_edit_triggers(self) -> list[EditTriggerStr]:
        return [k for k, v in EDIT_TRIGGERS.items() if v & self.editTriggers()]

    def set_selection_behaviour(self, behaviour: SelectionBehaviourStr):
        """Set selection behaviour for given item view.

        Args:
            behaviour: selection behaviour to use

        Raises:
            InvalidParamError: behaviour does not exist
        """
        if behaviour not in SELECTION_BEHAVIOUR:
            raise InvalidParamError(behaviour, SELECTION_BEHAVIOUR)
        self.setSelectionBehavior(SELECTION_BEHAVIOUR[behaviour])

    def get_selection_behaviour(self) -> SelectionBehaviourStr:
        """Return current selection behaviour.

        Returns:
            selection behaviour
        """
        return SELECTION_BEHAVIOUR.inverse[self.selectionBehavior()]

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

    def num_selected(self) -> int:
        """Return amount of selected rows.

        Returns:
            amount of selected rows
        """
        if self.selectionModel() is None:
            return 0
        return len(self.selectionModel().selectedRows())

    def jump_to_column(self, col_num: int):
        """Make sure column at given index is visible.

        scrolls to column at given index

        Args:
            col_num: column to scroll to
        """
        if self.model() is None:
            return
        idx = self.model().index(0, col_num)
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

    def scroll_to(self, index, mode: ScrollHintStr = "ensure_visible"):
        if mode not in SCROLL_HINT:
            raise InvalidParamError(mode, SCROLL_HINT)
        self.scrollTo(index, SCROLL_HINT[mode])

    def highlight_when_inactive(self):
        """Highlight items when widget does not have focus."""
        p = gui.Palette()
        p.highlight_inactive()
        self.setPalette(p)

    def set_icon_size(self, size: int | types.SizeType):
        if isinstance(size, tuple):
            size = QtCore.QSize(*size)
        elif isinstance(size, int):
            size = QtCore.QSize(size, size)
        self.setIconSize(size)
