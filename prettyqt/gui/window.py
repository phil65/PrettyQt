from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


ANCESTER_MODES = bidict(
    exclude_transients=QtGui.QWindow.AncestorMode.ExcludeTransients,
    include_transients=QtGui.QWindow.AncestorMode.IncludeTransients,
)

VISIBILITY = bidict(
    windowed=QtGui.QWindow.Visibility.Windowed,
    minimized=QtGui.QWindow.Visibility.Minimized,
    maximized=QtGui.QWindow.Visibility.Maximized,
    fullscreen=QtGui.QWindow.Visibility.FullScreen,
    automatic=QtGui.QWindow.Visibility.AutomaticVisibility,
    hidden=QtGui.QWindow.Visibility.Hidden,
)

VisibilityStr = Literal[
    "windowed", "minimized", "maximized", "fullscreen", "automatic", "hidden"
]


QtGui.QWindow.__bases__ = (core.Object, gui.Surface)


class Window(QtGui.QWindow):
    def __repr__(self):
        return f"{type(self).__name__}()"

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

    def start_system_resize(self, edge: constants.EdgeStr) -> bool:
        """Start system resize.

        Args:
            edge: edge to resize

        Raises:
            InvalidParamError: edge does not exist
        """
        if edge not in constants.EDGES:
            raise InvalidParamError(edge, constants.EDGES)
        return self.startSystemResize(constants.EDGES[edge])

    def get_screen(self) -> gui.Screen:
        return gui.Screen(self.screen())


if __name__ == "__main__":
    wnd = Window()
