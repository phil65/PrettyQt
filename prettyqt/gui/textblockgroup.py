from __future__ import annotations

from collections.abc import Iterator

from prettyqt import gui
from prettyqt.qt import QtGui


QtGui.QTextBlockGroup.__bases__ = (gui.TextObject,)


class TextBlockGroup(QtGui.QTextBlockGroup):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __iter__(self) -> Iterator[gui.TextBlock]:
        return iter(gui.TextBlock(i) for i in self.blockList())

    def get_blocklist(self) -> list[gui.TextBlock]:
        return [gui.TextBlock(i) for i in self.blockList()]


if __name__ == "__main__":
    doc = gui.TextDocument()
    group = TextBlockGroup(doc)
    for textblock in group:
        pass
