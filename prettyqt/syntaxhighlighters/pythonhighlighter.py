# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import core, gui


def return_format(color, style=""):
    """
    Return a QTextCharFormat with the given attributes.
    """
    fmt = gui.TextCharFormat()
    fmt.set_foreground_color(color)
    if "bold" in style:
        fmt.set_font_weight("bold")
    if "italic" in style:
        fmt.setFontItalic(True)

    return fmt


# Syntax styles that can be shared by all languages

STYLES = {
    "keyword": return_format([200, 120, 50], "bold"),
    "operator": return_format([150, 150, 150]),
    "brace": return_format("darkGray"),
    "defclass": return_format([20, 20, 255], "bold"),
    "string": return_format([20, 110, 100]),
    "string2": return_format([30, 120, 110]),
    "comment": return_format([128, 128, 128]),
    "self": return_format([150, 85, 140], "italic"),
    "numbers": return_format([100, 150, 190]),
}

KEYWORDS = [
    "and", "assert", "break", "class", "continue", "def",
    "del", "elif", "else", "except", "exec", "finally",
    "for", "from", "global", "if", "import", "in",
    "is", "lambda", "not", "or", "pass", "print",
    "raise", "return", "try", "while", "yield",
    "None", "True", "False",
]

# Python operators
OPERATORS = [
    "=",
    # Comparison
    "==", "!=", "<", "<=", ">", ">=",
    # Arithmetic
    r"\+", "-", r"\*", "/", "//", r"\%", r"\*\*",
    # In-place
    r"\+=", "-=", r"\*=", "/=", r"\%=",
    # Bitwise
    r"\^", r"\|", r"\&", r"\~", ">>", "<<",
]

# Python braces
BRACES = [
    r"\{", r"\}", r"\(", r"\)", r"\[", r"\]",
]


class PythonHighlighter(gui.SyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """

    # Python keywords

    def __init__(self, parent=None):
        super().__init__(parent)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (core.RegExp("'''"), 1, STYLES["string2"])
        self.tri_double = (core.RegExp('"""'), 2, STYLES["string2"])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r"\b%s\b" % w, 0, STYLES["keyword"])
                  for w in KEYWORDS]
        rules += [(r"%s" % o, 0, STYLES["operator"])
                  for o in OPERATORS]
        rules += [(r"%s" % b, 0, STYLES["brace"])
                  for b in BRACES]

        # All other rules
        rules += [
            # 'self'
            (r"\bself\b", 0, STYLES["self"]),
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES["string"]),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES["string"]),
            # 'def' followed by an identifier
            (r"\bdef\b\s*(\w+)", 1, STYLES["defclass"]),
            # 'class' followed by an identifier
            (r"\bclass\b\s*(\w+)", 1, STYLES["defclass"]),
            # From '#' until a newline
            (r"#[^\n]*", 0, STYLES["comment"]),
            # Numeric literals
            (r"\b[+-]?[0-9]+[lL]?\b", 0, STYLES["numbers"]),
            (r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b", 0, STYLES["numbers"]),
            (r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b", 0, STYLES["numbers"]),
        ]

        # Build a core.RegExp for each pattern
        self.rules = [(core.RegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, fmt in self.rules:
            index = expression.indexIn(text)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        if not self.match_multiline(text, *self.tri_single):
            self.match_multiline(text, *self.tri_double)

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
