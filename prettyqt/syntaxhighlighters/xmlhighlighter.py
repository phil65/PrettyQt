# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
based on http://www.yasinuludag.com/blog/?p=49
"""

from prettyqt import core, gui


class XmlHighlighter(gui.SyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlight_rules = []

        xmlElementFormat = gui.TextCharFormat()
        xmlElementFormat.set_foreground_color("blue")
        self.highlight_rules.append((core.RegExp(r"\\b[A-Za-z0-9_]+(?=[\s/>])"),
                                     xmlElementFormat))
        xml_attr_format = gui.TextCharFormat()
        xml_attr_format.setFontItalic(True)
        xml_attr_format.set_foreground_color("lightgreen")
        self.highlight_rules.append((core.RegExp(r"\\b[A-Za-z0-9_]+(?=\\=)"),
                                     xml_attr_format))
        self.highlight_rules.append((core.RegExp(r"="), xml_attr_format))

        self.valueFormat = gui.TextCharFormat()
        self.valueFormat.set_foreground_color("orange")
        self.valueStartExpression = core.RegExp(r"\"")
        self.valueEndExpression = core.RegExp(r"\"(?=[\s></])")

        singleLineCommentFormat = gui.TextCharFormat()
        singleLineCommentFormat.set_foreground_color("lightgrey")
        self.highlight_rules.append((core.RegExp(r"<!--[^\n]*-->"),
                                     singleLineCommentFormat))

        textFormat = gui.TextCharFormat()
        textFormat.set_foreground_color("black")
        # (?<=...)  - lookbehind is not supported
        self.highlight_rules.append((core.RegExp(r">(.+)(?=</)"), textFormat))

        keywordFormat = gui.TextCharFormat()
        keywordFormat.set_foreground_color("red")
        keywordFormat.setFontWeight(gui.Font.Bold)
        keywordPatterns = ["\\b?xml\\b", "/>", ">", "<", "</"]
        self.highlight_rules += [(core.RegExp(pattern), keywordFormat)
                                 for pattern in keywordPatterns]

    # VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING

    def highlightBlock(self, text):
        # for every pattern
        for pattern, format in self.highlight_rules:
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
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.valueStartExpression.indexIn(text)
        while startIndex >= 0:
            endIndex = self.valueEndExpression.indexIn(text, startIndex)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                matched_len = self.valueEndExpression.matchedLength()
                commentLength = endIndex - startIndex + matched_len
            self.setFormat(startIndex, commentLength, self.valueFormat)
            startIndex = self.valueStartExpression.indexIn(text,
                                                           startIndex + commentLength)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = XmlHighlighter(editor.document())
    editor.show()
    app.exec_()
