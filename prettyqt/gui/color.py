from __future__ import annotations

from typing import Any, Dict, Optional, Union

from prettyqt.qt import QtGui
from prettyqt.utils import helpers


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
    def from_cmyk(cls, *args, **kwargs) -> Color:
        return cls(cls.fromCmykF(*args, **kwargs))

    @classmethod
    def interpolate_color(
        cls,
        start: QtGui.QColor,
        end: QtGui.QColor,
        percent: int,
        colorspace: Optional[QtGui.QColor.Spec] = QtGui.QColor.Rgb,
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

        out = cls()
        if colorspace == cls.Rgb:
            components = helpers.get_color_percentage(
                start.getRgb(), end.getRgb(), percent  # type: ignore
            )
            out.setRgb(*components)
        elif colorspace == cls.Hsv:
            components = helpers.get_color_percentage(
                start.getHsv(), end.getHsv(), percent  # type: ignore
            )
            out.setHsv(*components)
        elif colorspace == cls.Hsl:
            components = helpers.get_color_percentage(
                start.getHsl(), end.getHsl(), percent  # type: ignore
            )
            out.setHsl(*components)
        else:
            raise ValueError("Invalid colorspace!")
        out = out.convertTo(start.spec())
        return out

    def as_qt(self) -> QtGui.QColor:
        return QtGui.QColor(self)
