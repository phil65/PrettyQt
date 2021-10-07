from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


STYLES = bidict(
    disc=QtGui.QTextListFormat.Style.ListDisc,
    circle=QtGui.QTextListFormat.Style.ListCircle,
    square=QtGui.QTextListFormat.Style.ListSquare,
    decimal=QtGui.QTextListFormat.Style.ListDecimal,
    lower_alpha=QtGui.QTextListFormat.Style.ListLowerAlpha,
    upper_alpha=QtGui.QTextListFormat.Style.ListUpperAlpha,
    lower_roman=QtGui.QTextListFormat.Style.ListLowerRoman,
    upper_roman=QtGui.QTextListFormat.Style.ListUpperRoman,
)

StyleStr = Literal[
    "disc",
    "circle",
    "square",
    "decimal",
    "lower_alpha",
    "upper_alpha",
    "lower_roman",
    "upper_roman",
]

QtGui.QTextListFormat.__bases__ = (gui.TextFormat,)


class TextListFormat(QtGui.QTextListFormat):
    def set_style(self, style: StyleStr):
        """Set the style.

        Args:
            style: style

        Raises:
            InvalidParamError: invalid style
        """
        if style not in STYLES:
            raise InvalidParamError(style, STYLES)
        self.setStyle(STYLES[style])

    def get_style(self) -> StyleStr:
        """Get current style.

        Returns:
            current style
        """
        return STYLES.inverse[self.style()]
