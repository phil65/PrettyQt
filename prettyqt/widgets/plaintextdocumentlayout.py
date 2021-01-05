from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtWidgets


QtWidgets.QPlainTextDocumentLayout.__bases__ = (gui.AbstractTextDocumentLayout,)


class PlainTextDocumentLayout(QtWidgets.QPlainTextDocumentLayout):
    def serialize_fields(self):
        return dict(cursor_width=self.cursorWidth())


if __name__ == "__main__":
    doc = gui.TextDocument()
    layout = PlainTextDocumentLayout(doc)
    print(len(layout))
