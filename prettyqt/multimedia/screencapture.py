from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict


ERROR = bidict(
    no_error=QtMultimedia.QScreenCapture.Error.NoError,
    internal_error=QtMultimedia.QScreenCapture.Error.InternalError,
    capturing_not_supported=QtMultimedia.QScreenCapture.Error.CapturingNotSupported,
    capture_failed=QtMultimedia.QScreenCapture.Error.CaptureFailed,
    not_found=QtMultimedia.QScreenCapture.Error.NotFound,
)

ErrorStr = Literal["none", "resource", "format", "network", "access_denied"]


class ScreenCapture(core.ObjectMixin, QtMultimedia.QScreenCapture):
    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return ERROR.inverse[self.error()]

    def set_screen(self, screen: int | gui.QScreen | Literal["primary"]):
        match screen:
            case int():
                screen = gui.GuiApplication.screens()[screen]
            case gui.QScreen():
                pass
            case "primary":
                screen = gui.GuiApplication.primaryScreen()
            case _:
                raise TypeError(screen)
        self.setScreen(screen)


if __name__ == "__main__":
    player = ScreenCapture()
    source = player.get_source()
    print(source.isValid())
