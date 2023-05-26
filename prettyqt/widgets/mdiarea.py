from __future__ import annotations

from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, colors, datatypes


VIEW_MODE = bidict(
    default=QtWidgets.QMdiArea.ViewMode.SubWindowView,
    tabbed=QtWidgets.QMdiArea.ViewMode.TabbedView,
)

ViewModeStr = Literal["default", "tabbed"]

WINDOW_ORDER = bidict(
    creation=QtWidgets.QMdiArea.WindowOrder.CreationOrder,
    stacking=QtWidgets.QMdiArea.WindowOrder.StackingOrder,
    activation_history=QtWidgets.QMdiArea.WindowOrder.ActivationHistoryOrder,
)

WindowOrderStr = Literal["creation", "stacking", "activation_history"]

TAB_POSITION = bidict(
    north=QtWidgets.QTabWidget.TabPosition.North,
    south=QtWidgets.QTabWidget.TabPosition.South,
    west=QtWidgets.QTabWidget.TabPosition.West,
    east=QtWidgets.QTabWidget.TabPosition.East,
)

TabPositionStr = Literal["north", "south", "west", "east"]


class MdiArea(widgets.AbstractScrollAreaMixin, QtWidgets.QMdiArea):
    def __add__(self, other: QtWidgets.QWidget):
        self.add(other)
        return self

    def set_view_mode(self, mode: ViewModeStr):
        """Set view mode for the MDI area.

        Args:
            mode: view mode to use

        Raises:
            InvalidParamError: view mode does not exist
        """
        if mode not in VIEW_MODE:
            raise InvalidParamError(mode, VIEW_MODE)
        self.setViewMode(VIEW_MODE[mode])

    def get_view_mode(self) -> ViewModeStr:
        """Return current view mode.

        Returns:
            view mode
        """
        return VIEW_MODE.inverse[self.viewMode()]

    def set_window_order(self, mode: WindowOrderStr):
        """Set the window order behaviour for the MDI area.

        Args:
            mode: window order behaviour to use

        Raises:
            InvalidParamError: window order mode not existing.
        """
        if mode not in WINDOW_ORDER:
            raise InvalidParamError(mode, WINDOW_ORDER)
        self.setActivationOrder(WINDOW_ORDER[mode])

    def get_window_order(self) -> WindowOrderStr:
        """Return current window order.

        Returns:
            view mode
        """
        return WINDOW_ORDER.inverse[self.activationOrder()]

    def set_tab_position(self, position: TabPositionStr):
        """Set tab position for the MDI area.

        Args:
            position: tabs position to use

        Raises:
            InvalidParamError: tab position does not exist
        """
        if position not in TAB_POSITION:
            raise InvalidParamError(position, TAB_POSITION)
        self.setTabPosition(TAB_POSITION[position])

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
    print(widget.get_properties())
    widget.add(le2)
    widget.show()
    app.main_loop()
