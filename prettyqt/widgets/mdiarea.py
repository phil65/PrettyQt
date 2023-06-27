from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import bidict, colors, datatypes


ViewModeStr = Literal["default", "tabbed"]

VIEW_MODE: bidict[ViewModeStr, QtWidgets.QMdiArea.ViewMode] = bidict(
    default=QtWidgets.QMdiArea.ViewMode.SubWindowView,
    tabbed=QtWidgets.QMdiArea.ViewMode.TabbedView,
)

WindowOrderStr = Literal["creation", "stacking", "activation_history"]

WINDOW_ORDER: bidict[WindowOrderStr, QtWidgets.QMdiArea.WindowOrder] = bidict(
    creation=QtWidgets.QMdiArea.WindowOrder.CreationOrder,
    stacking=QtWidgets.QMdiArea.WindowOrder.StackingOrder,
    activation_history=QtWidgets.QMdiArea.WindowOrder.ActivationHistoryOrder,
)

TabPositionStr = Literal["north", "south", "west", "east"]

TAB_POSITION: bidict[TabPositionStr, QtWidgets.QTabWidget.TabPosition] = bidict(
    north=QtWidgets.QTabWidget.TabPosition.North,
    south=QtWidgets.QTabWidget.TabPosition.South,
    west=QtWidgets.QTabWidget.TabPosition.West,
    east=QtWidgets.QTabWidget.TabPosition.East,
)


class MdiArea(widgets.AbstractScrollAreaMixin, QtWidgets.QMdiArea):
    def __add__(self, other: QtWidgets.QWidget):
        self.add(other)
        return self

    def set_view_mode(self, mode: ViewModeStr | QtWidgets.QMdiArea.ViewMode):
        """Set view mode for the MDI area.

        Args:
            mode: view mode to use
        """
        self.setViewMode(VIEW_MODE.get_enum_value(mode))

    def get_view_mode(self) -> ViewModeStr:
        """Return current view mode.

        Returns:
            view mode
        """
        return VIEW_MODE.inverse[self.viewMode()]

    def set_window_order(self, mode: WindowOrderStr | QtWidgets.QMdiArea.WindowOrder):
        """Set the window order behaviour for the MDI area.

        Args:
            mode: window order behaviour to use
        """
        self.setActivationOrder(WINDOW_ORDER.get_enum_value(mode))

    def get_window_order(self) -> WindowOrderStr:
        """Return current window order.

        Returns:
            view mode
        """
        return WINDOW_ORDER.inverse[self.activationOrder()]

    def set_tab_position(
        self, position: TabPositionStr | QtWidgets.QTabWidget.TabPosition
    ):
        """Set tab position for the MDI area.

        Args:
            position: tabs position to use
        """
        self.setTabPosition(TAB_POSITION.get_enum_value(position))

    def get_tab_position(self) -> TabPositionStr:
        """Return current tab position.

        Returns:
            tab position
        """
        return TAB_POSITION.inverse[self.tabPosition()]

    def set_background(
        self,
        brush_or_color: datatypes.ColorAndBrushType,
        pattern: constants.BrushStyleStr = "solid",
    ):
        if isinstance(brush_or_color, QtGui.QBrush):
            brush = brush_or_color
        else:
            color = colors.get_color(brush_or_color)
            brush = gui.Brush(color, constants.BRUSH_STYLE[pattern])
        self.setBackground(brush)

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def add(self, *item: QtWidgets.QWidget):
        for i in item:
            self.add_subwindow(i)

    def add_subwindow(self, widget: QtWidgets.QWidget) -> QtWidgets.QMdiSubWindow:
        if not isinstance(widget, QtWidgets.QMdiSubWindow):
            window = widgets.MdiSubWindow()
            window.setWidget(widget)
            self.addSubWindow(window)
            return window
        else:
            return self.addSubWindow(widget)


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiArea()
    widget.set_background("green", "cross")
    le = widgets.LineEdit("test")
    le2 = widgets.LineEdit("test")
    widget.add(le)
    widget.add(le2)
    widget.show()
    app.exec()
