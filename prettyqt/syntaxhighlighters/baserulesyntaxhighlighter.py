from __future__ import annotations

from collections.abc import Iterator
from re import Pattern

from prettyqt import gui


class BaseRuleSyntaxHighlighter(gui.SyntaxHighlighter):
    RULES: list = []

    @classmethod
    def iter_rules(cls) -> Iterator[tuple[Pattern, int, gui.TextCharFormat]]:
        for rule in cls.RULES:
            if isinstance(rule.compiled, list):
                for i in rule.compiled:
                    yield (i, rule.nth, rule.fmt)
            else:
                yield (rule.compiled, rule.nth, rule.fmt)

    def highlightBlock(self, text: str):
        """Apply syntax highlighting to the given block of text."""
        # Do other syntax formatting
        for expression, nth, fmt in self.iter_rules():
            for match in expression.finditer(text):
                span = match.span(nth)
                self.setFormat(span[0], span[1] - span[0], fmt)
