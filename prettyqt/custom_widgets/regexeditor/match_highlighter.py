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
        self.matches = []

    def set_prog(self, prog):
        self.prog = prog
        text = self.document().toPlainText()
        if self.prog is not None:
            self.matches = [m.span() for m in self.prog.finditer(text)]
            # print(self.matches)
        self.rehighlight()

    def highlightBlock(self, text):
        block = self.currentBlock()
        # line_no = block.blockNumber()
        # if line_no == 0:
        #     self.setCurrentBlockState(-1)
        start_char = block.position()
        end_char = start_char + block.length()
        # print(f"\nline {line_no} ({start_char} - {end_char})")
        # print(f"prev block state: {self.previousBlockState()}")
        if not self.matches or not text:
            return None
        for start, end in self.matches:
            match_len = end - start
            starts_in_line = start_char <= start <= end_char
            ends_in_line = start_char <= end <= end_char
            line_pos = start - start_char
            if starts_in_line and ends_in_line:
                # print(f"in line: {line_pos} - {line_pos + match_len}")
                self.setFormat(line_pos, line_pos + match_len, self._format)
            elif ends_in_line:
                # if self.previousBlockState() == 1:
                # print(f"ends: {end}")
                self.setFormat(0, end, self._format)
                self.setCurrentBlockState(-1)
            elif starts_in_line:
                # print(f"starts: {line_pos}")
                self.setCurrentBlockState(1)
                self.setFormat(line_pos, end_char, self._format)
