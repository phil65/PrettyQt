# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QTreeWidget.__bases__ = (widgets.TreeView,)


class TreeWidget(QtWidgets.QTreeWidget):
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TreeWidget()
    widget.show()
    app.exec_()
