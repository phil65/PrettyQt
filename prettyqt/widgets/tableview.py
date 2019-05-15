# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class TableView(QtWidgets.QTableView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(self.__class__.__name__)
        self.setHorizontalHeader(widgets.HeaderView(parent=self))
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

    def h_header(self):
        return self.horizontalHeader()

    def setup_list_style(self):
        self.setSelectionBehavior(self.SelectRows)
        self.h_header().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(self.verticalHeader().Fixed)
        self.verticalHeader().setDefaultSectionSize(28)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.resizeColumnsToContents()
        else:
            self.h_header().resizeSections(self.h_header().Interactive)


TableView.__bases__[0].__bases__ = (widgets.AbstractItemView,)

if __name__ == "__main__":
    app = widgets.app()
    dlg = widgets.MainWindow()
    status_bar = TableView()
    dlg.show()
    app.exec_()
