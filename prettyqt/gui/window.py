# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

ANCESTER_MODES = bidict(
    exclude_transients=QtGui.QWindow.ExcludeTransients,
    include_transients=QtGui.QWindow.IncludeTransients,
)

VISIBILITIES = bidict(
    windowed=QtGui.QWindow.Windowed,
    minimized=QtGui.QWindow.Minimized,
    maximized=QtGui.QWindow.Maximized,
    fullscreen=QtGui.QWindow.FullScreen,
    automatic=QtGui.QWindow.AutomaticVisibility,
    hidden=QtGui.QWindow.Hidden,
)

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

    def set_visibility(self, visibility: str):
        """Set window visibility.

        Valid values: "windowed", "maximized", "minimized", "fullscreen", "automatic",
                      "hidden"

        Args:
            visibility: window visibility

        Raises:
            InvalidParamError: window visibility does not exist
        """
        if visibility not in VISIBILITIES:
            raise InvalidParamError(visibility, VISIBILITIES)
        self.setVisibility(VISIBILITIES[visibility])

    def get_visibility(self) -> str:
        """Get the current window visibility.

        Possible values: "windowed", "maximized", "minimized", "fullscreen", "automatic",
                         "hidden"

        Returns:
            window visibility
        """
        return VISIBILITIES.inv[self.visibility()]


if __name__ == "__main__":
    wnd = Window()
