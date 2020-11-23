# -*- coding: utf-8 -*-

from typing import List

from qtpy import QtGui

from prettyqt import gui

QtGui.QTextBlockGroup.__bases__ = (gui.TextObject,)


class TextBlockGroup(QtGui.QTextBlockGroup):
    def __repr__(self):
        return "TextBlockGroup()"

    def __iter__(self):
        return iter(gui.TextBlock(i) for i in self.blockList())

    def get_blocklist(self) -> List[gui.TextBlock]:
        return [gui.TextBlock(i) for i in self.blockList()]


if __name__ == "__main__":
    doc = gui.TextDocument()
    group = TextBlockGroup(doc)
    for textblock in group:
        pass
