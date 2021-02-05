"""Contains the quick reference widget."""
from __future__ import annotations

import pathlib

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class QuickRefWidget(widgets.Widget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.resize(608, 353)
        self.gridLayout = widgets.GridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.textedit_quickref = widgets.TextEdit(parent=self)
        self.textedit_quickref.setReadOnly(True)
        self.textedit_quickref.setObjectName("textedit_quickref")
        self.gridLayout.addWidget(self.textedit_quickref, 0, 0, 1, 1)
        html_file = pathlib.Path("ref.html")
        text = html_file.read_text()
        self.textedit_quickref.setHtml(text)

    def _show_context_menu(self, pos):
        self.context_menu.exec_(self.textedit_quickref.mapToGlobal(pos))


if __name__ == "__main__":
    app = widgets.app()
    widget = QuickRefWidget()
    widget.show()
    app.main_loop()
