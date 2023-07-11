from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import bidict, datatypes


RemoveBehaviourStr = Literal["left_tab", "right_tab", "previous_tab"]

REMOVE_BEHAVIOUR: bidict[RemoveBehaviourStr, widgets.QTabBar.SelectionBehavior] = bidict(
    left_tab=widgets.QTabBar.SelectionBehavior.SelectLeftTab,
    right_tab=widgets.QTabBar.SelectionBehavior.SelectRightTab,
    previous_tab=widgets.QTabBar.SelectionBehavior.SelectPreviousTab,
)

ShapeStr = Literal[
    "rounded_north",
    "rounded_south",
    "rounded_west",
    "rounded_east",
    "triangular_north",
    "triangular_south",
    "triangular_west",
    "triangular_east",
]

SHAPE: bidict[ShapeStr, widgets.QTabBar.Shape] = bidict(
    rounded_north=widgets.QTabBar.Shape.RoundedNorth,
    rounded_south=widgets.QTabBar.Shape.RoundedSouth,
    rounded_west=widgets.QTabBar.Shape.RoundedWest,
    rounded_east=widgets.QTabBar.Shape.RoundedEast,
    triangular_north=widgets.QTabBar.Shape.TriangularNorth,
    triangular_south=widgets.QTabBar.Shape.TriangularSouth,
    triangular_west=widgets.QTabBar.Shape.TriangularWest,
    triangular_east=widgets.QTabBar.Shape.TriangularEast,
)

PositionStr = Literal["left", "right"]

POSITIONS: bidict[PositionStr, widgets.QTabBar.ButtonPosition] = bidict(
    left=widgets.QTabBar.ButtonPosition.LeftSide,
    right=widgets.QTabBar.ButtonPosition.RightSide,
)


class TabBarWrapper:
    def __init__(self, indexer, widget: widgets.QTabBar):
        self._widget = widget
        self._range = (
            range(
                indexer.start or 0,
                indexer.stop or self._widget.count(),
                indexer.step or 1,
            )
            if isinstance(indexer, slice)
            else range(indexer, indexer + 1)
        )

    def __getattr__(self, val: str):
        method = self._widget.__getattr__(val)

        if len(self._range) == 1:

            def fn(*args, **kwargs):
                return method(self._range.start, *args, **kwargs)

            return fn

        def fn(*args, **kwargs):
            return [method(i, *args, **kwargs) for i in self._range]

        return fn


class TabBarMixin(widgets.WidgetMixin):
    tab_doubleclicked = core.Signal(int, core.QPoint)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.set_elide_mode("right")
        self.set_selection_behavior_on_remove("left_tab")

    def __getitem__(self, index: int | slice):
        return TabBarWrapper(index, self)

    def __setitem__(self, index: tuple[int, PositionStr], value: widgets.QWidget | None):
        self.set_tab(index[0], index[1], value)

    def get_tab_button(
        self, index: int, position: PositionStr | widgets.QTabBar.ButtonPosition
    ) -> widgets.QWidget:
        return self.tabButton(index[0], POSITIONS.get_enum_value(index[1]))

    #  Send the tab_doubleclicked when a tab is double clicked
    def mouseDoubleClickEvent(self, event):
        event.accept()
        tab = self.tabAt(event.position().toPoint())
        pos = gui.QCursor.pos()
        self.tab_doubleclicked.emit(tab, pos)

    def set_icon_size(self, size: datatypes.SizeType):
        """Set size of the icons."""
        self.setIconSize(datatypes.to_size(size))

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def set_tab(
        self,
        index: int,
        position: PositionStr | widgets.QTabBar.ButtonPosition,
        widget: widgets.QWidget | None,
    ) -> None:
        self.setTabButton(index, POSITIONS.get_enum_value(position), widget)

    def set_selection_behavior_on_remove(
        self, mode: RemoveBehaviourStr | widgets.QTabBar.SelectionBehavior
    ) -> None:
        """Set the remove hehaviour.

        What tab should be set as current when removeTab is called
        if the removed tab is also the current tab.

        Args:
            mode: new remove behaviour
        """
        self.setSelectionBehaviorOnRemove(REMOVE_BEHAVIOUR.get_enum_value(mode))

    def get_remove_behaviour(self) -> RemoveBehaviourStr:
        """Return remove behaviour.

        Returns:
            remove behaviour
        """
        return REMOVE_BEHAVIOUR.inverse[self.selectionBehaviorOnRemove()]

    def set_elide_mode(
        self, mode: constants.TextElideModeStr | constants.TextElideMode
    ) -> None:
        """Set elide mode.

        Args:
            mode: elide mode to use
        """
        self.setElideMode(constants.TEXT_ELIDE_MODE.get_enum_value(mode))

    def get_elide_mode(self) -> constants.TextElideModeStr:
        """Return elide mode.

        Returns:
            elide mode
        """
        return constants.TEXT_ELIDE_MODE.inverse[self.elideMode()]


class TabBar(TabBarMixin, widgets.QTabBar):
    """Tab bar, e.g. for use in tabbed dialogs."""


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    tabwidget = widgets.TabWidget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.PlainTextEdit("Test 243434")
    tabwidget.add_tab(widget2, label="test")
    tabwidget.add_tab(widget3, label="test")
    tabbar = tabwidget.tabBar()
    tabwidget.show()
    app.exec()
