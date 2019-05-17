# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict
from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import widgets

ELIDE_MODES = bidict(dict(left=QtCore.Qt.ElideLeft,
                          right=QtCore.Qt.ElideRight,
                          middle=QtCore.Qt.ElideMiddle,
                          none=QtCore.Qt.ElideNone))

REMOVE_BEHAVIOURS = bidict(dict(left_tab=QtWidgets.QTabBar.SelectLeftTab,
                                right_tab=QtWidgets.QTabBar.SelectRightTab,
                                previous_tab=QtWidgets.QTabBar.SelectPreviousTab))

SHAPES = bidict(dict(rounded_north=QtWidgets.QTabBar.RoundedNorth,
                     rounded_south=QtWidgets.QTabBar.RoundedSouth,
                     rounded_west=QtWidgets.QTabBar.RoundedWest,
                     rounded_east=QtWidgets.QTabBar.RoundedEast,
                     triangular_north=QtWidgets.QTabBar.TriangularNorth,
                     triangular_south=QtWidgets.QTabBar.TriangularSouth,
                     triangular_west=QtWidgets.QTabBar.TriangularWest,
                     triangular_east=QtWidgets.QTabBar.TriangularEast))

POSITIONS = dict(left=QtWidgets.QTabBar.LeftSide,
                 right=QtWidgets.QTabBar.RightSide)


class TabBar(QtWidgets.QTabBar):
    on_detach = QtCore.Signal(int, QtCore.QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.set_elide_mode("right")
        self.set_remove_behaviour("left_tab")
        self.mouse_cursor = QtGui.QCursor()

    def __getitem__(self, index):
        return self.tabButton(index[0], POSITIONS[index[1]])

    def __setitem__(self, index, value):
        self.set_tab(index[0], index[1], value)

    def __getstate__(self):
        return dict(movable=self.isMovable(),
                    document_mode=self.documentMode(),
                    current_index=self.currentIndex(),
                    # shape=self.shape(),
                    draw_base=self.drawBase(),
                    elide_mode=self.get_elide_mode(),
                    icon_size=self.iconSize())

    def __setstate__(self, state):
        self.__init__()
        self.setDocumentMode(state.get("document_mode", False))
        self.setMovable(state.get("movable", False))
        # self.setShape(state.get("shape", "rounded"))
        self.setIconSize(state["icon_size"])
        self.setDrawBase(state.get("draw_base"))
        self.set_elide_mode(state.get("elide_mode"))
        self.setCurrentIndex(state.get("index", 0))

    #  Send the on_detach when a tab is double clicked
    def mouseDoubleClickEvent(self, event):
        event.accept()
        self.on_detach.emit(self.tabAt(event.pos()), self.mouse_cursor.pos())

    def set_icon_size(self, size: int):
        self.setIconSize(QtCore.QSize(size, size))

    def set_tab(self, index: int, position, widget):
        self.setTabButton(index, POSITIONS[position], widget)

    def set_remove_behaviour(self, mode: str):
        """sets the remove hehaviour

        What tab should be set as current when removeTab is called
        if the removed tab is also the current tab.
        Possible values: left, right, previous
        Args:
            mode: new remove behaviour
        """
        if mode not in REMOVE_BEHAVIOURS:
            raise ValueError("Mode not available")
        self.setSelectionBehaviorOnRemove(REMOVE_BEHAVIOURS[mode])

    def get_remove_behaviour(self) -> str:
        return REMOVE_BEHAVIOURS.inv[self.selectionBehaviorOnRemove()]

    def set_elide_mode(self, mode: str):
        if mode not in ELIDE_MODES:
            raise ValueError("Mode not available")
        self.setElideMode(ELIDE_MODES[mode])

    def get_elide_mode(self) -> str:
        return ELIDE_MODES.inv[self.elideMode()]


TabBar.__bases__[0].__bases__ = (widgets.Widget,)
