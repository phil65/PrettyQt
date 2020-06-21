# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import functools
import logging
import operator
from typing import Any, Generator, List, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import constants, gui, widgets
from prettyqt.utils import bidict

TRIGGERS = bidict(none=QtWidgets.QAbstractItemView.NoEditTriggers,
                  double_click=QtWidgets.QAbstractItemView.DoubleClicked,
                  edit_key=QtWidgets.QAbstractItemView.EditKeyPressed)

SELECTION_BEHAVIOURS = bidict(rows=QtWidgets.QAbstractItemView.SelectRows,
                              columns=QtWidgets.QAbstractItemView.SelectColumns,
                              items=QtWidgets.QAbstractItemView.SelectItems)

SELECTION_MODES = bidict(single=QtWidgets.QAbstractItemView.SingleSelection,
                         extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                         multi=QtWidgets.QAbstractItemView.MultiSelection,
                         none=QtWidgets.QAbstractItemView.NoSelection)

SCROLL_MODES = bidict(item=QtWidgets.QAbstractItemView.ScrollPerItem,
                      pixel=QtWidgets.QAbstractItemView.ScrollPerPixel)

QtWidgets.QAbstractItemView.__bases__ = (widgets.AbstractScrollArea,)


class AbstractItemView(QtWidgets.QAbstractItemView):

    def __len__(self):
        if self.model() is not None:
            return self.model().rowCount()
        return 0

    def selectAll(self):
        """
        Override, we dont want to selectAll for too many items for performance reasons
        """
        if self.model() is None:
            return None
        if self.model().rowCount() * self.model().columnCount() > 1_000_000:
            logging.info("Too many cells to select.")
            return None
        super().selectAll()

    def setModel(self, model):
        """
        delete old selection model explicitely, seems to help with memory usage
        """
        old_model = self.model()
        old_sel_model = self.selectionModel()
        if old_model is not None or model is not None:
            super().setModel(model)
        # if old_model:
        #     old_model.deleteLater()
        #     del old_model
        if old_sel_model:
            old_sel_model.deleteLater()
            del old_sel_model

    def set_model(self, model):
        self.setModel(model)

    def set_delegate(self,
                     delegate,
                     column: Optional[int] = None,
                     row: Optional[int] = None,
                     persistent: bool = False):
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
        """
        select all items from list (deselect when all selected)
        """
        if self.selectionModel() is None:
            return None
        if self.selectionModel().hasSelection():
            self.clearSelection()
        else:
            self.selectAll()

    def set_table_color(self, color: str):
        self.setStyleSheet(f"QHeaderView::section {{ background-color:{color} }}")

    def current_index(self) -> Optional[int]:
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex()

    def current_data(self):
        if self.model() is None:
            return None
        return self.current_index().data(QtCore.Qt.UserRole)

    def current_row(self) -> Optional[int]:
        return self.current_index().row()

    def current_column(self) -> Optional[int]:
        return self.current_index().column()

    def selected_indexes(self) -> List[QtCore.QModelIndex]:
        """
        returns list of selected indexes in first row
        """
        indexes = (x for x in self.selectedIndexes() if x.column() == 0)
        return sorted(indexes, key=lambda x: x.row())

    def selected_names(self) -> Generator[Any, None, None]:
        """
        returns generator yielding item names
        """
        return (x.data(constants.NAME_ROLE)
                for x in self.selected_indexes())

    def selected_rows(self) -> Generator[int, None, None]:
        """
        returns generator yielding row nums
        """
        return (x.row() for x in self.selected_indexes())

    def selected_data(self) -> Generator[Any, None, None]:
        """
        returns generator yielding selected userData
        """
        return (x.data(constants.USER_ROLE)
                for x in self.selected_indexes())

    def setup_dragdrop_move(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setDropIndicatorShown(True)

    def set_edit_triggers(self, *triggers: Optional[str]):
        triggers = ["none" if t is None else t for t in triggers]
        for item in triggers:
            if item not in TRIGGERS:
                raise ValueError("trigger type not available")
        flags = functools.reduce(operator.ior, [TRIGGERS[t] for t in triggers])
        self.setEditTriggers(flags)

    def get_edit_triggers(self) -> list:
        return [k for k, v in TRIGGERS.items() if v & self.editTriggers()]

    def set_selection_behaviour(self, behaviour: str):
        """set selection behaviour for given item view

        Allowed values are "rows", "columns", "items"

        Args:
            behaviour: selection behaviour to use

        Raises:
            ValueError: behaviour does not exist
        """
        if behaviour not in SELECTION_BEHAVIOURS:
            raise ValueError("invalid selection behaviour")
        self.setSelectionBehavior(SELECTION_BEHAVIOURS[behaviour])

    def get_selection_behaviour(self) -> str:
        """returns current selection behaviour

        Possible values: "rows", "columns", "items"

        Returns:
            selection behaviour
        """
        return SELECTION_BEHAVIOURS.inv[self.selectionBehavior()]

    def set_selection_mode(self, mode: Optional[str]):
        """set selection mode for given item view

        Allowed values are "single", "extended", "multi" or "none"

        Args:
            mode: selection mode to use

        Raises:
            ValueError: mode does not exist
        """
        if mode is None:
            mode = "none"
        if mode not in SELECTION_MODES:
            raise ValueError("Format must be either 'single', 'extended',"
                             "'multi' or 'None'")
        self.setSelectionMode(SELECTION_MODES[mode])

    def get_selection_mode(self) -> str:
        """returns current selection mode

        Possible values: "single", "extended", "multi" or "none"

        Returns:
            selection mode
        """
        return SELECTION_MODES.inv[self.selectionMode()]

    def set_scroll_mode(self, mode: str):
        """sets the scroll mode for both directions

        possible values are "item", "pixel"

        Args:
            mode: mode to set

        Raises:
            ValueError: invalid scroll mode
        """
        if mode not in SCROLL_MODES:
            raise ValueError("Invalid scroll mode")
        self.setHorizontalScrollMode(SCROLL_MODES[mode])
        self.setVerticalScrollMode(SCROLL_MODES[mode])

    def set_horizontal_scroll_mode(self, mode: str):
        """sets the horizontal scroll mode

        possible values are "item", "pixel"

        Args:
            mode: mode to set

        Raises:
            ValueError: invalid scroll mode
        """
        if mode not in SCROLL_MODES:
            raise ValueError("Invalid scroll mode")
        self.setHorizontalScrollMode(SCROLL_MODES[mode])

    def set_vertical_scroll_mode(self, mode: str):
        """sets the vertical scroll mode

        possible values are "item", "pixel"

        Args:
            mode: mode to set

        Raises:
            ValueError: invalid scroll mode
        """
        if mode not in SCROLL_MODES:
            raise ValueError("Invalid scroll mode")
        self.setVerticalScrollMode(SCROLL_MODES[mode])

    def num_selected(self) -> int:
        """returns amount of selected rows

        Returns:
            amount of selected rows
        """
        if self.selectionModel() is None:
            return 0
        return len(self.selectionModel().selectedRows())

    def jump_to_column(self, col_num: int):
        """make sure column at given index is visible

        scrolls to column at given index

        Args:
            col_num: column to scroll to
        """
        if self.model() is None:
            return None
        idx = self.model().index(0, col_num)
        self.scrollTo(idx)

    def scroll_to_top(self):
        """override to use abstractitemview-way of scrolling to top
        """
        self.scrollToTop()

    def scroll_to_bottom(self):
        """override to use abstractitemview-way of scrolling to bottom
        """
        self.scrollToBottom()

    def select_last_row(self):
        idx = self.model().createIndex(self.model().rowCount() - 1, 0)
        self.setCurrentIndex(idx)

    def highlight_when_inactive(self):
        """also highlight items when widget does not have focus
        """
        p = gui.Palette()
        p.highlight_inactive()
        self.setPalette(p)
