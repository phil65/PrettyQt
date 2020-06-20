# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import bidict

VIEW_MODES = bidict(default=QtWidgets.QMdiArea.SubWindowView,
                    tabbed=QtWidgets.QMdiArea.TabbedView)


WINDOW_ORDERS = bidict(creation=QtWidgets.QMdiArea.CreationOrder,
                       stacking=QtWidgets.QMdiArea.StackingOrder,
                       activation=QtWidgets.QMdiArea.ActivationHistoryOrder)

TAB_POSITIONS = bidict(north=QtWidgets.QTabWidget.North,
                       south=QtWidgets.QTabWidget.South,
                       west=QtWidgets.QTabWidget.West,
                       east=QtWidgets.QTabWidget.East)

QtWidgets.QMdiArea.__bases__ = (widgets.AbstractScrollArea,)


class MdiArea(QtWidgets.QMdiArea):

    def __add__(self, other):
        if isinstance(other, QtWidgets.QWidget):
            self.add(other)
            return self

    def set_view_mode(self, mode: str):
        """set view mode for the MDI area

        Valid values are "default", "tabbed"

        Args:
            mode: view mode to use

        Raises:
            ValueError: view mode does not exist
        """
        if mode not in VIEW_MODES:
            raise ValueError("Invalid value for mode.")
        self.setViewMode(VIEW_MODES[mode])

    def get_view_mode(self) -> str:
        """returns current view mode

        Possible values: "default", "tabbed"

        Returns:
            view mode
        """
        return VIEW_MODES.inv[self.viewMode()]

    def set_window_order(self, mode: str):
        """set the window order behaviour for the MDI area

        Valid values are "creation", "stacking", "activation"

        Args:
            mode: window order behaviour to use

        Raises:
            ValueError: window order mode not existing.
        """
        if mode not in WINDOW_ORDERS:
            raise ValueError("Invalid value for mode.")
        self.setActivationOrder(WINDOW_ORDERS[mode])

    def get_window_order(self) -> str:
        """returns current window order

        Possible values: "creation", "stacking", "activation"

        Returns:
            view mode
        """
        return WINDOW_ORDERS.inv[self.activationOrder()]

    def set_tab_position(self, position: str):
        """set tab position for the MDI area

        Valid values are "north", "south", "west", "east"

        Args:
            position: tabs position to use

        Raises:
            ValueError: tab position does not exist
        """
        if position not in TAB_POSITIONS:
            raise ValueError("Invalid value for tab position.")
        self.setTabPosition(TAB_POSITIONS[position])

    def get_tab_position(self) -> str:
        """returns current tab position

        Possible values: "north", "south", "west", "east"

        Returns:
            tab position
        """
        return TAB_POSITIONS.inv[self.tabPosition()]

    def set_background(self, bg_color):
        if isinstance(bg_color, str):
            bg_color = gui.Brush(gui.Color("black"))
        self.setBackground(bg_color)

    def add(self, *item: QtWidgets.QWidget):
        for i in item:
            if not isinstance(i, QtWidgets.QMdiSubWindow):
                widget = widgets.MdiSubWindow()
                widget.setWidget(i)
                self.addSubWindow(widget)
            else:
                self.addSubWindow(i)


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiArea()
    le = widgets.LineEdit("test")
    le2 = widgets.LineEdit("test")
    widget.add(le)
    widget.add(le2)
    widget.show()
    app.exec_()
