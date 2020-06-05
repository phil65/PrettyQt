# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class Event(QtCore.QEvent):

    def __repr__(self):
        return f"Event({self.type()})"
