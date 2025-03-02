from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui
from prettyqt.utils import bidict, datatypes, get_repr


if TYPE_CHECKING:
    from collections.abc import Callable


AncestorModeStr = Literal["exclude_transients", "include_transients"]

ANCESTER_MODES: bidict[AncestorModeStr, gui.QWindow.AncestorMode] = bidict(
    exclude_transients=gui.QWindow.AncestorMode.ExcludeTransients,
    include_transients=gui.QWindow.AncestorMode.IncludeTransients,
)

VisibilityStr = Literal[
    "windowed", "minimized", "maximized", "fullscreen", "automatic", "hidden"
]

VISIBILITY: bidict[VisibilityStr, gui.QWindow.Visibility] = bidict(
    windowed=gui.QWindow.Visibility.Windowed,
    minimized=gui.QWindow.Visibility.Minimized,
    maximized=gui.QWindow.Visibility.Maximized,
    fullscreen=gui.QWindow.Visibility.FullScreen,
    automatic=gui.QWindow.Visibility.AutomaticVisibility,
    hidden=gui.QWindow.Visibility.Hidden,
)


class WindowMixin(core.ObjectMixin, gui.SurfaceMixin):
    def __repr__(self):
        return get_repr(self)

    def add_shortcut(
        self,
        keysequence: datatypes.KeyCombinationType,
        callback: Callable | None = None,
        context: constants.ShortcutContextStr | constants.ShortcutContext = "window",
    ) -> gui.Shortcut:
        if not isinstance(keysequence, gui.QKeySequence):
            keysequence = gui.KeySequence(keysequence)
        context = constants.SHORTCUT_CONTEXT.get_enum_value(context)
        return gui.Shortcut(keysequence, self, callback, context=context)

    def set_visibility(self, visibility: VisibilityStr | gui.QWindow.Visibility):
        """Set window visibility.

        Args:
            visibility: window visibility
        """
        self.setVisibility(VISIBILITY.get_enum_value(visibility))

    def get_visibility(self) -> VisibilityStr:
        """Get the current window visibility.

        Returns:
            window visibility
        """
        return VISIBILITY.inverse[self.visibility()]

    def start_system_resize(self, edge: constants.EdgeStr | constants.Edge) -> bool:
        """Start system resize.

        Args:
            edge: edge to resize
        """
        return self.startSystemResize(constants.EDGES.get_enum_value(edge))

    def get_screen(self) -> gui.Screen:
        return gui.Screen(self.screen())

    def get_cursor(self) -> gui.Cursor:
        return gui.Cursor(self.cursor())

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_modality(
        self, modality: constants.WindowModalityStr | constants.WindowModality
    ) -> None:
        """Set modality for the window.

        Args:
            modality: modality for the window
        """
        self.setModality(constants.WINDOW_MODALITY.get_enum_value(modality))

    def get_modality(self) -> constants.WindowModalityStr:
        return constants.WINDOW_MODALITY.inverse[self.modality()]

    def set_file_path(self, file_path: str | os.PathLike[str]):
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


class Window(WindowMixin, gui.QWindow):
    pass


if __name__ == "__main__":
    wnd = Window()
