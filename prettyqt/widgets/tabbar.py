# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore, QtGui


class TabBar(QtWidgets.QTabBar):
    on_detach = QtCore.Signal(int, QtCore.QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setElideMode(QtCore.Qt.ElideRight)
        self.set_remove_behaviour("left_tab")
        self.mouse_cursor = QtGui.QCursor()

    #  Send the on_detach when a tab is double clicked
    def mouseDoubleClickEvent(self, event):
        event.accept()
        self.on_detach.emit(self.tabAt(event.pos()), self.mouse_cursor.pos())

    def set_remove_behaviour(self, mode):
        if mode == "left_tab":
            self.setSelectionBehaviorOnRemove(QtWidgets.QTabBar.SelectLeftTab)


