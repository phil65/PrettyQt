from typing import Literal

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

ANCESTER_MODES = bidict(
    exclude_transients=QtGui.QWindow.ExcludeTransients,
    include_transients=QtGui.QWindow.IncludeTransients,
)

VISIBILITY = bidict(
    windowed=QtGui.QWindow.Windowed,
    minimized=QtGui.QWindow.Minimized,
    maximized=QtGui.QWindow.Maximized,
    fullscreen=QtGui.QWindow.FullScreen,
    automatic=QtGui.QWindow.AutomaticVisibility,
    hidden=QtGui.QWindow.Hidden,
)

VisibilityStr = Literal[
    "windowed", "minimized", "maximized", "fullscreen", "automatic", "hidden"
]

EDGES = bidict(
    top=QtCore.Qt.TopEdge,
    left=QtCore.Qt.LeftEdge,
    right=QtCore.Qt.RightEdge,
    bottom=QtCore.Qt.BottomEdge,
    top_left=QtCore.Qt.TopEdge | QtCore.Qt.LeftEdge,
    top_right=QtCore.Qt.TopEdge | QtCore.Qt.RightEdge,
    bottom_left=QtCore.Qt.BottomEdge | QtCore.Qt.LeftEdge,
    bottom_right=QtCore.Qt.BottomEdge | QtCore.Qt.RightEdge,
)

EdgeStr = Literal[
    "top",
    "left",
    "right",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
]

QtGui.QWindow.__bases__ = (core.Object, gui.Surface)


class Window(QtGui.QWindow):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    # def serialize_fields(self):
    #     return dict(
    #         speed=self.speed(),
    #         visibility=self.get_visibility(),
    #         scaled_size=self.scaledSize(),
    #         background_color=self.backgroundColor(),
    #     )

    def set_visibility(self, visibility: VisibilityStr):
        """Set window visibility.

        Args:
            visibility: window visibility

        Raises:
            InvalidParamError: window visibility does not exist
        """
        if visibility not in VISIBILITY:
            raise InvalidParamError(visibility, VISIBILITY)
        self.setVisibility(VISIBILITY[visibility])

    def get_visibility(self) -> VisibilityStr:
        """Get the current window visibility.

        Returns:
            window visibility
        """
        return VISIBILITY.inverse[self.visibility()]

    def start_system_resize(self, edge: EdgeStr) -> bool:
        """Start system resize.

        Args:
            edge: edge to resize

        Raises:
            InvalidParamError: edge does not exist
        """
        if edge not in EDGES:
            raise InvalidParamError(edge, EDGES)
        return self.startSystemResize(EDGES[edge])


if __name__ == "__main__":
    wnd = Window()
