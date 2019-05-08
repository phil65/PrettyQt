# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class IntValidator(QtGui.QIntValidator):

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top())

    def __setstate__(self, state):
        super().__init__()
        self.setRange(state["bottom"], state["top"])


if __name__ == "__main__":
    val = IntValidator()
    val.setRange(0, 9)
