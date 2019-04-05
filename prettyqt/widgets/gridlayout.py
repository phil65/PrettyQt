# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from prettyqt import widgets


MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)


class GridLayout(QtWidgets.QGridLayout):

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    layout = GridLayout()
    widget = widgets.Widget()
    widget.setLayout(layout)
    widget.show()
    app.exec_()
