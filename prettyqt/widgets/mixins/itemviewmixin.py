# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import logging
from typing import Any, Generator, List, Optional

from qtpy import QtCore


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

    def setModel(self, model):
        """
        delete old selection model explicitely, seems to help with memory usage
        """
        if model is not None:
            model.do_sort = False
        super().setModel(model)
        self.setEnabled(model is not None)
        if model is None:
            return None
        model.do_sort = True
        if self.save_headers and not self.col_vis_restored:
            self.col_vis_restored = True
            self.h_header().load_section_visibility()

    def setup_list_style(self):
        self.setSelectionBehavior(self.SelectRows)
        self.h_header().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(self.verticalHeader().Fixed)
        self.verticalHeader().setDefaultSectionSize(28)

    def setup_dragdrop_move(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setDropIndicatorShown(True)

    def selected_indexes(self) -> List[QtCore.QModelIndex]:
        """
        returns list of selected indexes in first row
        """
        indexes = (x for x in self.selectedIndexes() if x.column() == 0)
        return sorted(indexes, key=lambda x: x.row())

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

    def current_index(self) -> Optional[int]:
        """returns current index

        Returns:
            current index if available, else None
        """
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex()

    def current_data(self):
        """returns data from current index (UserRole)

        Returns:
            UserRole data from current index if available, else None
        """
        if self.model() is None:
            return None
        role = self.model().DATA_ROLE
        return self.current_index().data(role)

    def add_item(self, item):
        """append an item to the model

        Args:
            item: item to add to model
        """
        if item is None:
            logging.error("Tried to add None")
            return None
        self.model().add_item(item)
        self.scrollToBottom()
        self.raise_dock()
