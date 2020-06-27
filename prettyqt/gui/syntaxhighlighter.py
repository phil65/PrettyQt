# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core


QtGui.QSyntaxHighlighter.__bases__ = (core.Object,)


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    RULES = []

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

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, fmt in self.yield_rules():
            index = expression.indexIn(text)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)
