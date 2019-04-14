# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, gui


class JsonHighlighter(gui.SyntaxHighlighter):

    def __init__(self, parent=None):
        """ Constructor
        """
        super().__init__(parent)

        self.symbol_format = gui.TextCharFormat()
        self.symbol_format.set_foreground_color("red")
        self.symbol_format.set_font_weight("bold")

        self.name_format = gui.TextCharFormat()
        self.name_format.set_foreground_color("blue")
        self.name_format.set_font_weight("bold")
        self.name_format.setFontItalic(True)

        self.value_format = gui.TextCharFormat()
        self.value_format.set_foreground_color("darkgreen")

    def highlightBlock(self, text):
        """ Highlight a block of code using the rules outlined in the Constructor
        """
        expression = core.RegExp("(\\{|\\}|\\[|\\]|\\:|\\,)")
        for index, length in expression.matches_in_text(text):
            self.setFormat(index, length, self.symbol_format)

        text.replace("\\\"", "  ")

        expression = core.RegExp("\".*\" *\\:")
        expression.setMinimal(True)
        for index, length in expression.matches_in_text(text):
            self.setFormat(index, length, self.name_format)

        expression = core.RegExp("\\: *\".*\"")
        expression.setMinimal(True)
        for index, length in expression.matches_in_text(text):
            self.setFormat(index, length, self.value_format)
