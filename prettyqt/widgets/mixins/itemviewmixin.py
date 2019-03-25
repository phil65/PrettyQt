# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Generator, Any, Optional, List
import logging

from qtpy import QtCore, QtWidgets


SELECTION_MODES = dict(single=QtWidgets.QAbstractItemView.SingleSelection,
                       extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                       multi=QtWidgets.QAbstractItemView.MultiSelection,
                       none=QtWidgets.QAbstractItemView.NoSelection)

logging.basicConfig(level=logging.DEBUG)


class ItemViewMixin(object):

    def __init__(self, *args, **kwargs):
        """
        Custom TreeView for managing the imported data
        """
        self.first_load = True
        super().__init__(*args, **kwargs)
        self.do_sort = True
        self.menu = None
        self.col_vis_restored = False
        self.setObjectName(self.__class__.__name__)
        # visual settings
        # self.setAllColumnsShowFocus(True)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.context_actions = []

    def selectAll(self):
        """
        Override, we dont want to selectAll for too many items for performance reasons
        """
        if self.model() is None:
            return False
        if self.model().rowCount() * self.model().columnCount() > 1_000_000:
            logging.info("Too many cells to select.")
            return False
        super().selectAll()
        return True

    def setModel(self, model):
        """
        delete old selection model explicitely, seems to help with memory usage
        """
        if model is not None:
            model.do_sort = False
        old_sel_model = self.selectionModel()
        super().setModel(model)
        self.setEnabled(model is not None)
        if old_sel_model:
            del old_sel_model
        if model is None:
            return None
        model.do_sort = True
        if self.save_headers and not self.col_vis_restored:
            self.col_vis_restored = True
            self.h_header().load_section_visibility()

    def setup_list_style(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.h_header().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(self.verticalHeader().Fixed)
        self.verticalHeader().setDefaultSectionSize(28)

    def setup_dragdrop_move(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setDropIndicatorShown(True)

    def selected_indexes(self) -> List[QtCore.QModelIndex]:
        """
        returns list of selected indexes in first row
        """
        indexes = (x for x in self.selectedIndexes() if x.column() == 0)
        return sorted(indexes, key=lambda x: x.row())

    def num_selected(self) -> int:
        """
        returns amount of selected rows
        """
        if self.selectionModel() is None:
            return 0
        return len(self.selectionModel().selectedRows())

    def selected_rows(self) -> Generator[int, None, None]:
        """
        returns generator yielding row nums
        """
        return (x.row() for x in self.selected_indexes())

    def selected_data(self) -> Generator[Any, None, None]:
        """
        returns generator yielding selected userData
        """
        return (x.data(self.model().DATA_ROLE)
                for x in self.selected_indexes())

    def current(self) -> Optional[int]:
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex()

    def current_data(self):
        if self.model() is None:
            return None
        role = self.model().DATA_ROLE
        return self.current().data(role)

    def raise_dock(self) -> bool:
        node = self
        while node:
            node = node.parent()
            if isinstance(node, QtWidgets.QDockWidget):
                node.setVisible(True)
                node.raise_()
                return True
        return False

    def jump_to_column(self, col_num: int):
        """
        make sure column at index *col_num is visible
        """
        if self.model() is None:
            return None
        idx = self.model().index(0, col_num)
        self.scrollTo(idx)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.resizeColumnsToContents()
        else:
            self.h_header().resizeSections(self.h_header().Interactive)

    def set_selection_mode(self, mode: str):
        self.setSelectionMode(SELECTION_MODES[mode])

    def add_item(self, item):
        """
        append an item to the list
        """
        if item is None:
            logging.error("Tried to add None")
            return None
        self.model().add_item(item)
        self.scrollToBottom()
        self.raise_dock()
