# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore


MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)

ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                  right=QtCore.Qt.AlignRight,
                  top=QtCore.Qt.AlignTop,
                  bottom=QtCore.Qt.AlignBottom)


class Layout(QtWidgets.QLayout):

    def __repr__(self):
        return f"{self.__class__.__name__}: {len(self)} children"

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def set_alignment(self, alignment: str):
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment!r} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])
