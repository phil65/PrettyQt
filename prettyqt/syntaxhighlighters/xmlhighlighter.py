"""Based on http://www.yasinuludag.com/blog/?p=49 ."""

from __future__ import annotations

from prettyqt import core, gui, syntaxhighlighters


class Rule(syntaxhighlighters.HighlightRule):
    pass


class Element(Rule):
    regex = r"\b[A-Za-z0-9_]+(?=[\s/>])"
    color = "blue"


class Attribute(Rule):
    regex = r"\b[A-Za-z0-9_]+(?=\=)"
    color = "darkgreen"
    italic = True


class EqualSign(Rule):
    regex = r"="
    color = "darkgreen"


class LineComment(Rule):
    regex = r"<!--[^\n]*-->"
    color = "lightgrey"


class Text(Rule):
    regex = r">(.+)(?=</)"


class Keyword(Rule):
    regex = [r"\b?xml\b", "/>", ">", "<", "</"]
    bold = True
    color = "red"


VALUE_FORMAT = gui.TextCharFormat()
VALUE_FORMAT.set_foreground_color("orange")
VALUE_START_EXPRESSION = core.RegularExpression(r"\"")
VALUE_END_EXPRESSION = core.RegularExpression(r"\"(?=[\s></])")


class XmlHighlighter(gui.SyntaxHighlighter):

    RULES = Rule.__subclasses__()

    def highlightBlock(self, text: str):
        super().highlightBlock(text)
        # HANDLE QUOTATION MARKS NOW.. WE WANT TO START WITH " AND END WITH "..
        # A THIRD " SHOULD NOT CAUSE THE WORDS INBETWEEN SECOND AND THIRD
        # TO BE COLORED
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = VALUE_START_EXPRESSION.match(text).capturedStart()
        while start_index >= 0:
            match = VALUE_END_EXPRESSION.match(text, start_index)
            end_index = match.capturedStart()
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_len = len(text) - start_index
            else:
                comment_len = end_index - start_index + match.capturedLength()
            self.setFormat(start_index, comment_len, VALUE_FORMAT)
            start_index = VALUE_START_EXPRESSION.match(
                text, start_index + comment_len
            ).capturedStart()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = XmlHighlighter(editor.document())
    editor.show()
    app.main_loop()
