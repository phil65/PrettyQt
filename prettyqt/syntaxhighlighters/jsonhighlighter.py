# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, gui


BRACKETS = core.RegularExpression("(\\{|\\}|\\[|\\]|\\:|\\,)")
REGEXP1 = core.RegularExpression("\".*\" *\\:")
REGEXP2 = core.RegularExpression("\\: *\".*\"")

SYMBOL_FORMAT = gui.TextCharFormat()
SYMBOL_FORMAT.set_foreground_color("red")
SYMBOL_FORMAT.set_font_weight("bold")

NAME_FORMAT = gui.TextCharFormat()
NAME_FORMAT.set_foreground_color("blue")

VALUE_FORMAT = gui.TextCharFormat()
VALUE_FORMAT.set_foreground_color("darkgreen")


class JsonHighlighter(gui.SyntaxHighlighter):

    def highlightBlock(self, text):
        """ Highlight a block of code using the rules outlined in the Constructor
        """
        for index, length in BRACKETS.matches_in_text(text):
            self.setFormat(index, length, SYMBOL_FORMAT)

        text.replace("\\\"", "  ")
        for index, length in REGEXP1.matches_in_text(text):
            self.setFormat(index, length, NAME_FORMAT)
        for index, length in REGEXP2.matches_in_text(text):
            self.setFormat(index, length, VALUE_FORMAT)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = JsonHighlighter(editor.document())
    editor.show()
    app.exec_()
