# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets

TRIGGERS = dict(none=QtWidgets.QAbstractItemView.DoubleClicked,
                double_click=QtWidgets.QAbstractItemView.DoubleClicked,
                edit_key=QtWidgets.QAbstractItemView.EditKeyPressed)

SCROLLBAR_POLICY = dict(always_on=QtCore.Qt.ScrollBarAlwaysOn,
                        always_off=QtCore.Qt.ScrollBarAlwaysOff,
                        as_needed=QtCore.Qt.ScrollBarAsNeeded)

SELECTION_BEHAVIOURS = dict(rows=QtWidgets.QAbstractItemView.SelectRows,
                            columns=QtWidgets.QAbstractItemView.SelectColumns,
                            items=QtWidgets.QAbstractItemView.SelectItems)


class TableView(QtWidgets.QTableView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def h_header(self):
        return self.horizontalHeader()

    def set_horizontal_scrollbar_visibility(self, mode):
        self.setHorizontalScrollBarPolicy(SCROLLBAR_POLICY[mode])

    def set_selection_behaviour(self, mode):
        self.setSelectionBehaviour(SELECTION_BEHAVIOURS[mode])


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    dlg = widgets.MainWindow()
    status_bar = TableView()
    dlg.show()
    app.exec_()
