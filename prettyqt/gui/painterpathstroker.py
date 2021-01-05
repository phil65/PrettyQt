from __future__ import annotations

from prettyqt import constants, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError


class PainterPathStroker(QtGui.QPainterPathStroker):
    def set_cap_style(self, style: constants.CapStyleStr):
        """Set cap style to use.

        Args:
            style: cap style to use

        Raises:
            InvalidParamError: cap style does not exist
        """
        if style not in constants.CAP_STYLE:
            raise InvalidParamError(style, constants.CAP_STYLE)
        self.setCapStyle(constants.CAP_STYLE[style])

    def get_cap_style(self) -> constants.CapStyleStr:
        """Return current cap style.

        Returns:
            cap style
        """
        return constants.CAP_STYLE.inverse[self.capStyle()]

    def set_join_style(self, style: constants.JoinStyleStr):
        """Set join style to use.

        Args:
            style: join style to use

        Raises:
            InvalidParamError: join style does not exist
        """
        if style not in constants.JOIN_STYLE:
            raise InvalidParamError(style, constants.JOIN_STYLE)
        self.setJoinStyle(constants.JOIN_STYLE[style])

    def get_join_style(self) -> constants.JoinStyleStr:
        """Return current join style.

        Returns:
            join style
        """
        return constants.JOIN_STYLE.inverse[self.joinStyle()]

    def create_stroke(self, path: QtGui.QPainterPath) -> gui.PainterPath:
        return gui.PainterPath(self.createStroke(path))


if __name__ == "__main__":
    p = PainterPathStroker(QtCore.QPoint(1, 1))
    print(list(p))
