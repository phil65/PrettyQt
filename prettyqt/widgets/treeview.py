# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import logging
from typing import Any, Generator, List, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets

SELECTION_MODES = dict(single=QtWidgets.QAbstractItemView.SingleSelection,
                       extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                       multi=QtWidgets.QAbstractItemView.MultiSelection,
                       none=QtWidgets.QAbstractItemView.NoSelection)

SELECTION_BEHAVIOURS = dict(rows=QtWidgets.QAbstractItemView.SelectRows,
                            items=QtWidgets.QAbstractItemView.SelectItems,
                            columns=QtWidgets.QAbstractItemView.SelectColumns)

SCROLLBAR_POLICY = dict(always_on=QtCore.Qt.ScrollBarAlwaysOn,
                        always_off=QtCore.Qt.ScrollBarAlwaysOff,
                        as_needed=QtCore.Qt.ScrollBarAsNeeded)


class TreeView(QtWidgets.QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(self.__class__.__name__)

        # visual settings
        self.setAnimated(True)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)
        self.setUniformRowHeights(True)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

        # misc
        self.setHeader(widgets.HeaderView(parent=self))
        self.set_selection_mode("extended")

    def setModel(self, model):
        """
        delete old selection model explicitely, seems to help with memory usage
        """
        old_sel_model = self.selectionModel()
        super().setModel(model)
        if old_sel_model:
            del old_sel_model

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

    def h_header(self):
        return self.header()

    def current_index(self) -> Optional[int]:
        if self.selectionModel() is None:
            return None
        return self.selectionModel().currentIndex()

    def current_data(self):
        if self.model() is None:
            return None
        return self.current_index().data(QtCore.Qt.UserRole)

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
        return (x.data(self.model().NAME_ROLE)
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
        return (x.data(self.model().QtCore.Qt.UserRole)
                for x in self.selected_indexes())

    def setup_list_style(self):
        self.setSelectionBehavior(self.SelectRows)
        self.h_header().setStretchLastSection(True)

    def setup_dragdrop_move(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setDropIndicatorShown(True)

    def set_horizontal_scrollbar_visibility(self, mode: str):
        self.setHorizontalScrollBarPolicy(SCROLLBAR_POLICY[mode])

    def set_vertical_scrollbar_visibility(self, mode: str):
        self.setVerticalScrollBarPolicy(SCROLLBAR_POLICY[mode])

    def set_horizontal_scrollbar_width(self, width):
        stylesheet = f"QScrollBar:horizontal {{height: {width}px;}}"
        self.horizontalScrollBar().setStyleSheet(stylesheet)

    def set_vertical_scrollbar_width(self, width):
        stylesheet = f"QScrollBar:vertical {{height: {width}px;}}"
        self.verticalScrollBar().setStyleSheet(stylesheet)

    def set_selection_mode(self, mode: str):
        """set selection mode for given item view

        Allowed values are "single", "extended", "multi" or "none"

        Args:
            mode: selection mode to use

        Raises:
            ValueError: mode does not exist
        """
        if mode not in SELECTION_MODES:
            raise ValueError("Format must be either 'single', 'extended',"
                             "'multi' or 'None'")
        self.setSelectionMode(SELECTION_MODES[mode])

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

    def num_selected(self) -> int:
        """returns amount of selected rows

        Returns:
            amount of selected rows
            int
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

    def highlight_when_inactive(self):
        """also highlight items when widget does not have focus
        """
        p = gui.Palette()
        p.highlight_inactive()
        self.setPalette(p)

    def raise_dock(self) -> bool:
        node = self
        while node:
            node = node.parent()
            if isinstance(node, QtWidgets.QDockWidget):
                node.setVisible(True)
                node.raise_()
                return True
        return False

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.h_header().resizeSections(self.h_header().ResizeToContents)
        else:
            self.h_header().resize_sections("interactive")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = QtWidgets.QMainWindow()
    status_bar = TreeView()
    dlg.show()
    app.exec_()
