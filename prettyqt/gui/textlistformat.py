from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


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

STYLES: bidict[StyleStr, QtGui.QTextListFormat.Style] = bidict(
    disc=QtGui.QTextListFormat.Style.ListDisc,
    circle=QtGui.QTextListFormat.Style.ListCircle,
    square=QtGui.QTextListFormat.Style.ListSquare,
    decimal=QtGui.QTextListFormat.Style.ListDecimal,
    lower_alpha=QtGui.QTextListFormat.Style.ListLowerAlpha,
    upper_alpha=QtGui.QTextListFormat.Style.ListUpperAlpha,
    lower_roman=QtGui.QTextListFormat.Style.ListLowerRoman,
    upper_roman=QtGui.QTextListFormat.Style.ListUpperRoman,
)


class TextListFormat(gui.TextFormatMixin, QtGui.QTextListFormat):
    def set_style(self, style: StyleStr | QtGui.QTextListFormat.Style):
        """Set the style.

        Args:
            style: style
        """
        self.setStyle(STYLES.get_enum_value(style))

    def get_style(self) -> StyleStr:
        """Get current style.

        Returns:
            current style
        """
        return STYLES.inverse[self.style()]
