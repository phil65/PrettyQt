# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui


class MatchHighlighter(gui.SyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self.prog = None
        self._format = gui.TextCharFormat()
        self._format.set_background_color("lightgreen")

    def set_prog(self, prog):
        self.prog = prog
        self.rehighlight()

    def highlightBlock(self, text):
        if self.prog and text:
            for m in self.prog.finditer(text):
                start, end = m.span()
                self.setFormat(start, end - start, self._format)
