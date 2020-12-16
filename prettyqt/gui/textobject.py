from qtpy import QtGui

from prettyqt import core, gui


QtGui.QTextObject.__bases__ = (core.Object,)


class TextObject(QtGui.QTextObject):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def get_format(self) -> gui.TextFormat:
        return gui.TextFormat(self.format())


if __name__ == "__main__":
    doc = TextObject()
