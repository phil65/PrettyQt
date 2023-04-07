from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class TextImageFormat(gui.TextCharFormatMixin, QtGui.QTextImageFormat):
    def __bool__(self):
        return self.isValid()


if __name__ == "__main__":
    fmt = TextImageFormat()
    print(bool(fmt))
