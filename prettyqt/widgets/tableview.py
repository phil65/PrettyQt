# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class TableView(QtWidgets.QTableView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def h_header(self):
        return self.horizontalHeader()


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    dlg = widgets.MainWindow()
    status_bar = TableView()
    dlg.show()
    app.exec_()
