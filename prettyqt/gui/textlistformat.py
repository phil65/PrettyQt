from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import InvalidParamError, bidict


STYLES = bidict(
    disc=QtGui.QTextListFormat.ListDisc,
    circle=QtGui.QTextListFormat.ListCircle,
    square=QtGui.QTextListFormat.ListSquare,
    decimal=QtGui.QTextListFormat.ListDecimal,
    lower_alpha=QtGui.QTextListFormat.ListLowerAlpha,
    upper_alpha=QtGui.QTextListFormat.ListUpperAlpha,
    lower_roman=QtGui.QTextListFormat.ListLowerRoman,
    upper_roman=QtGui.QTextListFormat.ListUpperRoman,
)


QtGui.QTextListFormat.__bases__ = (gui.TextFormat,)


class TextListFormat(QtGui.QTextListFormat):
    def set_style(self, style: str):
        """Set the style.

        Valid values are "disc", "circle", square", "decimal", "lower_alpha",
                         "upper_alpha", "lower_roman", upper_roman"

        Args:
            style: style

        Raises:
            InvalidParamError: invalid style
        """
        if style not in STYLES:
            raise InvalidParamError(style, STYLES)
        self.setStyle(STYLES[style])

    def get_style(self) -> str:
        """Get current style.

        Possible values are "disc", "circle", square", "decimal", "lower_alpha",
                            "upper_alpha", "lower_roman", upper_roman"

        Returns:
            current style
        """
        return STYLES.inverse[self.style()]
