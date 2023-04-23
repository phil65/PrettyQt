from __future__ import annotations

import contextlib

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class TextLayout(QtGui.QTextLayout):
    def __repr__(self):
        return get_repr(self, self.text())

    @contextlib.contextmanager
    def process_layout(self):
        self.beginLayout()
        yield self
        self.endLayout()

    def get_text_option(self) -> gui.TextOption:
        return gui.TextOption(self.textOption())


if __name__ == "__main__":
    layout = TextLayout()
