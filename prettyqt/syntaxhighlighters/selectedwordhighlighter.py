import re
from typing import TYPE_CHECKING, Literal, cast

from prettyqt import core, gui


if TYPE_CHECKING:
    from prettyqt import widgets


ModeStr = Literal["word", "all"]

PAT = re.compile("\\s+")


class SelectedWordHighlighter(gui.SyntaxHighlighter):
    def __init__(self, parent: gui.QTextDocument | None = None):
        super().__init__(parent)
        self._selection_term = ""
        self._mode = "word"
        self._highlight_format = gui.TextCharFormat()
        self._highlight_format.setBackground(gui.Color(255, 210, 120))
        self._highlight_format.setFontWeight(gui.QFont.Weight.Bold)
        self._highlight_pattern = None
        if parent is None:
            raise TypeError(parent)
        # the document may belong to a prettyqt text edit
        widget = parent.parent()
        self._widget: widgets.PlainTextEdit | None = (
            cast("widgets.PlainTextEdit", widget) if widget is not None else None
        )
        if self._widget is not None and hasattr(self._widget, "selectionChanged"):
            self._widget.selectionChanged.connect(self._filter_selection_for_single_word)

    def set_selection_term(self, term: str):
        if term == self._selection_term:
            return
        self._selection_term = term
        self._update()

    def _update(self):
        escaped = re.escape(self._selection_term)
        match self._mode:
            case "all":
                search_pattern = escaped
            case "word":
                search_pattern = f"\\b{escaped}\\b"
            case _:
                raise ValueError(self._mode)
        self._highlight_pattern = core.RegularExpression(search_pattern)
        self.rehighlight()

    def get_selection_term(self) -> str:
        return self._selection_term

    def set_selection_mode(self, mode: ModeStr):
        if mode == self._mode:
            return
        self._mode = mode
        self._update()

    def get_selection_mode(self) -> ModeStr:
        return self._mode

    def highlightBlock(self, text):
        if len(self._selection_term) > 1:
            self._apply_highlight(text)

    def _apply_highlight(self, text):
        if self._highlight_pattern is None:
            return
        for m in self._highlight_pattern.finditer(text):
            length = m.span()[1] - m.span()[0]
            self.setFormat(m.span()[0], length, self._highlight_format)

    def _filter_selection_for_single_word(self):
        if self._widget is None:
            return
        tc = self._widget.selecter.get_text_cursor()
        current_selection = tc.selectedText()
        if not [p for p in PAT.split(current_selection) if p]:  # SkipEmptyParts
            self.set_selection_term("")
            return
        tc.select_text("start_of_word", "end_of_word")
        term = current_selection if current_selection == tc.selectedText() else ""
        self.set_selection_term(term)

    selectionTerm = core.Property(  # noqa: N815
        str,
        get_selection_term,
        set_selection_term,
        doc="String to highlight in the document",
    )
    selectionMode = core.Property(  # noqa: N815
        str,
        get_selection_mode,
        set_selection_mode,
        doc="Selection mode",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = SelectedWordHighlighter(editor.document())
    editor.set_syntaxhighlighter(highlighter)
    # highlighter = SelectedWordHighlighter(editor.document())
    editor.show()
    app.exec()
