from qtpy import QtGui

from prettyqt import gui


QtGui.QTextImageFormat.__bases__ = (gui.TextCharFormat,)


class TextImageFormat(QtGui.QTextImageFormat):
    def __bool__(self):
        return self.isValid()


if __name__ == "__main__":
    fmt = TextImageFormat()
    print(bool(fmt))
