from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class TextObjectMixin(core.ObjectMixin):
    def __repr__(self):
        return get_repr(self)

    def get_format(self) -> gui.TextFormat:
        return gui.TextFormat(self.format())


class TextObject(TextObjectMixin, QtGui.QTextObject):
    pass


if __name__ == "__main__":
    doc = gui.TextDocument()
    obj = TextObject(doc)
