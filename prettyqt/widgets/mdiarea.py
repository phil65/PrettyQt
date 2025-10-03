from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from prettyqt import constants, gui, widgets
from prettyqt.utils import bidict, colors


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


ViewModeStr = Literal["default", "tabbed"]

VIEW_MODE: bidict[ViewModeStr, widgets.QMdiArea.ViewMode] = bidict(
    default=widgets.QMdiArea.ViewMode.SubWindowView,
    tabbed=widgets.QMdiArea.ViewMode.TabbedView,
)

WindowOrderStr = Literal["creation", "stacking", "activation_history"]

WINDOW_ORDER: bidict[WindowOrderStr, widgets.QMdiArea.WindowOrder] = bidict(
    creation=widgets.QMdiArea.WindowOrder.CreationOrder,
    stacking=widgets.QMdiArea.WindowOrder.StackingOrder,
    activation_history=widgets.QMdiArea.WindowOrder.ActivationHistoryOrder,
)

TabPositionStr = Literal["north", "south", "west", "east"]

TAB_POSITION: bidict[TabPositionStr, widgets.QTabWidget.TabPosition] = bidict(
    north=widgets.QTabWidget.TabPosition.North,
    south=widgets.QTabWidget.TabPosition.South,
    west=widgets.QTabWidget.TabPosition.West,
    east=widgets.QTabWidget.TabPosition.East,
)


class MdiArea(widgets.AbstractScrollAreaMixin, widgets.QMdiArea):
    """Area in which MDI windows are displayed."""

    def __add__(self, other: widgets.QWidget):
        self.add(other)
        return self

    def set_view_mode(self, mode: ViewModeStr | widgets.QMdiArea.ViewMode):
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

    def set_window_order(self, mode: WindowOrderStr | widgets.QMdiArea.WindowOrder):
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

    def set_tab_position(self, position: TabPositionStr | widgets.QTabWidget.TabPosition):
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
        if isinstance(brush_or_color, gui.QBrush):
            brush = brush_or_color
        else:
            color = colors.get_color(brush_or_color)
            brush = gui.Brush(color, constants.BRUSH_STYLE[pattern])
        self.setBackground(brush)

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def add(self, *item: widgets.QWidget):
        for i in item:
            self.add_subwindow(i)

    def add_subwindow(self, widget: widgets.QWidget) -> widgets.QMdiSubWindow:
        if not isinstance(widget, widgets.QMdiSubWindow):
            window = widgets.MdiSubWindow()
            window.setWidget(widget)
            self.addSubWindow(window)
            return window
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
