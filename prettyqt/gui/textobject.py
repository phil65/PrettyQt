from typing import TYPE_CHECKING

from prettyqt import core, gui
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from prettyqt.qt import QtGui

    _TextObjectBase = QtGui.QTextObject
else:
    _TextObjectBase = object


class TextObjectMixin(core.ObjectMixin, _TextObjectBase):
    def __repr__(self):
        return get_repr(self)

    def get_format(self) -> gui.TextFormat:
        return gui.TextFormat(self.format())


class TextObject(TextObjectMixin, gui.QTextObject):
    pass


if __name__ == "__main__":
    doc = gui.TextDocument()
    obj = TextObject(doc)
