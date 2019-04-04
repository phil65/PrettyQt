# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class MenuBar(QtWidgets.QMenuBar):

    def add_action(self, action):
        self.addAction(action)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    menu_bar = MenuBar()
    win.setMenuBar(menu_bar)
    win.show()
    app.exec_()
