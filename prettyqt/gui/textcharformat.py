from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.utils import bidict, colors, datatypes


mod = gui.QTextCharFormat

FontPropertiesInheritanceBehaviorStr = Literal["none", "single"]

FONT_PROPERTY_INHERITANCE_BEHAVIOUR: bidict[
    FontPropertiesInheritanceBehaviorStr, mod.FontPropertiesInheritanceBehavior
] = bidict(
    none=mod.FontPropertiesInheritanceBehavior.FontPropertiesSpecifiedOnly,
    single=mod.FontPropertiesInheritanceBehavior.FontPropertiesAll,
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

UNDERLINE_STYLE: bidict[UnderlineStyleStr, mod.UnderlineStyle] = bidict(
    none=mod.UnderlineStyle.NoUnderline,
    single=mod.UnderlineStyle.SingleUnderline,
    dash=mod.UnderlineStyle.DashUnderline,
    dot=mod.UnderlineStyle.DotLine,
    dashdot=mod.UnderlineStyle.DashDotLine,
    dashdotline=mod.UnderlineStyle.DashDotDotLine,
    wave=mod.UnderlineStyle.WaveUnderline,
    spellcheck=mod.UnderlineStyle.SpellCheckUnderline,
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

VERTICAL_ALIGNMENT: bidict[
    VerticalAlignmentStr, gui.QTextCharFormat.VerticalAlignment
] = bidict(
    normal=gui.QTextCharFormat.VerticalAlignment.AlignNormal,
    super_script=gui.QTextCharFormat.VerticalAlignment.AlignSuperScript,
    sub_script=gui.QTextCharFormat.VerticalAlignment.AlignSubScript,
    middle=gui.QTextCharFormat.VerticalAlignment.AlignMiddle,
    bottom=gui.QTextCharFormat.VerticalAlignment.AlignBottom,
    top=gui.QTextCharFormat.VerticalAlignment.AlignTop,
    baseline=gui.QTextCharFormat.VerticalAlignment.AlignBaseline,
)


class TextCharFormatMixin(gui.TextFormatMixin):
    def __init__(
        self,
        text_color: datatypes.ColorType | gui.QBrush = None,
        bold: bool = False,
        italic: bool = False,
    ):
        super().__init__()
        if text_color is not None:
            self.set_foreground_color(text_color)
        if bold:
            self.set_font_weight("bold")
        self.setFontItalic(italic)

    def set_foreground_color(self, color: datatypes.ColorType | gui.QBrush):
        if not isinstance(color, gui.QBrush):
            color = colors.get_color(color)
        self.setForeground(color)

    def set_background_color(self, color: datatypes.ColorType | gui.QBrush):
        if not isinstance(color, gui.QBrush):
            color = colors.get_color(color)
        self.setBackground(color)

    def set_font_weight(self, weight: gui.font.WeightStr | gui.Font.Weight):
        """Set the font weight.

        Args:
            weight: font weight
        """
        self.setFontWeight(gui.font.WEIGHT.get_enum_value(weight))

    def get_font_weight(self) -> gui.font.WeightStr:
        """Get current font weight.

        Returns:
            current font weight
        """
        return gui.font.WEIGHT.inverse[self.fontWeight()]

    def set_underline_style(self, style: UnderlineStyleStr | mod.UnderlineStyle):
        """Set the underline style.

        Args:
            style: underline style
        """
        self.setUnderlineStyle(UNDERLINE_STYLE.get_enum_value(style))

    def get_underline_style(self) -> UnderlineStyleStr:
        """Get current underline style.

        Returns:
            current underline style
        """
        return UNDERLINE_STYLE.inverse[self.underlineStyle()]

    def set_vertical_alignment(
        self, alignment: VerticalAlignmentStr | gui.QTextCharFormat.VerticalAlignment
    ):
        """Set the vertical alignment.

        Args:
            alignment: vertical alignment
        """
        self.setVerticalAlignment(VERTICAL_ALIGNMENT.get_enum_value(alignment))

    def get_vertical_alignment(self) -> VerticalAlignmentStr:
        """Get current vertical alignment.

        Returns:
            current vertical alignment
        """
        return VERTICAL_ALIGNMENT.inverse[self.verticalAlignment()]

    def set_font_style_hint(self, hint: gui.font.StyleHintStr | gui.Font.StyleHint):
        """Set the font style hint.

        Args:
            hint: font style hint
        """
        self.setFontStyleHint(gui.font.STYLE_HINTS.get_enum_value(hint))

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())


class TextCharFormat(TextCharFormatMixin, gui.QTextCharFormat):
    pass


if __name__ == "__main__":
    w = TextCharFormat()
