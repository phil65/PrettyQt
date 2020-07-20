# -*- coding: utf-8 -*-
"""
"""

from typing import Union

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, colors


UNDERLINE_STYLES = bidict(
    none=QtGui.QTextCharFormat.NoUnderline,
    single=QtGui.QTextCharFormat.SingleUnderline,
    dash=QtGui.QTextCharFormat.DashUnderline,
    dot=QtGui.QTextCharFormat.DotLine,
    dashdot=QtGui.QTextCharFormat.DashDotLine,
    dashdotline=QtGui.QTextCharFormat.DashDotDotLine,
    wave=QtGui.QTextCharFormat.WaveUnderline,
    spellcheck=QtGui.QTextCharFormat.SpellCheckUnderline,
)


WEIGHTS = gui.font.WEIGHTS  # type: ignore

STYLE_HINTS = gui.font.STYLE_HINTS  # type: ignore


class TextCharFormat(QtGui.QTextCharFormat):
    def __init__(
        self,
        text_color: Union[colors.ColorType, QtGui.QBrush] = None,
        bold: bool = False,
        italic: bool = False,
    ):
        super().__init__()
        if text_color is not None:
            self.set_foreground_color(text_color)
        if bold:
            self.set_font_weight("bold")
        self.setFontItalic(italic)

    def set_foreground_color(self, color: Union[colors.ColorType, QtGui.QBrush]):
        if not isinstance(color, QtGui.QBrush):
            color = colors.get_color(color)
        self.setForeground(color)

    def set_background_color(self, color: Union[colors.ColorType, QtGui.QBrush]):
        if not isinstance(color, QtGui.QBrush):
            color = colors.get_color(color)
        self.setBackground(color)

    def set_font_weight(self, weight: str):
        """sets the font weight

        Valid values are "thin", "extra_light", light", "medium", "demi_bold", "bold",
                         "extra_bold", normal", "black"

        Args:
            weight: font weight

        Raises:
            ValueError: invalid font weight
        """
        if weight not in WEIGHTS:
            raise ValueError("Invalid font weight")
        self.setFontWeight(WEIGHTS[weight])

    def get_font_weight(self) -> str:
        """get current font weight

        Possible values are "thin", "light", "medium" or "bold"

        Returns:
            current font weight
        """
        return WEIGHTS.inv[self.fontWeight()]

    def set_underline_style(self, style: str):
        """sets the underline style

        Valid values are "none", "single", "dash", "dot", "dashdot", "dashdotline",
        "wave", "spellcheck"

        Args:
            style: underline style

        Raises:
            ValueError: invalid underline style
        """
        if style not in UNDERLINE_STYLES:
            raise ValueError("Invalid underline style")
        self.setUnderlineStyle(UNDERLINE_STYLES[style])

    def get_underline_style(self) -> str:
        """get current underline style

        Possible values are "none", "single", "dash", "dot", "dashdot", "dashdotline",
        "wave", "spellcheck"

        Returns:
            current underline style
        """
        return UNDERLINE_STYLES.inv[self.underlineStyle()]

    def set_font_style_hint(self, hint: str):
        """sets the font style hint

        Valid values are "any", "sans_serif", "serif", "typewriter", "decorative",
        "monospace", "fantasy", "cursive", "system"

        Args:
            hint: font style hint

        Raises:
            ValueError: invalid font style hint
        """
        if hint not in STYLE_HINTS:
            raise ValueError("Invalid font style hint")
        self.setFontStyleHint(STYLE_HINTS[hint])

    def select_full_width(self, value: bool = True):
        self.setProperty(QtGui.QTextFormat.FullWidthSelection, value)
