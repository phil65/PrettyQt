# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QTreeView.__bases__ = (widgets.AbstractItemView,)


class TreeView(QtWidgets.QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.__class__.__name__

        # visual settings
        self.setAnimated(True)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)
        self.setUniformRowHeights(True)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

        # misc
        self.h_header = widgets.HeaderView("horizontal", parent=self)
        self.set_selection_mode("extended")

    @property
    def h_header(self):
        return self.header()

    @h_header.setter
    def h_header(self, header):
        self.setHeader(header)

    def expand_all(self):
        self.expandAll()

    def set_indentation(self, indentation: int):
        self.setIndentation(indentation)

    def setup_list_style(self):
        self.setSelectionBehavior(self.SelectRows)
        self.h_header.setStretchLastSection(True)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.h_header.resizeSections(self.h_header.ResizeToContents)
        else:
            self.h_header.resize_sections("interactive")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = QtWidgets.QMainWindow()
    status_bar = TreeView()
    dlg.show()
    app.exec_()
