from qtpy import QtGui, QtCore

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError


CAP_STYLES = bidict(
    flat=QtCore.Qt.FlatCap, square=QtCore.Qt.SquareCap, round=QtCore.Qt.RoundCap
)

JOIN_STYLES = bidict(
    miter=QtCore.Qt.MiterJoin,
    bevel=QtCore.Qt.BevelJoin,
    round=QtCore.Qt.RoundJoin,
    svg_miter=QtCore.Qt.SvgMiterJoin,
)


class PainterPathStroker(QtGui.QPainterPathStroker):
    def set_cap_style(self, style: str):
        """Set cap style to use.

        Allowed values are "flat", "square", "round"

        Args:
            style: cap style to use

        Raises:
            InvalidParamError: cap style does not exist
        """
        if style not in CAP_STYLES:
            raise InvalidParamError(style, CAP_STYLES)
        self.setCapStyle(CAP_STYLES[style])

    def get_cap_style(self) -> str:
        """Return current cap style.

        Possible values: "flat", "square", "round"

        Returns:
            cap style
        """
        return CAP_STYLES.inverse[self.capStyle()]

    def set_join_style(self, style: str):
        """Set join style to use.

        Allowed values are "miter", "bevel", "round", "svg_miter"

        Args:
            style: join style to use

        Raises:
            InvalidParamError: join style does not exist
        """
        if style not in JOIN_STYLES:
            raise InvalidParamError(style, JOIN_STYLES)
        self.setJoinStyle(JOIN_STYLES[style])

    def get_join_style(self) -> str:
        """Return current join style.

        Possible values: "miter", "bevel", "round", "svg_miter"

        Returns:
            join style
        """
        return JOIN_STYLES.inverse[self.joinStyle()]

    def create_stroke(self, path: QtGui.QPainterPath) -> gui.PainterPath:
        return gui.PainterPath(self.createStroke(path))


if __name__ == "__main__":
    p = PainterPathStroker(QtCore.QPoint(1, 1))
    print(list(p))
