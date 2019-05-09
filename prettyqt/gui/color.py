# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class Color(QtGui.QColor):

    def __repr__(self):
        return f"Color({self.red()}, {self.green()}, {self.blue()}, {self.alpha()})"

    def __str__(self):
        return self.name()

    def __reduce__(self):
        return (self.__class__, (self.red(), self.green(), self.blue(), self.alpha()))

    def set_color(self, color):
        if isinstance(color, str):
            self.setNamedColor(color)
        else:
            self.setRgb(*color)

    @classmethod
    def from_text(cls, text):
        """Create a QColor from specified string"""
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

    def as_qt(self):
        return QtGui.QColor(self)
