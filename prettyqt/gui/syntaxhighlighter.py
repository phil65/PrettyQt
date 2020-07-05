# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtGui

from prettyqt import core


QtGui.QSyntaxHighlighter.__bases__ = (core.Object,)


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    RULES: list = []

    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def yield_rules(cls):
        for Rule in cls.RULES:
            if isinstance(Rule.compiled, list):
                for i in Rule.compiled:
                    yield (i, Rule.nth, Rule.format)
            else:
                yield (Rule.compiled, Rule.nth, Rule.format)

    def highlightBlock(self, text: str):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, fmt in self.yield_rules():
            for match in expression.finditer(text):
                span = match.span(nth)
                self.setFormat(span[0], span[1] - span[0], fmt)
