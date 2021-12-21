from __future__ import annotations

from typing import Literal

from deprecated import deprecated

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


REMOVE_BEHAVIOUR = bidict(
    left_tab=QtWidgets.QTabBar.SelectionBehavior.SelectLeftTab,
    right_tab=QtWidgets.QTabBar.SelectionBehavior.SelectRightTab,
    previous_tab=QtWidgets.QTabBar.SelectionBehavior.SelectPreviousTab,
)

RemoveBehaviourStr = Literal["left_tab", "right_tab", "previous_tab"]

SHAPE = bidict(
    rounded_north=QtWidgets.QTabBar.Shape.RoundedNorth,
    rounded_south=QtWidgets.QTabBar.Shape.RoundedSouth,
    rounded_west=QtWidgets.QTabBar.Shape.RoundedWest,
    rounded_east=QtWidgets.QTabBar.Shape.RoundedEast,
    triangular_north=QtWidgets.QTabBar.Shape.TriangularNorth,
    triangular_south=QtWidgets.QTabBar.Shape.TriangularSouth,
    triangular_west=QtWidgets.QTabBar.Shape.TriangularWest,
    triangular_east=QtWidgets.QTabBar.Shape.TriangularEast,
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

POSITIONS = bidict(
    left=QtWidgets.QTabBar.ButtonPosition.LeftSide,
    right=QtWidgets.QTabBar.ButtonPosition.RightSide,
)

PositionStr = Literal["left", "right"]

QtWidgets.QTabBar.__bases__ = (widgets.Widget,)


class TabBar(QtWidgets.QTabBar):
    on_detach = QtCore.Signal(int, QtCore.QPoint)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.set_elide_mode("right")
        self.set_selection_behavior_on_remove("left_tab")

    def __getitem__(self, index: tuple[int, str]):
        return self.tabButton(index[0], POSITIONS[index[1]])

    def __setitem__(
        self, index: tuple[int, PositionStr], value: QtWidgets.QWidget | None
    ):
        self.set_tab(index[0], index[1], value)

    def serialize_fields(self):
        return dict(
            movable=self.isMovable(),
            document_mode=self.documentMode(),
            current_index=self.currentIndex(),
            # shape=self.shape(),
            draw_base=self.drawBase(),
            elide_mode=self.get_elide_mode(),
            icon_size=core.Size(self.iconSize()),
        )

    def __setstate__(self, state):
        self.setDocumentMode(state.get("document_mode", False))
        self.setMovable(state.get("movable", False))
        # self.setShape(state.get("shape", "rounded"))
        self.setIconSize(state["icon_size"])
        self.setDrawBase(state.get("draw_base"))
        self.set_elide_mode(state.get("elide_mode"))
        self.setCurrentIndex(state.get("index", 0))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    #  Send the on_detach when a tab is double clicked
    def mouseDoubleClickEvent(self, event):
        event.accept()
        tab = self.tabAt(event.position())
        pos = QtGui.QCursor.pos()
        self.on_detach.emit(tab, pos)

    def set_icon_size(self, size: int | types.SizeType):
        """Set size of the icons."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def set_tab(
        self, index: int, position: PositionStr, widget: QtWidgets.QWidget | None
    ) -> None:
        self.setTabButton(index, POSITIONS[position], widget)  # type: ignore

    @deprecated(
        reason="This method is deprecated, use set_selection_behavior_on_remove instead."
    )
    def set_remove_behaviour(self, mode: RemoveBehaviourStr) -> None:
        self.set_selection_behavior_on_remove(mode)

    def set_selection_behavior_on_remove(self, mode: RemoveBehaviourStr) -> None:
        """Set the remove hehaviour.

        What tab should be set as current when removeTab is called
        if the removed tab is also the current tab.

        Args:
            mode: new remove behaviour
        """
        if mode not in REMOVE_BEHAVIOUR:
            raise InvalidParamError(mode, REMOVE_BEHAVIOUR)
        self.setSelectionBehaviorOnRemove(REMOVE_BEHAVIOUR[mode])

    def get_remove_behaviour(self) -> RemoveBehaviourStr:
        """Return remove behaviour.

        Returns:
            remove behaviour
        """
        return REMOVE_BEHAVIOUR.inverse[self.selectionBehaviorOnRemove()]

    def set_elide_mode(self, mode: constants.ElideModeStr) -> None:
        """Set elide mode.

        Args:
            mode: elide mode to use

        Raises:
            InvalidParamError: invalid elide mode
        """
        if mode not in constants.ELIDE_MODE:
            raise InvalidParamError(mode, constants.ELIDE_MODE)
        self.setElideMode(constants.ELIDE_MODE[mode])

    def get_elide_mode(self) -> constants.ElideModeStr:
        """Return elide mode.

        Returns:
            elide mode
        """
        return constants.ELIDE_MODE.inverse[self.elideMode()]
