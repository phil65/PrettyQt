from __future__ import annotations

from typing import Any, Literal

from typing_extensions import Self

from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr, helpers


SpecStr = Literal["rgb", "hsv", "cmyk", "hsl", "extended_rgb", "invalid"]

SPEC: bidict[SpecStr, QtGui.QColor.Spec] = bidict(
    rgb=QtGui.QColor.Spec.Rgb,
    hsv=QtGui.QColor.Spec.Hsv,
    cmyk=QtGui.QColor.Spec.Cmyk,
    hsl=QtGui.QColor.Spec.Hsl,
    extended_rgb=QtGui.QColor.Spec.ExtendedRgb,
    invalid=QtGui.QColor.Spec.Invalid,
)

NameFormatStr = Literal["hex_rgb", "hex_argb"]
NameStr = NameFormatStr | Literal["svg_rgb", "svg_argb", "qcss_rgb", "qcss_argb"]

NAME_FORMAT: bidict[NameFormatStr, QtGui.QColor.NameFormat] = bidict(
    hex_rgb=QtGui.QColor.NameFormat.HexRgb, hex_argb=QtGui.QColor.NameFormat.HexArgb
)


def is_valid_color(text: str):
    if text.startswith("#") and len(text) in {4, 7} and text[1:].isalnum():
        return True
    return text.lower() in QtGui.QColor.colorNames()


class Color(QtGui.QColor):
    """Colors based on RGB, HSV or CMYK values."""

    def __init__(self, *args):
        match args:
            case (QtGui.QColor(),):
                super().__init__()
                self.setRgba(args[0].rgba())
            case (str(),):
                if not is_valid_color(args[0]):
                    raise ValueError(args[0])
                super().__init__(args[0])
            case _:
                super().__init__(*args)

    def __repr__(self):
        return get_repr(self, self.red(), self.green(), self.blue(), self.alpha())

    def __str__(self):
        return self.name() if self.alpha() == 255 else self.name(self.NameFormat.HexArgb)

    def __reduce__(self):
        return type(self), (self.red(), self.green(), self.blue(), self.alpha())

    def __format__(self, format_spec: NameStr):
        try:
            return self.get_name(format_spec)
        except ValueError:
            return super().__format__(format_spec)

    @property
    def _red(self) -> int:
        return self.red()

    @property
    def _green(self) -> int:
        return self.green()

    @property
    def _blue(self) -> int:
        return self.blue()

    @property
    def _alpha(self) -> int:
        return self.alpha()

    __match_args__ = ("_red", "_green", "_blue", "_alpha")

    def serialize(self) -> dict[str, Any]:
        return dict(color=self.name())

    def set_color(self, color: str | tuple):
        if isinstance(color, str):
            self.setNamedColor(color)
        else:
            self.setRgb(*color)

    @classmethod
    def from_cmyk(cls, c: float, m: float, y: float, k: float, a: float = 1.0) -> Self:
        return cls(cls.fromCmykF(c, m, y, k, a))

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, a: float = 1.0) -> Self:
        return cls(cls.fromHsvF(h, s, v, a))

    # @classmethod
    # def interpolate_color(
    #     cls,
    #     start: QtGui.QColor,
    #     end: QtGui.QColor,
    #     percent: int,
    #     colorspace: SpecStr | QtGui.QColor.Spec = "rgb",
    # ) -> Self:
    #     """Get an interpolated color value.

    #     Args:
    #         start: The start color.
    #         end: The end color.
    #         percent: Which value to get (0 - 100)
    #         colorspace: The desired interpolation color system. If None, take
    #                     system from start color.
    #     Return:
    #         The interpolated QColor, with the same spec as the given start color.
    #     """
    #     def _get_color(colorspace, start, end):
    #         out = cls()
    #         match colorspace:
    #             case "rgb":
    #                 components = helpers.get_color_percentage(
    #                     start.getRgb(), end.getRgb(), percent  # type: ignore
    #                 )
    #                 out.setRgb(*components)
    #             case "hsv":
    #                 components = helpers.get_color_percentage(
    #                     start.getHsv(), end.getHsv(), percent  # type: ignore
    #                 )
    #                 out.setHsv(*components)
    #             case "hsl":
    #                 components = helpers.get_color_percentage(
    #                     start.getHsl(), end.getHsl(), percent  # type: ignore
    #                 )
    #                 out.setHsl(*components)
    #         return out

    #     match colorspace:
    #         case None:
    #             colorspace = SPEC.inverse[start.spec()]
    #             color = _get_color(colorspace, start, end)
    #         case str() | QtGui.QColor.Spec():
    #             colorspace = SPEC.get_str_value(colorspace)
    #             color = _get_color(colorspace, start, end)
    #         case _:
    #             raise ValueError("Invalid colorspace!")
    #     return cls(color.convert_to(colorspace))

    @classmethod
    def interpolate_color(
        cls,
        start: QtGui.QColor,
        end: QtGui.QColor,
        percent: int,
        colorspace: SpecStr | None = "rgb",
    ) -> Self:
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
            return cls(*end.getRgb()) if percent == 100 else cls(*start.getRgb())
        out = cls()
        match colorspace:
            case "rgb":
                components = helpers.get_color_percentage(
                    start.getRgb(), end.getRgb(), percent  # type: ignore
                )
                out.setRgb(*components)
            case "hsv":
                components = helpers.get_color_percentage(
                    start.getHsv(), end.getHsv(), percent  # type: ignore
                )
                out.setHsv(*components)
            case "hsl":
                components = helpers.get_color_percentage(
                    start.getHsl(), end.getHsl(), percent  # type: ignore
                )
                out.setHsl(*components)
            case _:
                raise ValueError("Invalid colorspace!")
        return cls(out.convertTo(start.spec()))

    def is_dark(self) -> bool:
        """Check whether a color is 'dark'."""
        return self.lightness() < 128

    def get_spec(self) -> SpecStr:
        return SPEC.inverse[self.spec()]

    def convert_to(self, spec: SpecStr) -> Self:
        # return Color(self.convertTo(SPEC[spec]))
        color = type(self)()
        match spec:
            case "rgb":
                rgb = self.getRgb()
                color.setRgb(*rgb)
            case "hsv":
                hsv = self.getHsv()
                color.setHsv(*hsv)
            case "cmyk":
                cmyk = self.getCmyk()
                color.setCmyk(*cmyk)
            case "hsl":
                hsl = self.getHsl()
                color.setHsl(*hsl)
            case "extended_rgb":
                ergb = self.getRgbF()
                color.setRgbF(*ergb)
        return color

    def get_name(self, name_format: NameStr = "hex_argb") -> str:
        match name_format:
            case "svg_rgb" | "svg_argb" if not self.isValid():
                return 'fill=""'
            case "svg_rgb":
                return f'fill="rgb({self.red()}, {self.green()}, {self.blue()})"'
            case "svg_argb":
                fill_str = f"rgb({self.red()}, {self.green()}, {self.blue()})"
                return f'fill="{fill_str}" fill-opacity="{self.alpha()}"'
            case "qcss_argb" | "qcss_rgb":
                return self.get_css(fmt="rgba" if name_format == "qcss_argb" else "rgb")
            case _ if name_format in NAME_FORMAT:
                return self.name(NAME_FORMAT[name_format])
            case _:
                raise ValueError(name_format)

    def get_css(self, fmt: Literal["rgb", "rgba", "hsva", "hsla"] | None = None) -> str:
        css_format = fmt or self.spec()
        match css_format:
            case self.Spec.Rgb | "rgba":
                string = ", ".join([str(i) for i in self.getRgb()])
                return f"rgba({string})"
            case self.Spec.Hsv | "hsva":
                string = ", ".join([str(i) for i in self.getHsv()])
                return f"hsva({string})"
            case self.Spec.Hsl | "hsla":
                string = ", ".join([str(i) for i in self.getHsl()])
                return f"hsla({string})"
            case "rgb":
                return f"rgb({self.red()}, {self.green()}, {self.blue()})"
            case _:
                raise ValueError(css_format)

    def as_qt(self) -> QtGui.QColor:
        return self.convertTo(self.spec())

    def inverted(self, invert_alpha: bool = False) -> Self:
        return type(self)(
            255 - self.red(),
            255 - self.green(),
            255 - self.blue(),
            255 - self.alpha() if invert_alpha else self.alpha(),
        )

    def drift(self, factor: int = 1.0) -> Self:
        """Return color that is lighter or darker than the base color."""
        Cls = type(self)
        if self == Color("#000000"):
            return Cls(Color("#050505").lighter(int(factor * 100)))
        elif self.lightness() > 128:
            return Cls(self.darker(int(factor * 100)))
        else:
            return Cls(self.lighter(int(factor * 100)))


# QtGui.QColor.__str__ = __str__
# QtGui.QColor.__reduce__ = __reduce__
# QtGui.QColor.__str__ = __str__
# QtGui.QColor._red = _red
# QtGui.QColor._green = _green
# QtGui.QColor._blue = _blue
# QtGui.QColor._red = _red
# QtGui.QColor.__match_args__ = ("_red", "_green", "_blue", "_alpha")

# QtGui.QColor.serialize = serialize
# QtGui.QColor.set_color = set_color
# QtGui.QColor.from_cmyk = from_cmyk
# QtGui.QColor.from_hsv = from_hsv
# QtGui.QColor.interpolate_color = interpolate_color
# QtGui.QColor.is_dark = is_dark
# QtGui.QColor.get_spec = get_spec
# QtGui.QColor.convert_to = convert_to
# QtGui.QColor.get_name = get_name
# QtGui.QColor.inverted = inverted
# QtGui.QColor.drift = drift

# Color = QtGui.QColor

if __name__ == "__main__":
    color = Color("#FFFFFF")
    color = color.drift(1.3)
