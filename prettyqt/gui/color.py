from __future__ import annotations

from typing import Any, Dict, Union

from prettyqt.qt import QtGui


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

    def as_qt(self) -> QtGui.QColor:
        return QtGui.QColor(self)
