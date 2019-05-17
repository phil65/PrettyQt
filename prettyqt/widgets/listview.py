# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from prettyqt import widgets


class ListView(QtWidgets.QListView):
    pass


ListView.__bases__[0].__bases__ = (widgets.AbstractItemView,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = QtWidgets.QMainWindow()
    status_bar = ListView()
    dlg.show()
    app.exec_()
