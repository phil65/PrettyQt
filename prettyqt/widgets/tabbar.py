from typing import Literal, Optional, Tuple, Union

from deprecated import deprecated
from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import constants, core, widgets
from prettyqt.utils import InvalidParamError, bidict


REMOVE_BEHAVIOUR = bidict(
    left_tab=QtWidgets.QTabBar.SelectLeftTab,
    right_tab=QtWidgets.QTabBar.SelectRightTab,
    previous_tab=QtWidgets.QTabBar.SelectPreviousTab,
)

RemoveBehaviourStr = Literal["left_tab", "right_tab", "previous_tab"]

SHAPE = bidict(
    rounded_north=QtWidgets.QTabBar.RoundedNorth,
    rounded_south=QtWidgets.QTabBar.RoundedSouth,
    rounded_west=QtWidgets.QTabBar.RoundedWest,
    rounded_east=QtWidgets.QTabBar.RoundedEast,
    triangular_north=QtWidgets.QTabBar.TriangularNorth,
    triangular_south=QtWidgets.QTabBar.TriangularSouth,
    triangular_west=QtWidgets.QTabBar.TriangularWest,
    triangular_east=QtWidgets.QTabBar.TriangularEast,
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

POSITIONS = bidict(left=QtWidgets.QTabBar.LeftSide, right=QtWidgets.QTabBar.RightSide)

PositionStr = Literal["left", "right"]

QtWidgets.QTabBar.__bases__ = (widgets.Widget,)


class TabBar(QtWidgets.QTabBar):
    on_detach = QtCore.Signal(int, QtCore.QPoint)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.set_elide_mode("right")
        self.set_selection_behavior_on_remove("left_tab")
        self.mouse_cursor = QtGui.QCursor()

    def __getitem__(self, index: Tuple[int, str]):
        return self.tabButton(index[0], POSITIONS[index[1]])

    def __setitem__(self, index: Tuple[int, str], value: Optional[QtWidgets.QWidget]):
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
        self.on_detach.emit(self.tabAt(event.pos()), self.mouse_cursor.pos())

    def set_icon_size(self, size: Union[int, Tuple[int, int], QtCore.QSize]):
        """Set size of the icons."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def set_tab(
        self, index: int, position: str, widget: Optional[QtWidgets.QWidget]
    ) -> None:
        self.setTabButton(index, POSITIONS[position], widget)

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
