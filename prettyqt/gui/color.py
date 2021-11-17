from __future__ import annotations

from typing import Any, Literal

from deprecated import deprecated

from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, helpers, types


SPEC = bidict(
    rgb=QtGui.QColor.Spec.Rgb,
    hsv=QtGui.QColor.Spec.Hsv,
    cmyk=QtGui.QColor.Spec.Cmyk,
    hsl=QtGui.QColor.Spec.Hsl,
    extended_rgb=QtGui.QColor.Spec.ExtendedRgb,
    invalid=QtGui.QColor.Spec.Invalid,
)

SpecStr = Literal["rgb", "hsv", "cmyk", "hsl", "extended_rgb", "invalid"]

NAME_FORMAT = bidict(
    hex_rgb=QtGui.QColor.NameFormat.HexRgb, hex_argb=QtGui.QColor.NameFormat.HexArgb
)

NameFormatStr = Literal["hex_rgb", "hex_argb"]
NameStr = Literal["hex_rgb", "hex_argb", "svg_rgb", "svg_argb", "qcss_rgb", "qcss_argb"]


class Color(QtGui.QColor):
    def __init__(self, *args):
        # PySide2 workaround
        if len(args) == 1:
            if isinstance(args[0], QtGui.QColor):
                super().__init__(args[0].name())
            elif isinstance(args[0], str):
                super().__init__()
                self.set_color(args[0])
            else:
                super().__init__(*args)
        else:
            super().__init__(*args)

    def __repr__(self):
        return (
            f"{type(self).__name__}({self.red()}, {self.green()}, "
            f"{self.blue()}, {self.alpha()})"
        )

    def __str__(self):
        return self.name() if self.alpha() == 255 else self.name(self.NameFormat.HexArgb)

    def __reduce__(self):
        return type(self), (self.red(), self.green(), self.blue(), self.alpha())

    def serialize_fields(self):
        return dict(color=self.toString())

    def serialize(self) -> dict[str, Any]:
        return self.serialize_fields()

    def set_color(self, color: str | tuple):
        if isinstance(color, str):
            self.setNamedColor(color)
        else:
            self.setRgb(*color)

    @classmethod
    def from_text(cls, text: str) -> Color:
        """Create a QColor from specified string."""
        color = cls()
        if text.startswith("#") and len(text) == 7:
            correct = "#0123456789abcdef"
            for char in text:
                if char.lower() not in correct:
                    return color
        elif text not in list(cls.colorNames()):
            return color
        color.setNamedColor(text)
        return color

    @classmethod
    def from_cmyk(cls, c: float, m: float, y: float, k: float, a: float = 1.0) -> Color:
        return cls(cls.fromCmykF(c, m, y, k, a))

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, a: float = 1.0) -> Color:
        return cls(cls.fromHsvF(h, s, v, a))

    @classmethod
    def interpolate_color(
        cls,
        start: QtGui.QColor,
        end: QtGui.QColor,
        percent: int,
        colorspace: SpecStr | None = "rgb",
    ) -> Color:
        """Get an interpolated color value.

        Args:
            start: The start color.
            end: The end color.
            percent: Which value to get (0 - 100)
            colorspace: The desired interpolation color system,
                        QColor::{Rgb,Hsv,Hsl} (from QColor::Spec enum)
                        If None, start is used except when percent is 100.

        Return:
            The interpolated QColor, with the same spec as the given start color.
        """
        if colorspace is None:
            if percent == 100:
                return cls(*end.getRgb())
            else:
                return cls(*start.getRgb())
        if colorspace not in SPEC:
            raise InvalidParamError(colorspace, SPEC)
        out = cls()
        if colorspace == "rgb":
            components = helpers.get_color_percentage(
                start.getRgb(), end.getRgb(), percent  # type: ignore
            )
            out.setRgb(*components)
        elif colorspace == "hsv":
            components = helpers.get_color_percentage(
                start.getHsv(), end.getHsv(), percent  # type: ignore
            )
            out.setHsv(*components)
        elif colorspace == "hsl":
            components = helpers.get_color_percentage(
                start.getHsl(), end.getHsl(), percent  # type: ignore
            )
            out.setHsl(*components)
        else:
            raise ValueError("Invalid colorspace!")
        out = out.convertTo(start.spec())
        return out

    def is_dark(self) -> bool:
        """Check whether a color is 'dark'."""
        return self.lightness() < 128

    def get_name(self, name_format: NameStr = "hex_argb") -> str:
        if name_format == "svg_rgb":
            if not self.isValid():
                return 'fill=""'
            return f'fill="rgb({self.red()}, {self.green()}, {self.blue()})"'
        elif name_format == "svg_argb":
            if not self.isValid():
                return 'fill=""'
            fill_str = f"rgb({self.red()}, {self.green()}, {self.blue()})"
            return f'fill="{fill_str}" fill-opacity="{self.alpha()}"'
        elif name_format == "qcss_argb":
            return f"rgba({self.red()}, {self.green()}, {self.blue()}, {self.alpha()})"
        elif name_format == "qcss_rgb":
            return f"rgb({self.red()}, {self.green()}, {self.blue()})"
        else:
            return self.name(NAME_FORMAT[name_format])

    @deprecated(reason="This method is deprecated, use Color.get_name instead.")
    def to_qsscolor(self) -> str:
        """Convert Color to a string that can be used in a QStyleSheet."""
        return f"rgba({self.red()}, {self.green()}, {self.blue()}, {self.alpha()})"

    def as_qt(self) -> QtGui.QColor:
        return QtGui.QColor(self)

    def inverted(self, invert_alpha: bool = False) -> Color:
        return Color(
            255 - self.red(),
            255 - self.green(),
            255 - self.blue(),
            255 - self.alpha() if invert_alpha else self.alpha(),
        )

    @classmethod
    def drift_color(cls, color: types.ColorAndBrushType, factor: int = 110):
        """Return color that is lighter or darker than the base color.

        If base_color.lightness is higher than 128, the returned color is darker
        otherwise is is lighter.
        :param base_color: The base color to drift from
        ;:param factor: drift factor (%)
        :return A lighter or darker color.
        """
        base_color = cls(color)
        if base_color.lightness() > 128:
            return base_color.darker(factor)
        else:
            if base_color == Color("#000000"):
                return cls.drift_color(cls("#101010"), factor + 20)
            else:
                return base_color.lighter(factor + 10)
