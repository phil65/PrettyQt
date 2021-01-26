from __future__ import annotations

from typing import Any, Dict, Literal, Optional, Union

from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, helpers


SPEC = bidict(
    rgb=QtGui.QColor.Rgb,
    hsv=QtGui.QColor.Hsv,
    cmyk=QtGui.QColor.Cmyk,
    hsl=QtGui.QColor.Hsl,
    extended_rgb=QtGui.QColor.ExtendedRgb,
    invalid=QtGui.QColor.Invalid,
)

SpecStr = Literal["rgb", "hsv", "cmyk", "hsl", "extended_rgb", "invalid"]


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
        return self.name()

    def __reduce__(self):
        return type(self), (self.red(), self.green(), self.blue(), self.alpha())

    def serialize_fields(self):
        return dict(color=self.toString())

    def serialize(self) -> Dict[str, Any]:
        return self.serialize_fields()

    def set_color(self, color: Union[str, tuple]):
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
        colorspace: Optional[SpecStr] = "rgb",
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
