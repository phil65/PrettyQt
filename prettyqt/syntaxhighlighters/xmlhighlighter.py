# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
based on http://www.yasinuludag.com/blog/?p=49
"""

from prettyqt import core, gui

HIGHLIGHT_RULES = []

ELEMENT_FORMAT = gui.TextCharFormat()
ELEMENT_FORMAT.set_foreground_color("blue")
HIGHLIGHT_RULES.append((core.RegExp(r"\\b[A-Za-z0-9_]+(?=[\s/>])"), ELEMENT_FORMAT))
ATTR_FORMAT = gui.TextCharFormat()
ATTR_FORMAT.setFontItalic(True)
ATTR_FORMAT.set_foreground_color("lightgreen")
HIGHLIGHT_RULES.append((core.RegExp(r"\\b[A-Za-z0-9_]+(?=\\=)"), ATTR_FORMAT))
HIGHLIGHT_RULES.append((core.RegExp(r"="), ATTR_FORMAT))

LINE_COMMENT_FORMAT = gui.TextCharFormat()
LINE_COMMENT_FORMAT.set_foreground_color("lightgrey")
HIGHLIGHT_RULES.append((core.RegExp(r"<!--[^\n]*-->"), LINE_COMMENT_FORMAT))

TEXT_FORMAT = gui.TextCharFormat()
TEXT_FORMAT.set_foreground_color("black")
# (?<=...)  - lookbehind is not supported
HIGHLIGHT_RULES.append((core.RegExp(r">(.+)(?=</)"), TEXT_FORMAT))

KEYWORD_FORMAT = gui.TextCharFormat()
KEYWORD_FORMAT.set_foreground_color("red")
KEYWORD_FORMAT.setFontWeight(gui.Font.Bold)
KEYWORD_PATTERNS = ["\\b?xml\\b", "/>", ">", "<", "</"]
HIGHLIGHT_RULES += [(core.RegExp(p), KEYWORD_FORMAT) for p in KEYWORD_PATTERNS]

VALUE_FORMAT = gui.TextCharFormat()
VALUE_FORMAT.set_foreground_color("orange")
VALUE_START_EXPRESSION = core.RegExp(r"\"")
VALUE_END_EXPRESSION = core.RegExp(r"\"(?=[\s></])")


class XmlHighlighter(gui.SyntaxHighlighter):

    # VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING

    def highlightBlock(self, text):
        # for every pattern
        for pattern, format in HIGHLIGHT_RULES:
            # Create a regular expression from the retrieved pattern
            expression = core.RegExp(pattern)
            # Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)
            # While the index is greater than 0
            while index >= 0:
                # Get the length of how long the expression is true,
                # set the format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                # Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)

        # HANDLE QUOTATION MARKS NOW.. WE WANT TO START WITH " AND END WITH "..
        # A THIRD " SHOULD NOT CAUSE THE WORDS INBETWEEN SECOND AND THIRD
        # TO BE COLORED
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = VALUE_START_EXPRESSION.indexIn(text)
        while start_index >= 0:
            end_index = VALUE_END_EXPRESSION.indexIn(text, start_index)
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_len = len(text) - start_index
            else:
                matched_len = VALUE_END_EXPRESSION.matchedLength()
                comment_len = end_index - start_index + matched_len
            self.setFormat(start_index, comment_len, VALUE_FORMAT)
            start_index = VALUE_START_EXPRESSION.indexIn(text, start_index + comment_len)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = XmlHighlighter(editor.document())
    editor.show()
    app.exec_()
