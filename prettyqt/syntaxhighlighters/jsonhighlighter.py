from __future__ import annotations

import regex as re

from prettyqt import gui


BRACKETS = re.compile(r"(\{|\}|\[|\]|\:|\,)")
REGEXP1 = re.compile(r"\".*\" *\:")
REGEXP2 = re.compile(r"\: *\".*\"")

SYMBOL_FORMAT = gui.TextCharFormat()
SYMBOL_FORMAT.set_foreground_color("red")
SYMBOL_FORMAT.set_font_weight("bold")

NAME_FORMAT = gui.TextCharFormat()
NAME_FORMAT.set_foreground_color("blue")

VALUE_FORMAT = gui.TextCharFormat()
VALUE_FORMAT.set_foreground_color("darkgreen")


class JsonHighlighter(gui.SyntaxHighlighter):
    def highlightBlock(self, text: str):
        """Highlight a block of code using the rules outlined in the Constructor."""
        for m in BRACKETS.finditer(text):
            self.setFormat(m.span()[0], m.span()[1] - m.span()[0], SYMBOL_FORMAT)

        text.replace('\\"', "  ")
        for m in REGEXP1.finditer(text):
            self.setFormat(m.span()[0], m.span()[1] - m.span()[0], NAME_FORMAT)
        for m in REGEXP2.finditer(text):
            self.setFormat(m.span()[0], m.span()[1] - m.span()[0], VALUE_FORMAT)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = JsonHighlighter(editor.document())
    editor.show()
    app.main_loop()
