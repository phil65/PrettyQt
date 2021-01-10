from __future__ import annotations

from prettyqt.qt import QtGui


class TextLayout(QtGui.QTextLayout):
    def __repr__(self):
        return f"{type(self).__name__}({self.text()!r})"


if __name__ == "__main__":
    layout = TextLayout()
