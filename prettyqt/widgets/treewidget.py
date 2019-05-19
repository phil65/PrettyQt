# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class TreeWidget(QtWidgets.QTreeWidget):
    pass


TreeWidget.__bases__[0].__bases__ = (widgets.TreeView,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TreeWidget()
    widget.show()
    app.exec_()
