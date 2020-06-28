# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, gui, syntaxhighlighters

KEYWORDS = [
    "and", "assert", "break", "continue", "class", "def"
    "del", "elif", "else", "except", "exec", "finally",
    "for", "from", "global", "if", "import", "in",
    "is", "lambda", "not", "or", "pass", "print",
    "raise", "return", "try", "while", "yield",
    "None", "True", "False",
]

OPERATORS = [
    "=",
    "==", "!=", "<", "<=", ">", ">=",
    r"\+", "-", r"\*", "/", "//", r"\%", r"\*\*",
    r"\+=", "-=", r"\*=", "/=", r"\%=",
    r"\^", r"\|", r"\&", r"\~", ">>", "<<",
]


class Rule(syntaxhighlighters.HighlightRule):
    pass


class Keyword(Rule):
    regex = r"\b%s\b" % r"\b|\b".join(KEYWORDS)
    color = gui.Color(200, 120, 50)
    bold = True


class Operator(Rule):
    regex = r"%s" % "|".join(OPERATORS)
    color = gui.Color(150, 150, 150)


class Bracket(Rule):
    regex = r"[\[\]\{\}\(\)]"
    color = "darkgray"


class Self(Rule):
    regex = r"\bself\b"
    color = gui.Color(150, 85, 140)
    italic = True


class String(Rule):
    regex = [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]
    color = gui.Color(20, 110, 100)


class Def(Rule):
    regex = r"\bdef\b\s*(\w+)"
    color = gui.Color(20, 20, 255)
    bold = True
    nth = 1


class Class(Rule):
    regex = r"\bclass\b\s*(\w+)"
    color = gui.Color(20, 20, 255)
    bold = True
    nth = 1


class Comment(Rule):
    regex = r"#[^\n]*"
    color = "lightgray"


class Number(Rule):
    regex = [r"\b[+-]?[0-9]+[lL]?\b",
             r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b",
             r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"]
    color = gui.Color(100, 150, 190)


# Multi-line strings (expression, flag, style)
# FIXME: The triple-quotes in these two lines will mess up the
# syntax highlighting from this point onward
fmt = gui.TextCharFormat()
fmt.set_foreground_color([30, 120, 110])
TRI_SINGLE = (core.RegExp("'''"), 1, fmt)
TRI_DOUBLE = (core.RegExp('"""'), 2, fmt)


class PythonHighlighter(gui.SyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    RULES = Rule.__subclasses__()

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        super().highlightBlock(text)
        self.setCurrentBlockState(0)
        # Do multi-line strings
        if not self.match_multiline(text, *TRI_SINGLE):
            self.match_multiline(text, *TRI_DOUBLE)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``core.RegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
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
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        return self.currentBlockState() == in_state


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = PythonHighlighter(editor.document())
    editor.show()
    app.exec_()
