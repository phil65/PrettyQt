# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    def __init__(self, path, width=None, parent=None):
        pass

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

    def set_buttons(self, buttons):
        self.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                QtWidgets.QDialogButtonBox.Ok)

    def add_accept_button(self, button):
        self.addButton(button, QtWidgets.QDialogButtonBox.AcceptRole)

    def add_reject_button(self, button):
        self.addButton(button, QtWidgets.QDialogButtonBox.RejectRole)
