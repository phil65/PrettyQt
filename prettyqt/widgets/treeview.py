# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


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

    def h_header(self):
        return self.header()

    def setup_list_style(self):
        self.setSelectionBehavior(self.SelectRows)
        self.h_header().setStretchLastSection(True)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.h_header().resizeSections(self.h_header().ResizeToContents)
        else:
            self.h_header().resize_sections("interactive")


TreeView.__bases__[0].__bases__ = (widgets.AbstractItemView,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = QtWidgets.QMainWindow()
    status_bar = TreeView()
    dlg.show()
    app.exec_()
