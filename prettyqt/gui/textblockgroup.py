from __future__ import annotations

from collections.abc import Iterator

from prettyqt import gui
from prettyqt.utils import get_repr


class TextBlockGroup(gui.TextObjectMixin, gui.QTextBlockGroup):
    def __repr__(self):
        return get_repr(self)

    def __iter__(self) -> Iterator[gui.TextBlock]:
        return iter(gui.TextBlock(i) for i in self.blockList())

    def get_blocklist(self) -> list[gui.TextBlock]:
        return [gui.TextBlock(i) for i in self.blockList()]


if __name__ == "__main__":
    doc = gui.TextDocument()
    group = TextBlockGroup(doc)
