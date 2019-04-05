# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class StatusBar(QtWidgets.QStatusBar):

    def add_action(self, action):
        self.addAction(action)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = QtWidgets.QMainWindow()
    status_bar = StatusBar()
    dlg.setStatusBar(status_bar)
    dlg.show()
    app.exec_()
