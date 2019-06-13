# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from prettyqt import widgets


QtWidgets.QColumnView.__bases__ = (widgets.AbstractItemView,)


class ColumnView(QtWidgets.QColumnView):
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = QtWidgets.QMainWindow()
    status_bar = ColumnView()
    dlg.show()
    app.exec_()
