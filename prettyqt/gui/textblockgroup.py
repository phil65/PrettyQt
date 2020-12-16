from typing import Iterator, List

from qtpy import QtGui

from prettyqt import gui


QtGui.QTextBlockGroup.__bases__ = (gui.TextObject,)


class TextBlockGroup(QtGui.QTextBlockGroup):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __iter__(self) -> Iterator[gui.TextBlock]:
        return iter(gui.TextBlock(i) for i in self.blockList())

    def get_blocklist(self) -> List[gui.TextBlock]:
        return [gui.TextBlock(i) for i in self.blockList()]


if __name__ == "__main__":
    doc = gui.TextDocument()
    group = TextBlockGroup(doc)
    for textblock in group:
        pass
