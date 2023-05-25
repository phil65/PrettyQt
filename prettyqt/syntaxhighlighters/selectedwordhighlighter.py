from __future__ import annotations

import re

from prettyqt import core, gui
from prettyqt.qt import QtGui


class SelectedWordHighlighter(gui.SyntaxHighlighter):
    def __init__(self, parent: QtGui.QTextDocument | None = None):
        super().__init__(parent)
        self.selection_term = ""
        self._highlight_format = gui.TextCharFormat()
        self._highlight_format.setBackground(gui.Color(255, 210, 120))
        self._highlight_format.setFontWeight(QtGui.QFont.Weight.Bold)
        self._highlight_pattern = None
        self._widget = parent.parent()
        self._widget.selectionChanged.connect(self.filter_selection_for_single_word)

    def set_selection_term(self, term: str):
        if term == self.selection_term:
            return
        if term:
            term = f"\\b{term}\\b"
            if term == self.selection_term:
                return
        self.selection_term = term
        self._highlight_pattern = core.RegularExpression(self.selection_term)
        self.rehighlight()

    def highlightBlock(self, text):
        if len(self.selection_term) > 1:
            self.apply_highlight(text)

    def apply_highlight(self, text):
        for m in self._highlight_pattern.finditer(text):
            length = m.span()[1] - m.span()[0]
            self.setFormat(m.span()[0], length, self._highlight_format)

    def filter_selection_for_single_word(self):
        tc = self._widget.selecter.get_text_cursor()
        current_selection = tc.selectedText()
        pat = re.compile("\\s+")
        items = pat.split(current_selection)  # SkipEmptyParts
        if not items:
            self.set_selection_term("")
            return
        tc.select_text("start_of_word", "end_of_word")
        term = current_selection if current_selection == tc.selectedText() else ""
        self.set_selection_term(term)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = SelectedWordHighlighter(editor.document())
    editor.set_syntaxhighlighter(highlighter)
    # highlighter = SelectedWordHighlighter(editor.document())
    editor.show()
    app.main_loop()
