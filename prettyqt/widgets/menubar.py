# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class MenuBar(QtWidgets.QMenuBar):

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QAction, QtWidgets.QMenu)):
            self.add_item(other)
            return self

    def add_action(self, action: QtWidgets.QAction):
        return self.addAction(action)

    def add_menu(self, menu: QtWidgets.QMenu):
        return self.addMenu(menu)

    def add_item(self, item):
        if isinstance(item, QtWidgets.QMenu):
            return self.add_menu(item)
        else:
            return self.add_action(item)


MenuBar.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    win = QtWidgets.QMainWindow()
    menu_bar = MenuBar()
    win.setMenuBar(menu_bar)
    win.show()
    app.exec_()
