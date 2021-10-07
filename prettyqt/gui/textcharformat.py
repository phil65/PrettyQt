from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, colors, types


mod = QtGui.QTextCharFormat

FONT_PROPERTY_INHERITANCE_BEHAVIOUR = bidict(
    none=mod.FontPropertiesInheritanceBehavior.FontPropertiesSpecifiedOnly,
    single=mod.FontPropertiesInheritanceBehavior.FontPropertiesAll,
)

UNDERLINE_STYLE = bidict(
    none=mod.UnderlineStyle.NoUnderline,
    single=mod.UnderlineStyle.SingleUnderline,
    dash=mod.UnderlineStyle.DashUnderline,
    dot=mod.UnderlineStyle.DotLine,
    dashdot=mod.UnderlineStyle.DashDotLine,
    dashdotline=mod.UnderlineStyle.DashDotDotLine,
    wave=mod.UnderlineStyle.WaveUnderline,
    spellcheck=mod.UnderlineStyle.SpellCheckUnderline,
)

UnderlineStyleStr = Literal[
    "none",
    "single",
    "dash",
    "dot",
    "dashdot",
    "dashdotline",
    "wave",
    "spellcheck",
]

VERTICAL_ALIGNMENT = bidict(
    normal=QtGui.QTextCharFormat.VerticalAlignment.AlignNormal,
    super_script=QtGui.QTextCharFormat.VerticalAlignment.AlignSuperScript,
    sub_script=QtGui.QTextCharFormat.VerticalAlignment.AlignSubScript,
    middle=QtGui.QTextCharFormat.VerticalAlignment.AlignMiddle,
    bottom=QtGui.QTextCharFormat.VerticalAlignment.AlignBottom,
    top=QtGui.QTextCharFormat.VerticalAlignment.AlignTop,
    baseline=QtGui.QTextCharFormat.VerticalAlignment.AlignBaseline,
)

VerticalAlignmentStr = Literal[
    "normal",
    "super_script",
    "sub_script",
    "middle",
    "bottom",
    "top",
    "baseline",
]

QtGui.QTextCharFormat.__bases__ = (gui.TextFormat,)


class TextCharFormat(QtGui.QTextCharFormat):
    def __init__(
        self,
        text_color: types.ColorType | QtGui.QBrush = None,
        bold: bool = False,
        italic: bool = False,
    ):
        super().__init__()
        if text_color is not None:
            self.set_foreground_color(text_color)
        if bold:
            self.set_font_weight("bold")
        self.setFontItalic(italic)

    def set_foreground_color(self, color: types.ColorType | QtGui.QBrush):
        if not isinstance(color, QtGui.QBrush):
            color = colors.get_color(color)
        self.setForeground(color)

    def set_background_color(self, color: types.ColorType | QtGui.QBrush):
        if not isinstance(color, QtGui.QBrush):
            color = colors.get_color(color)
        self.setBackground(color)

    def set_font_weight(self, weight: gui.font.WeightStr):
        """Set the font weight.

        Args:
            weight: font weight

        Raises:
            InvalidParamError: invalid font weight
        """
        if weight not in gui.font.WEIGHT:
            raise InvalidParamError(weight, gui.font.WEIGHT)
        self.setFontWeight(gui.font.WEIGHT[weight])

    def get_font_weight(self) -> gui.font.WeightStr:
        """Get current font weight.

        Returns:
            current font weight
        """
        return gui.font.WEIGHT.inverse[self.fontWeight()]

    def set_underline_style(self, style: UnderlineStyleStr):
        """Set the underline style.

        Args:
            style: underline style

        Raises:
            InvalidParamError: invalid underline style
        """
        if style not in UNDERLINE_STYLE:
            raise InvalidParamError(style, UNDERLINE_STYLE)
        self.setUnderlineStyle(UNDERLINE_STYLE[style])

    def get_underline_style(self) -> UnderlineStyleStr:
        """Get current underline style.

        Returns:
            current underline style
        """
        return UNDERLINE_STYLE.inverse[self.underlineStyle()]

    def set_vertical_alignment(self, alignment: VerticalAlignmentStr):
        """Set the vertical alignment.

        Args:
            alignment: vertical alignment

        Raises:
            InvalidParamError: invalid vertical alignment
        """
        if alignment not in VERTICAL_ALIGNMENT:
            raise InvalidParamError(alignment, VERTICAL_ALIGNMENT)
        self.setVerticalAlignment(VERTICAL_ALIGNMENT[alignment])

    def get_vertical_alignment(self) -> VerticalAlignmentStr:
        """Get current vertical alignment.

        Returns:
            current vertical alignment
        """
        return VERTICAL_ALIGNMENT.inverse[self.verticalAlignment()]

    def set_font_style_hint(self, hint: gui.font.StyleHintStr):
        """Set the font style hint.

        Args:
            hint: font style hint

        Raises:
            InvalidParamError: invalid font style hint
        """
        if hint not in gui.font.STYLE_HINTS:
            raise InvalidParamError(hint, gui.font.STYLE_HINTS)
        self.setFontStyleHint(gui.font.STYLE_HINTS[hint])

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())
