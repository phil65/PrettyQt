from __future__ import annotations

from typing import Literal

from prettyqt import gui
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

STYLES: bidict[StyleStr, gui.QTextListFormat.Style] = bidict(
    disc=gui.QTextListFormat.Style.ListDisc,
    circle=gui.QTextListFormat.Style.ListCircle,
    square=gui.QTextListFormat.Style.ListSquare,
    decimal=gui.QTextListFormat.Style.ListDecimal,
    lower_alpha=gui.QTextListFormat.Style.ListLowerAlpha,
    upper_alpha=gui.QTextListFormat.Style.ListUpperAlpha,
    lower_roman=gui.QTextListFormat.Style.ListLowerRoman,
    upper_roman=gui.QTextListFormat.Style.ListUpperRoman,
)


class TextListFormat(gui.TextFormatMixin, gui.QTextListFormat):
    def set_style(self, style: StyleStr | gui.QTextListFormat.Style):
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
