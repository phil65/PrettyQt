# -*- coding: utf-8 -*-

from typing import Union

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, colors, InvalidParamError


FONT_PROPERTY_INHERITANCE_BEHAVIOUR = bidict(
    none=QtGui.QTextCharFormat.FontPropertiesSpecifiedOnly,
    single=QtGui.QTextCharFormat.FontPropertiesAll,
)

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

VERTICAL_ALIGNMENT = bidict(
    normal=QtGui.QTextCharFormat.AlignNormal,
    super_script=QtGui.QTextCharFormat.AlignSuperScript,
    sub_script=QtGui.QTextCharFormat.AlignSubScript,
    middle=QtGui.QTextCharFormat.AlignMiddle,
    bottom=QtGui.QTextCharFormat.AlignBottom,
    top=QtGui.QTextCharFormat.AlignTop,
    baseline=QtGui.QTextCharFormat.AlignBaseline,
)


QtGui.QTextCharFormat.__bases__ = (gui.TextFormat,)


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
        """Set the font weight.

        Valid values are "thin", "extra_light", light", "medium", "demi_bold", "bold",
                         "extra_bold", normal", "black"

        Args:
            weight: font weight

        Raises:
            InvalidParamError: invalid font weight
        """
        if weight not in gui.font.WEIGHTS:
            raise InvalidParamError(weight, gui.font.WEIGHTS)
        self.setFontWeight(gui.font.WEIGHTS[weight])

    def get_font_weight(self) -> str:
        """Get current font weight.

        Possible values are "thin", "light", "medium" or "bold"

        Returns:
            current font weight
        """
        return gui.font.WEIGHTS.inv[self.fontWeight()]

    def set_underline_style(self, style: str):
        """Set the underline style.

        Valid values are "none", "single", "dash", "dot", "dashdot", "dashdotline",
        "wave", "spellcheck"

        Args:
            style: underline style

        Raises:
            InvalidParamError: invalid underline style
        """
        if style not in UNDERLINE_STYLES:
            raise InvalidParamError(style, UNDERLINE_STYLES)
        self.setUnderlineStyle(UNDERLINE_STYLES[style])

    def get_underline_style(self) -> str:
        """Get current underline style.

        Possible values are "none", "single", "dash", "dot", "dashdot", "dashdotline",
        "wave", "spellcheck"

        Returns:
            current underline style
        """
        return UNDERLINE_STYLES.inv[self.underlineStyle()]

    def set_vertical_alignment(self, alignment: str):
        """Set the vertical alignment.

        Valid values: "normal", "super_script", "sub_script", "middle", "bottom", "top",
        "baseline"

        Args:
            alignment: vertical alignment

        Raises:
            InvalidParamError: invalid vertical alignment
        """
        if alignment not in VERTICAL_ALIGNMENT:
            raise InvalidParamError(alignment, VERTICAL_ALIGNMENT)
        self.setVerticalAlignment(VERTICAL_ALIGNMENT[alignment])

    def get_vertical_alignment(self) -> str:
        """Get current vertical alignment.

        Possible values: "normal", "super_script", "sub_script", "middle", "bottom",
        "top", "baseline"

        Returns:
            current vertical alignment
        """
        return VERTICAL_ALIGNMENT.inv[self.verticalAlignment()]

    def set_font_style_hint(self, hint: str):
        """Set the font style hint.

        Valid values are "any", "sans_serif", "serif", "typewriter", "decorative",
        "monospace", "fantasy", "cursive", "system"

        Args:
            hint: font style hint

        Raises:
            InvalidParamError: invalid font style hint
        """
        if hint not in gui.font.STYLE_HINTS:
            raise InvalidParamError(hint, gui.font.STYLE_HINTS)
        self.setFontStyleHint(gui.font.STYLE_HINTS[hint])

    def select_full_width(self, value: bool = True):
        self.setProperty(QtGui.QTextFormat.FullWidthSelection, value)

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())
