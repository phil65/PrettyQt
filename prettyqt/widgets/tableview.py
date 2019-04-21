# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
from prettyqt import gui


TRIGGERS = dict(none=QtWidgets.QAbstractItemView.DoubleClicked,
                double_click=QtWidgets.QAbstractItemView.DoubleClicked,
                edit_key=QtWidgets.QAbstractItemView.EditKeyPressed)

SCROLLBAR_POLICY = dict(always_on=QtCore.Qt.ScrollBarAlwaysOn,
                        always_off=QtCore.Qt.ScrollBarAlwaysOff,
                        as_needed=QtCore.Qt.ScrollBarAsNeeded)

SELECTION_BEHAVIOURS = dict(rows=QtWidgets.QAbstractItemView.SelectRows,
                            columns=QtWidgets.QAbstractItemView.SelectColumns,
                            items=QtWidgets.QAbstractItemView.SelectItems)

SELECTION_MODES = dict(single=QtWidgets.QAbstractItemView.SingleSelection,
                       extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                       multi=QtWidgets.QAbstractItemView.MultiSelection,
                       none=QtWidgets.QAbstractItemView.NoSelection)


class TableView(QtWidgets.QTableView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def h_header(self):
        return self.horizontalHeader()

    def set_horizontal_scrollbar_visibility(self, mode: str):
        self.setHorizontalScrollBarPolicy(SCROLLBAR_POLICY[mode])

    def set_vertical_scrollbar_visibility(self, mode: str):
        self.setVerticalScrollBarPolicy(SCROLLBAR_POLICY[mode])

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


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    dlg = widgets.MainWindow()
    status_bar = TableView()
    dlg.show()
    app.exec_()
