from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtWidgets


class PlainTextDocumentLayout(
    gui.AbstractTextDocumentLayoutMixin, QtWidgets.QPlainTextDocumentLayout
):
    pass


if __name__ == "__main__":
    doc = gui.TextDocument()
    layout = PlainTextDocumentLayout(doc)
