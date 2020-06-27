# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import syntaxhighlighters, core, gui

BASE_FONT = 12


class Rule(syntaxhighlighters.HighlightRule):
    font_size = BASE_FONT


class Link(Rule):
    regex = r'\[(.+)\]\(([^ ]+)( "(.+)")?\)'
    color = '#61AFE9'


class Image(Rule):
    regex = r'\!\[(.+)\]\(([^ ]+)( "(.+)")?\)'
    color = '#2B65D1'


class Heading1(Rule):
    regex = r"^#[^\n]*"
    color = "#E06C75"
    bold = True
    font_size = BASE_FONT * 2


class Heading2(Rule):
    regex = r"^##[^\n]*"
    color = "#E06C75"
    bold = True
    font_size = BASE_FONT * 1.5


class Heading3(Rule):
    regex = r"^###[^\n]*"
    color = "#E06C75"
    bold = True
    font_size = BASE_FONT * 1.17


class Heading4(Rule):
    regex = r"^####[^\n]*"
    color = "#E06C75"
    bold = True
    font_size = BASE_FONT


class Heading5(Rule):
    regex = r"^#####[^\n]*"
    color = "#E06C75"
    bold = True
    font_size = BASE_FONT * 0.83


class Heading6(Rule):
    regex = r"^######[^\n]*"
    color = "#E06C75"
    bold = True
    font_size = BASE_FONT * 0.67


class Emphasis(Rule):
    regex = r"(\*)([^\*]+)\1"
    color = "#BC78DD"
    italic = True


class Strong(Rule):
    regex = r"(\*{2})([^\*\*]+)\1"
    color = "#D19A66"
    bold = True


class Code(Rule):
    regex = [r"`[^`]*`", r"^((?:(?:[ ]{4}|\t).*(\R|$))+)"]
    color = "grey"


TRI_SINGLE = (core.RegExp("```"), Code.get_format())


class MarkdownHighlighter(gui.SyntaxHighlighter):

    RULES = Rule.__subclasses__()

    def highlightBlock(self, text):
        super().highlightBlock(text)
        self.setCurrentBlockState(0)
        self.match_multiline(text, *TRI_SINGLE)

    def match_multiline(self, text, delimiter, style):
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == 1:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start + add
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = MarkdownHighlighter(editor.document())
    editor.show()
    app.exec_()
