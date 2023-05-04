from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict, get_repr


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


class WindowMixin(core.ObjectMixin, gui.SurfaceMixin):
    def __repr__(self):
        return get_repr(self)

    # def serialize_fields(self):
    #     return dict(
    #         speed=self.speed(),
    #         visibility=self.get_visibility(),
    #         scaled_size=self.scaledSize(),
    #         background_color=self.backgroundColor(),
    #     )

    def add_shortcut(
        self,
        keysequence: str
        | QtCore.QKeyCombination
        | QtGui.QKeySequence
        | QtGui.QKeySequence.StandardKey,
        callback: Callable | None = None,
        context: constants.ShortcutContextStr = "window",
    ) -> gui.Shortcut:
        if isinstance(keysequence, str):
            keysequence = gui.KeySequence(keysequence)
        context = constants.SHORTCUT_CONTEXT[context]
        return gui.Shortcut(keysequence, self, callback, context=context)

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


class Window(WindowMixin, QtGui.QWindow):
    pass


if __name__ == "__main__":
    wnd = Window()
