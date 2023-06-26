from __future__ import annotations

import sys
from typing import Any, Literal

from typing_extensions import Self

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


CAPITALIZATION = bidict(
    mixed_case=QtGui.QFont.Capitalization.MixedCase,
    all_uppercase=QtGui.QFont.Capitalization.AllUppercase,
    all_lowercase=QtGui.QFont.Capitalization.AllLowercase,
    small_caps=QtGui.QFont.Capitalization.SmallCaps,
    capitalize=QtGui.QFont.Capitalization.Capitalize,
)

CapitalizationStr = Literal[
    "mixed_case", "all_uppercase", "all_lowercase", "small_caps", "capitalize"
]

HINTING_PREFERENCE = bidict(
    default=QtGui.QFont.HintingPreference.PreferDefaultHinting,
    none=QtGui.QFont.HintingPreference.PreferNoHinting,
    vertical=QtGui.QFont.HintingPreference.PreferVerticalHinting,
    full=QtGui.QFont.HintingPreference.PreferFullHinting,
)

HintingPreferenceStr = Literal["default", "none", "vertical", "full"]

SPACING_TYPE = bidict(
    percentage=QtGui.QFont.SpacingType.PercentageSpacing,
    absolute=QtGui.QFont.SpacingType.AbsoluteSpacing,
)

SpacingTypeStr = Literal["percentage", "absolute"]

STRETCH = bidict(
    any=QtGui.QFont.Stretch.AnyStretch,
    ultra_condensed=QtGui.QFont.Stretch.UltraCondensed,
    extra_condensed=QtGui.QFont.Stretch.ExtraCondensed,
    condensed=QtGui.QFont.Stretch.Condensed,
    semi_condensed=QtGui.QFont.Stretch.SemiCondensed,
    unstretched=QtGui.QFont.Stretch.Unstretched,
    semi_expanded=QtGui.QFont.Stretch.SemiExpanded,
    expanded=QtGui.QFont.Stretch.Expanded,
    extra_expanded=QtGui.QFont.Stretch.ExtraExpanded,
    ultra_expanded=QtGui.QFont.Stretch.UltraExpanded,
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
    normal=QtGui.QFont.Style.StyleNormal,
    italic=QtGui.QFont.Style.StyleItalic,
    oblique=QtGui.QFont.Style.StyleOblique,
)

StyleStr = Literal["normal", "italic", "oblique"]

STYLE_STRATEGY = bidict(
    prefer_default=QtGui.QFont.StyleStrategy.PreferDefault,
    prefer_bitmap=QtGui.QFont.StyleStrategy.PreferBitmap,
    prefer_device=QtGui.QFont.StyleStrategy.PreferDevice,
    prefer_outline=QtGui.QFont.StyleStrategy.PreferOutline,
    force_outline=QtGui.QFont.StyleStrategy.ForceOutline,
    no_antialias=QtGui.QFont.StyleStrategy.NoAntialias,
    so_subpixel_antialias=QtGui.QFont.StyleStrategy.NoSubpixelAntialias,
    prefer_antialias=QtGui.QFont.StyleStrategy.PreferAntialias,
    no_font_merging=QtGui.QFont.StyleStrategy.NoFontMerging,
    prefer_no_shaping=QtGui.QFont.StyleStrategy.PreferNoShaping,
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
    any=QtGui.QFont.StyleHint.AnyStyle,
    sans_serif=QtGui.QFont.StyleHint.SansSerif,
    serif=QtGui.QFont.StyleHint.Serif,
    typewriter=QtGui.QFont.StyleHint.TypeWriter,
    decorative=QtGui.QFont.StyleHint.Decorative,
    monospace=QtGui.QFont.StyleHint.Monospace,
    fantasy=QtGui.QFont.StyleHint.Fantasy,
    cursive=QtGui.QFont.StyleHint.Cursive,
    system=QtGui.QFont.StyleHint.System,
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
    thin=QtGui.QFont.Weight.Thin,
    extra_light=QtGui.QFont.Weight.ExtraLight,
    light=QtGui.QFont.Weight.Light,
    normal=QtGui.QFont.Weight.Normal,
    medium=QtGui.QFont.Weight.Medium,
    demi_bold=QtGui.QFont.Weight.DemiBold,
    bold=QtGui.QFont.Weight.Bold,
    extra_bold=QtGui.QFont.Weight.ExtraBold,
    black=QtGui.QFont.Weight.Black,
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


class Font(QtGui.QFont):
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
            return QtGui.QFont(font)
        else:
            return cls(font, size)
        # font.setStyleHint()

    def scaled(self, factor: float) -> Self:
        scaled = type(self)(self)
        if self.pointSizeF() != -1:
            scaled.setPointSizeF(self.pointSizeF() * factor)
        elif self.pixelSize() != -1:
            scaled.setPixelSize(int(self.pixelSize() * factor))
        return scaled

    def set_style_hint(self, hint: StyleHintStr | QtGui.QFont.StyleHint):
        """Set the style hint.

        Args:
            hint: style hint
        """
        self.setStyleHint(STYLE_HINTS.get_enum_value(hint))

    def set_weight(self, weight: WeightStr | QtGui.QFont.Weight):
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
