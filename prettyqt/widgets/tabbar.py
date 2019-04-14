# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtGui, QtWidgets

ELIDE_MODES = dict(left=QtCore.Qt.ElideLeft,
                   right=QtCore.Qt.ElideRight,
                   middle=QtCore.Qt.ElideMiddle,
                   none=QtCore.Qt.ElideNone)

SELECTION_MODES = dict(left_tab=QtWidgets.QTabBar.SelectLeftTab,
                       right_tab=QtWidgets.QTabBar.SelectRightTab,
                       previous_tab=QtWidgets.QTabBar.SelectPreviousTab)

SHAPES = dict(rounded_north=QtWidgets.QTabBar.RoundedNorth,
              rounded_south=QtWidgets.QTabBar.RoundedSouth,
              rounded_west=QtWidgets.QTabBar.RoundedWest,
              rounded_east=QtWidgets.QTabBar.RoundedEast,
              triangular_north=QtWidgets.QTabBar.TriangularNorth,
              triangular_south=QtWidgets.QTabBar.TriangularSouth,
              triangular_west=QtWidgets.QTabBar.TriangularWest,
              triangular_east=QtWidgets.QTabBar.TriangularEast)


class TabBar(QtWidgets.QTabBar):
    on_detach = QtCore.Signal(int, QtCore.QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.set_elide_mode("right")
        self.set_remove_behaviour("left_tab")
        self.mouse_cursor = QtGui.QCursor()

    #  Send the on_detach when a tab is double clicked
    def mouseDoubleClickEvent(self, event):
        event.accept()
        self.on_detach.emit(self.tabAt(event.pos()), self.mouse_cursor.pos())

    def set_icon_size(self, size: int):
        self.setIconSize(QtCore.QSize(size, size))

    def set_tab_button(self, index, widget, position: str = "left"):
        if position == "left":
            self.setTabButton(index, QtWidgets.QTabBar.LeftSide, widget)
        else:
            self.setTabButton(index, QtWidgets.QTabBar.RightSide, widget)

    def set_remove_behaviour(self, mode: str):
        """sets the remove hehaviour

        What tab should be set as current when removeTab is called
        if the removed tab is also the current tab.
        Possible values: left, right, previous
        Args:
            mode: new remove behaviour
        """
        if mode not in SELECTION_MODES:
            raise ValueError("Mode not available")
        self.setSelectionBehaviorOnRemove(SELECTION_MODES[mode])

    def set_elide_mode(self, mode: str):
        if mode not in ELIDE_MODES:
            raise ValueError("Mode not available")
        self.setElideMode(ELIDE_MODES[mode])
