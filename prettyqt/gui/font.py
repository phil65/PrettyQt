# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError, prettyprinter


CAPITALIZATION = bidict(
    mixed_case=QtGui.QFont.MixedCase,
    all_uppercase=QtGui.QFont.AllUppercase,
    all_lowercase=QtGui.QFont.AllLowercase,
    small_caps=QtGui.QFont.SmallCaps,
    capitalize=QtGui.QFont.Capitalize,
)

HINTING_PREFERENCE = bidict(
    default=QtGui.QFont.PreferDefaultHinting,
    none=QtGui.QFont.PreferNoHinting,
    vertical=QtGui.QFont.PreferVerticalHinting,
    full=QtGui.QFont.PreferFullHinting,
)

SPACING_TYPE = bidict(
    percentage=QtGui.QFont.PercentageSpacing,
    absolute=QtGui.QFont.AbsoluteSpacing,
)

STRETCH = bidict(
    any=QtGui.QFont.AnyStretch,
    ultra_condensed=QtGui.QFont.UltraCondensed,
    extra_condensed=QtGui.QFont.ExtraCondensed,
    condensed=QtGui.QFont.Condensed,
    semi_condensed=QtGui.QFont.SemiCondensed,
    unstretched=QtGui.QFont.Unstretched,
    semi_expanded=QtGui.QFont.SemiExpanded,
    expanded=QtGui.QFont.Expanded,
    extra_expanded=QtGui.QFont.ExtraExpanded,
    ultra_expanded=QtGui.QFont.UltraExpanded,
)

STYLE = bidict(
    normal=QtGui.QFont.StyleNormal,
    italic=QtGui.QFont.StyleItalic,
    oblique=QtGui.QFont.StyleOblique,
)

STYLE_STRATEGY = bidict(
    prefer_default=QtGui.QFont.PreferDefault,
    prefer_bitmap=QtGui.QFont.PreferBitmap,
    prefer_device=QtGui.QFont.PreferDevice,
    prefer_outline=QtGui.QFont.PreferOutline,
    force_outline=QtGui.QFont.ForceOutline,
    no_antialias=QtGui.QFont.NoAntialias,
    so_subpixel_antialias=QtGui.QFont.NoSubpixelAntialias,
    prefer_antialias=QtGui.QFont.PreferAntialias,
    open_gl_compatible=QtGui.QFont.OpenGLCompatible,
    no_font_merging=QtGui.QFont.NoFontMerging,
    prefer_no_shaping=QtGui.QFont.PreferNoShaping,
)  # ORed with PreferMatch, PreferQuality, ForceIntegerMetrics

STYLE_HINTS = bidict(
    any=QtGui.QFont.AnyStyle,
    sans_serif=QtGui.QFont.SansSerif,
    serif=QtGui.QFont.Serif,
    typewriter=QtGui.QFont.TypeWriter,
    decorative=QtGui.QFont.Decorative,
    monospace=QtGui.QFont.Monospace,
    fantasy=QtGui.QFont.Fantasy,
    cursive=QtGui.QFont.Cursive,
    system=QtGui.QFont.System,
)

WEIGHTS = bidict(
    thin=QtGui.QFont.Thin,
    extra_light=QtGui.QFont.ExtraLight,
    light=QtGui.QFont.Light,
    normal=QtGui.QFont.Normal,
    medium=QtGui.QFont.Medium,
    demi_bold=QtGui.QFont.DemiBold,
    bold=QtGui.QFont.Bold,
    extra_bold=QtGui.QFont.ExtraBold,
    black=QtGui.QFont.Black,
)


class Font(prettyprinter.PrettyPrinter, QtGui.QFont):
    def __repr__(self):
        return (
            f"Font('{self.family()}', {self.pointSize()}, "
            f"{self.weight()}, {self.italic()})"
        )

    def __getstate__(self):
        return dict(
            family=self.family(),
            pointsize=self.pointSize(),
            weight=self.weight(),
            italic=self.italic(),
        )

    def serialize(self):
        return self.__getstate__()

    def __setstate__(self, state):
        self.__init__()
        self.setFamily(state["family"])
        if state["pointsize"] > -1:
            self.setPointSize(state["pointsize"])
        self.setWeight(state["weight"])
        self.setItalic(state["italic"])

    @property
    def metrics(self):
        return gui.FontMetrics(self)

    def set_size(self, size: int):
        self.setPointSize(size)

    @classmethod
    def mono(cls, size=8):
        font = cls("Consolas", size)
        # font.setStyleHint()
        return font

    def set_style_hint(self, hint: str):
        """Set the style hint.

        Valid values are "any", "sans_serif", "serif", "typewriter", "decorative",
        "monospace", "fantasy", "cursive", "system"

        Args:
            hint: style hint

        Raises:
            InvalidParamError: invalid style hint
        """
        if hint not in STYLE_HINTS:
            raise InvalidParamError(hint, STYLE_HINTS)
        self.setStyleHint(STYLE_HINTS[hint])

    def set_weight(self, weight: str):
        """Set the font weight.

        Valid values are "thin", "extra_light", light", "medium", "demi_bold", "bold",
                         "extra_bold", normal", "black"

        Args:
            weight: font weight

        Raises:
            InvalidParamError: invalid font weight
        """
        if weight not in WEIGHTS:
            raise InvalidParamError(weight, WEIGHTS)
        self.setWeight(WEIGHTS[weight])

    def get_weight(self) -> str:
        """Get current font weight.

        Possible values are "thin", "extra_light", light", "medium", "demi_bold", "bold",
                            "extra_bold", normal", "black"

        Returns:
            current font weight
        """
        return WEIGHTS.inv[self.weight()]

    def set_capitalization(self, capitalization: str):
        """Set the font capitalization.

        Valid values are "mixed_case", "all_uppercase", all_lowercase", "small_caps",
                         "capitalize"

        Args:
            capitalization: font capitalization

        Raises:
            InvalidParamError: invalid font capitalization
        """
        if capitalization not in CAPITALIZATION:
            raise InvalidParamError(capitalization, CAPITALIZATION)
        self.setCapitalization(CAPITALIZATION[capitalization])

    def get_capitalization(self) -> str:
        """Get current font capitalization.

        Possible values are "mixed_case", "all_uppercase", all_lowercase", "small_caps",
                            "capitalize"

        Returns:
            current font capitalization
        """
        return CAPITALIZATION.inv[self.capitalization()]

    def set_hinting_preference(self, preference: str):
        """Set the hinting preference.

        Valid values are "default", "none", "vertical", "full"

        Args:
            preference: hinting preference

        Raises:
            InvalidParamError: invalid hinting preference
        """
        if preference not in HINTING_PREFERENCE:
            raise InvalidParamError(preference, HINTING_PREFERENCE)
        self.setHintingPreference(HINTING_PREFERENCE[preference])

    def get_hinting_preference(self) -> str:
        """Get current hinting preference.

        Possible values are "default", "none", "vertical", "full"

        Returns:
            current hinting preference
        """
        return HINTING_PREFERENCE.inv[self.hintingPreference()]

    def set_letter_spacing(self, typ: str, spacing: float):
        """Set the letter spacing.

        Valid values are "percentage", "absolute"

        Args:
            typ: letter spacing type
            spacing: spacing

        Raises:
            InvalidParamError: invalid letter spacing type
        """
        if typ not in SPACING_TYPE:
            raise InvalidParamError(typ, SPACING_TYPE)
        self.setLetterSpacing(SPACING_TYPE[typ], spacing)

    def get_letter_spacing_type(self) -> str:
        """Get current letter spacing type.

        Possible values are "percentage", "absolute"

        Returns:
            current letter spacing type
        """
        return SPACING_TYPE.inv[self.letterSpacingType()]

    def set_style(self, style: str):
        """Set the font style.

        Valid values are "normal", "italic", "oblique"

        Args:
            style: font style

        Raises:
            InvalidParamError: invalid font style
        """
        if style not in STYLE:
            raise InvalidParamError(style, STYLE)
        self.setStyle(STYLE[style])

    def get_style(self) -> str:
        """Get current font style.

        Possible values are "normal", "italic", "oblique"

        Returns:
            current font style
        """
        return STYLE.inv[self.style()]


if __name__ == "__main__":
    font = Font("Consolas")
