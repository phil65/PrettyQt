# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui


class MatchHighlighter(gui.SyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self._format_1 = gui.TextCharFormat()
        self._format_1.set_background_color("lightgreen")
        self._format_2 = gui.TextCharFormat()
        self._format_2.set_background_color("lightblue")
        self.spans = []

    def set_spans(self, spans):
        self.spans = spans
        # print(self.spans)
        self.rehighlight()

    def colorize(self, line_pos, match_len, match_num):
        fmt = self._format_1 if match_num % 2 == 0 else self._format_2
        self.setFormat(line_pos, match_len, fmt)

    def highlightBlock(self, text):
        block = self.currentBlock()
        # line_no = block.blockNumber()
        # if line_no == 0:
        #     self.setCurrentBlockState(-1)
        start_char = block.position()
        end_char = start_char + block.length()
        # print(f"\nline {line_no} ({start_char} - {end_char})")
        # print(f"prev block state: {self.previousBlockState()}")
        if not self.spans or not text:
            return None
        for i, (start, end) in enumerate(self.spans):
            match_len = end - start
            starts_in_line = start_char <= start <= end_char
            ends_in_line = start_char <= end <= end_char
            line_pos = start - start_char
            if starts_in_line and ends_in_line:
                # print(f"in line: {line_pos} - {line_pos + match_len}")
                self.colorize(line_pos, match_len, i)
            elif ends_in_line:
                # if self.previousBlockState() == 1:
                # print(f"ends: {end}")
                self.colorize(0, end, i)
                # self.setCurrentBlockState(-1)
            elif starts_in_line:
                # print(f"starts: {line_pos}")
                # self.setCurrentBlockState(1)
                self.colorize(line_pos, end_char, i)
