# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

H_ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    center=QtCore.Qt.AlignHCenter)


class GroupBox(QtWidgets.QGroupBox):

    def set_alignment(self):
        self.setAlignment(QtCore.Qt.Vertical)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = GroupBox()
    widget.show()
    app.exec_()
