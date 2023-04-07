from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui


class TextObjectMixin(core.ObjectMixin):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def get_format(self) -> gui.TextFormat:
        return gui.TextFormat(self.format())


class TextObject(TextObjectMixin, QtGui.QTextObject):
    pass


if __name__ == "__main__":
    doc = gui.TextDocument()
    obj = TextObject(doc)
