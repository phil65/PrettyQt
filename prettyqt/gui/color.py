from qtpy import QtGui


class Color(QtGui.QColor):
    def __init__(self, *args, **kwargs):
        # PySide2 workaround
        if len(args) == 1 and isinstance(args[0], Color):
            super().__init__(str(args[0]))
        else:
            super().__init__(*args, **kwargs)

    def __repr__(self):
        return (
            f"{type(self).__name__}({self.red()}, {self.green()}, "
            f"{self.blue()}, {self.alpha()})"
        )

    def __str__(self):
        return self.name()

    def __reduce__(self):
        return self.__class__, (self.red(), self.green(), self.blue(), self.alpha())

    def serialize_fields(self):
        return dict(color=self.toString())

    def serialize(self):
        return self.serialize_fields()

    def set_color(self, color):
        if isinstance(color, str):
            self.setNamedColor(color)
        else:
            self.setRgb(*color)

    @classmethod
    def from_text(cls, text):
        """Create a QColor from specified string."""
        color = cls()
        text = str(text)
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
    def from_cmyk(cls, *args, **kwargs):
        return cls(cls.fromCmykF(*args, **kwargs))

    def as_qt(self) -> QtGui.QColor:
        return QtGui.QColor(self)
