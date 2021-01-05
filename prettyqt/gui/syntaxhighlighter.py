from __future__ import annotations

from typing import Iterator, Optional, Pattern, Tuple

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui


QtGui.QSyntaxHighlighter.__bases__ = (core.Object,)


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    RULES: list = []

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)  # type: ignore

    @classmethod
    def yield_rules(cls) -> Iterator[Tuple[Pattern, int, gui.TextCharFormat]]:
        for Rule in cls.RULES:
            if isinstance(Rule.compiled, list):
                for i in Rule.compiled:
                    yield (i, Rule.nth, Rule.fmt)
            else:
                yield (Rule.compiled, Rule.nth, Rule.fmt)

    def highlightBlock(self, text: str):
        """Apply syntax highlighting to the given block of text."""
        # Do other syntax formatting
        for expression, nth, fmt in self.yield_rules():
            for match in expression.finditer(text):
                span = match.span(nth)
                self.setFormat(span[0], span[1] - span[0], fmt)
