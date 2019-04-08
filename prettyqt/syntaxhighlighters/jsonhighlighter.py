# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui, core


class JsonHighlighter(gui.SyntaxHighlighter):

    def __init__(self, parent=None):
        """ Constructor
        """
        super().__init__(parent)

        self.symbol_format = gui.TextCharFormat()
        self.symbol_format.set_foreground_color("red")
        self.symbol_format.setFontWeight(gui.Font.Bold)

        self.name_format = gui.TextCharFormat()
        self.name_format.set_foreground_color("blue")
        self.name_format.setFontWeight(gui.Font.Bold)
        self.name_format.setFontItalic(True)

        self.value_format = gui.TextCharFormat()
        self.value_format.set_foreground_color("darkgreen")

    def highlightBlock(self, text):
        """ Highlight a block of code using the rules outlined in the Constructor
        """
        expression = core.RegExp("(\\{|\\}|\\[|\\]|\\:|\\,)")
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, self.symbol_format)
            index = expression.indexIn(text, index + length)

        text.replace("\\\"", "  ")

        expression = core.RegExp("\".*\" *\\:")
        expression.setMinimal(True)
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length - 1, self.name_format)
            index = expression.indexIn(text, index + length)

        expression = core.RegExp("\\: *\".*\"")
        expression.setMinimal(True)
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length - 1, self.value_format)
            index = expression.indexIn(text, index + length)
