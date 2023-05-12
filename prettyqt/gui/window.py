from __future__ import annotations

from collections.abc import Callable
import os
import pathlib
from typing import Literal

from prettyqt import constants, core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, datatypes, get_repr


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
        keysequence: datatypes.KeyCombinationType,
        callback: Callable | None = None,
        context: constants.ShortcutContextStr = "window",
    ) -> gui.Shortcut:
        if not isinstance(keysequence, QtGui.QKeySequence):
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

    def get_cursor(self) -> gui.Cursor:
        return gui.Cursor(self.cursor())

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_modality(self, modality: constants.WindowModalityStr) -> None:
        """Set modality for the window.

        Args:
            modality: modality for the window

        Raises:
            InvalidParamError: modality type does not exist
        """
        if modality not in constants.WINDOW_MODALITY:
            raise InvalidParamError(modality, constants.WINDOW_MODALITY)
        self.setModality(constants.WINDOW_MODALITY[modality])

    def get_modality(self) -> constants.WindowModalityStr:
        return constants.WINDOW_MODALITY.inverse[self.modality()]

    def set_file_path(self, file_path: os.PathLike):
        path = os.fspath(file_path)
        self.setFilePath(path)

    def get_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.filePath())

    def get_type(self) -> constants.WindowTypeStr:
        return constants.WINDOW_TYPE.inverse[self.type()]

    def get_window_state(self) -> constants.WindowStateStr:
        return constants.WINDOW_STATES.inverse[self.windowState()]

    def get_window_states(self) -> list[constants.WindowStateStr]:
        return constants.WINDOW_STATES.get_list(self.windowStates())


class Window(WindowMixin, QtGui.QWindow):
    pass


if __name__ == "__main__":
    wnd = Window()
