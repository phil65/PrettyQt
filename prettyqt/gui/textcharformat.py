# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict


WEIGHTS = bidict(thin=QtGui.QFont.Thin,
                 light=QtGui.QFont.Light,
                 medium=QtGui.QFont.Medium,
                 bold=QtGui.QFont.Bold)

UNDERLINE_STYLES = bidict(none=QtGui.QTextCharFormat.NoUnderline,
                          single=QtGui.QTextCharFormat.SingleUnderline,
                          dash=QtGui.QTextCharFormat.DashUnderline,
                          dot=QtGui.QTextCharFormat.DotLine,
                          dashdot=QtGui.QTextCharFormat.DashDotLine,
                          dashdotline=QtGui.QTextCharFormat.DashDotDotLine,
                          wave=QtGui.QTextCharFormat.WaveUnderline,
                          spellcheck=QtGui.QTextCharFormat.SpellCheckUnderline)

STYLE_HINTS = bidict(any=QtGui.QFont.AnyStyle,
                     sans_serif=QtGui.QFont.SansSerif,
                     serif=QtGui.QFont.Serif,
                     typewriter=QtGui.QFont.TypeWriter,
                     decorative=QtGui.QFont.Decorative,
                     monospace=QtGui.QFont.Monospace,
                     fantasy=QtGui.QFont.Fantasy,
                     cursive=QtGui.QFont.Cursive,
                     system=QtGui.QFont.System)


class TextCharFormat(QtGui.QTextCharFormat):

    def set_foreground_color(self, color):
        if isinstance(color, (list, tuple)):
            color = gui.Color(*color)
        elif not isinstance(color, (QtGui.QColor, QtGui.QBrush)):
            color = gui.Color(color)
        self.setForeground(color)

    def set_background_color(self, color):
        if isinstance(color, (list, tuple)):
            color = gui.Color(*color)
        elif not isinstance(color, (QtGui.QColor, QtGui.QBrush)):
            color = gui.Color(color)
        self.setBackground(color)

    def set_font_weight(self, weight: str):
        """sets the font weight

        Valid values are "thin", "light", "medium" and "bold"

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

    def set_font_style_hint(self, hint):
        """sets the font style hint

        Valid values are "any", "sans_serif", "serif", "typewriter", "decorative",
        "monospace", "fantasy", "cursive", "system"

        Args:
            style: font style hint

        Raises:
            ValueError: invalid font style hint
        """
        if hint not in STYLE_HINTS:
            raise ValueError("Invalid font style hint")
        self.setFontStyleHint(STYLE_HINTS[hint])
