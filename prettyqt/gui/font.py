from __future__ import annotations

import sys
from typing import Any, Literal, Self

from prettyqt import gui
from prettyqt.utils import bidict, get_repr


CAPITALIZATION = bidict(
    mixed_case=gui.QFont.Capitalization.MixedCase,
    all_uppercase=gui.QFont.Capitalization.AllUppercase,
    all_lowercase=gui.QFont.Capitalization.AllLowercase,
    small_caps=gui.QFont.Capitalization.SmallCaps,
    capitalize=gui.QFont.Capitalization.Capitalize,
)

CapitalizationStr = Literal[
    "mixed_case", "all_uppercase", "all_lowercase", "small_caps", "capitalize"
]

HINTING_PREFERENCE = bidict(
    default=gui.QFont.HintingPreference.PreferDefaultHinting,
    none=gui.QFont.HintingPreference.PreferNoHinting,
    vertical=gui.QFont.HintingPreference.PreferVerticalHinting,
    full=gui.QFont.HintingPreference.PreferFullHinting,
)

HintingPreferenceStr = Literal["default", "none", "vertical", "full"]

SPACING_TYPE = bidict(
    percentage=gui.QFont.SpacingType.PercentageSpacing,
    absolute=gui.QFont.SpacingType.AbsoluteSpacing,
)

SpacingTypeStr = Literal["percentage", "absolute"]

STRETCH = bidict(
    any=gui.QFont.Stretch.AnyStretch,
    ultra_condensed=gui.QFont.Stretch.UltraCondensed,
    extra_condensed=gui.QFont.Stretch.ExtraCondensed,
    condensed=gui.QFont.Stretch.Condensed,
    semi_condensed=gui.QFont.Stretch.SemiCondensed,
    unstretched=gui.QFont.Stretch.Unstretched,
    semi_expanded=gui.QFont.Stretch.SemiExpanded,
    expanded=gui.QFont.Stretch.Expanded,
    extra_expanded=gui.QFont.Stretch.ExtraExpanded,
    ultra_expanded=gui.QFont.Stretch.UltraExpanded,
)

StretchStr = Literal[
    "any",
    "ultra_condensed",
    "extra_condensed",
    "condensed",
    "semi_condensed",
    "unstretched",
    "semi_expanded",
    "expanded",
    "extra_expanded",
    "ultra_expanded",
]

STYLE = bidict(
    normal=gui.QFont.Style.StyleNormal,
    italic=gui.QFont.Style.StyleItalic,
    oblique=gui.QFont.Style.StyleOblique,
)

StyleStr = Literal["normal", "italic", "oblique"]

STYLE_STRATEGY = bidict(
    prefer_default=gui.QFont.StyleStrategy.PreferDefault,
    prefer_bitmap=gui.QFont.StyleStrategy.PreferBitmap,
    prefer_device=gui.QFont.StyleStrategy.PreferDevice,
    prefer_outline=gui.QFont.StyleStrategy.PreferOutline,
    force_outline=gui.QFont.StyleStrategy.ForceOutline,
    no_antialias=gui.QFont.StyleStrategy.NoAntialias,
    so_subpixel_antialias=gui.QFont.StyleStrategy.NoSubpixelAntialias,
    prefer_antialias=gui.QFont.StyleStrategy.PreferAntialias,
    no_font_merging=gui.QFont.StyleStrategy.NoFontMerging,
    prefer_no_shaping=gui.QFont.StyleStrategy.PreferNoShaping,
)  # ORed with PreferMatch, PreferQuality, ForceIntegerMetrics

StyleStrategyStr = Literal[
    "prefer_default",
    "prefer_bitmap",
    "prefer_device",
    "prefer_outline",
    "force_outline",
    "no_antialias",
    "so_subpixel_antialias",
    "prefer_antialias",
    "no_font_merging",
    "prefer_no_shaping",
]

STYLE_HINTS = bidict(
    any=gui.QFont.StyleHint.AnyStyle,
    sans_serif=gui.QFont.StyleHint.SansSerif,
    serif=gui.QFont.StyleHint.Serif,
    typewriter=gui.QFont.StyleHint.TypeWriter,
    decorative=gui.QFont.StyleHint.Decorative,
    monospace=gui.QFont.StyleHint.Monospace,
    fantasy=gui.QFont.StyleHint.Fantasy,
    cursive=gui.QFont.StyleHint.Cursive,
    system=gui.QFont.StyleHint.System,
)

StyleHintStr = Literal[
    "any",
    "sans_serif",
    "serif",
    "typewriter",
    "decorative",
    "monospace",
    "fantasy",
    "cursive",
    "system",
]

WEIGHT = bidict(
    thin=gui.QFont.Weight.Thin,
    extra_light=gui.QFont.Weight.ExtraLight,
    light=gui.QFont.Weight.Light,
    normal=gui.QFont.Weight.Normal,
    medium=gui.QFont.Weight.Medium,
    demi_bold=gui.QFont.Weight.DemiBold,
    bold=gui.QFont.Weight.Bold,
    extra_bold=gui.QFont.Weight.ExtraBold,
    black=gui.QFont.Weight.Black,
)

WeightStr = Literal[
    "thin",
    "extra_light",
    "light",
    "normal",
    "medium",
    "demi_bold",
    "bold",
    "extra_bold",
    "black",
]


class Font(gui.QFont):
    """Specifies a query for a font used for drawing text."""

    def __repr__(self):
        return get_repr(
            self, self.family(), self.pointSize(), self.weight(), self.italic()
        )

    def __getstate__(self):
        return dict(
            family=self.family(),
            pointsize=self.pointSize(),
            weight=self.weight(),
            italic=self.italic(),
        )

    def __setstate__(self, state):
        self.setFamily(state["family"])
        if state["pointsize"] > -1:
            self.setPointSize(state["pointsize"])
        self.setWeight(state["weight"])
        self.setItalic(state["italic"])

    @property
    def _family(self) -> str:
        return self.family()

    __match_args__ = ("_family",)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize(self) -> dict[str, Any]:
        return self.__getstate__()

    @property
    def metrics(self) -> gui.FontMetrics:
        return gui.FontMetrics(self)

    def set_size(self, size: int):
        self.setPointSize(size)

    @classmethod
    def mono(cls, size=8, as_qt: bool = False) -> Self:
        match sys.platform:
            case "win32":
                font = "Consolas"
            case "darwin":
                font = "Menlo"
            case _:
                font = "Monospace"
        if as_qt:
            return gui.QFont(font)
        return cls(font, size)
        # font.setStyleHint()

    def scaled(self, factor: float) -> Self:
        scaled = type(self)(self)
        if self.pointSizeF() != -1:
            scaled.setPointSizeF(self.pointSizeF() * factor)
        elif self.pixelSize() != -1:
            scaled.setPixelSize(int(self.pixelSize() * factor))
        return scaled

    def set_style_hint(self, hint: StyleHintStr | gui.QFont.StyleHint):
        """Set the style hint.

        Args:
            hint: style hint
        """
        self.setStyleHint(STYLE_HINTS.get_enum_value(hint))

    def set_weight(self, weight: WeightStr | gui.QFont.Weight):
        """Set the font weight.

        Args:
            weight: font weight
        """
        self.setWeight(WEIGHT.get_enum_value(weight))

    def get_weight(self) -> WeightStr:
        """Get current font weight.

        Returns:
            current font weight
        """
        return WEIGHT.inverse[self.weight()]

    def set_capitalization(
        self, capitalization: CapitalizationStr | gui.Font.Capitalization
    ):
        """Set the font capitalization.

        Args:
            capitalization: font capitalization
        """
        self.setCapitalization(CAPITALIZATION.get_enum_value(capitalization))

    def get_capitalization(self) -> CapitalizationStr:
        """Get current font capitalization.

        Returns:
            current font capitalization
        """
        return CAPITALIZATION.inverse[self.capitalization()]

    def set_hinting_preference(
        self, preference: HintingPreferenceStr | gui.Font.HintingPreference
    ):
        """Set the hinting preference.

        Args:
            preference: hinting preference
        """
        self.setHintingPreference(HINTING_PREFERENCE.get_enum_value(preference))

    def get_hinting_preference(self) -> HintingPreferenceStr:
        """Get current hinting preference.

        Returns:
            current hinting preference
        """
        return HINTING_PREFERENCE.inverse[self.hintingPreference()]

    def set_letter_spacing(
        self, typ: SpacingTypeStr | gui.Font.SpacingType, spacing: float
    ):
        """Set the letter spacing.

        Args:
            typ: letter spacing type
            spacing: spacing
        """
        self.setLetterSpacing(SPACING_TYPE.get_enum_value(typ), spacing)

    def get_letter_spacing_type(self) -> SpacingTypeStr:
        """Get current letter spacing type.

        Returns:
            current letter spacing type
        """
        return SPACING_TYPE.inverse[self.letterSpacingType()]

    def set_style(self, style: StyleStr | gui.Font.Style):
        """Set the font style.

        Args:
            style: font style
        """
        self.setStyle(STYLE.get_enum_value(style))

    def get_style(self) -> StyleStr:
        """Get current font style.

        Returns:
            current font style
        """
        return STYLE.inverse[self.style()]

    def set_family(self, family: str, fallback: str | None = None):
        """Set the font family.

        Args:
            family: font family
            fallback: fallback font family
        """
        self.setFamily(family)
        font_info = gui.FontInfo(self)
        if fallback is not None and font_info.family() != family:
            self.setFamily(fallback)


if __name__ == "__main__":
    font = Font("Consolas")
