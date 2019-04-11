# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class ToolTip(QtWidgets.QToolTip):

    def set_formatted_text(self, text, linebreak_px=400):
        self.setText(f'<div style="max-width: {linebreak_px}px">{text}</div>')
