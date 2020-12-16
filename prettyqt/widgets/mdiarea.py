from typing import Literal, Union

from qtpy import QtGui, QtWidgets

from prettyqt import constants, gui, widgets
from prettyqt.utils import InvalidParamError, bidict, colors


VIEW_MODE = bidict(
    default=QtWidgets.QMdiArea.SubWindowView, tabbed=QtWidgets.QMdiArea.TabbedView
)

ViewModeStr = Literal["default", "tabbed"]

WINDOW_ORDER = bidict(
    creation=QtWidgets.QMdiArea.CreationOrder,
    stacking=QtWidgets.QMdiArea.StackingOrder,
    activation_history=QtWidgets.QMdiArea.ActivationHistoryOrder,
)

WindowOrderStr = Literal["creation", "stacking", "activation_history"]

TAB_POSITION = bidict(
    north=QtWidgets.QTabWidget.North,
    south=QtWidgets.QTabWidget.South,
    west=QtWidgets.QTabWidget.West,
    east=QtWidgets.QTabWidget.East,
)

TabPositionStr = Literal["north", "south", "west", "east"]

QtWidgets.QMdiArea.__bases__ = (widgets.AbstractScrollArea,)


class MdiArea(QtWidgets.QMdiArea):
    def __add__(self, other):
        if isinstance(other, QtWidgets.QWidget):
            self.add(other)
            return self

    def serialize_fields(self):
        return dict(
            view_mode=self.get_view_mode(),
            window_order=self.get_window_order(),
            tab_position=self.get_tab_position(),
            background=self.get_background(),
            document_mode=self.documentMode(),
        )

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
        brush_or_color: Union[QtGui.QBrush, colors.ColorType],
        pattern: str = "solid",
    ):
        if isinstance(brush_or_color, QtGui.QBrush):
            brush = brush_or_color
        else:
            pattern = constants.PATTERN[pattern]
            color = colors.get_color(brush_or_color)
            brush = gui.Brush(color, pattern)
        self.setBackground(brush)

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

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
    widget.set_background("green", "cross")
    le = widgets.LineEdit("test")
    le2 = widgets.LineEdit("test")
    widget.add(le)
    widget.add(le2)
    widget.show()
    app.main_loop()
