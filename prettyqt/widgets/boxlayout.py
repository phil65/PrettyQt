# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
from prettyqt import widgets


MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)

ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                  right=QtCore.Qt.AlignRight,
                  top=QtCore.Qt.AlignTop,
                  bottom=QtCore.Qt.AlignBottom)


class BoxLayout(QtWidgets.QBoxLayout):

    def __init__(self, orientation, parent=None):
        o = self.TopToBottom if orientation == "vertical" else self.LeftToRight
        super().__init__(o, parent)

    def __getitem__(self, index):
        return self.itemAt(index)

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def set_alignment(self, alignment):
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])


if __name__ == "__main__":
    import sys
    app = widgets.Application(sys.argv)
    layout = BoxLayout("vertical")
    widget = widgets.Widget()
    widget.setLayout(layout)
    widget.show()
    app.exec_()
