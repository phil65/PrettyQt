# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

BUTTONS = dict(cancel=QtWidgets.QDialogButtonBox.Cancel,
               ok=QtWidgets.QDialogButtonBox.Ok,
               save=QtWidgets.QDialogButtonBox.Save,
               open=QtWidgets.QDialogButtonBox.Open,
               close=QtWidgets.QDialogButtonBox.Close,
               discard=QtWidgets.QDialogButtonBox.Discard,
               apply=QtWidgets.QDialogButtonBox.Apply,
               reset=QtWidgets.QDialogButtonBox.Reset,
               restore_defaults=QtWidgets.QDialogButtonBox.RestoreDefaults,
               help=QtWidgets.QDialogButtonBox.Help,
               save_all=QtWidgets.QDialogButtonBox.SaveAll,
               yes=QtWidgets.QDialogButtonBox.Yes,
               yes_to_all=QtWidgets.QDialogButtonBox.YesToAll,
               no=QtWidgets.QDialogButtonBox.No,
               no_to_all=QtWidgets.QDialogButtonBox.NoToAll,
               abort=QtWidgets.QDialogButtonBox.Abort,
               retry=QtWidgets.QDialogButtonBox.Retry,
               ignore=QtWidgets.QDialogButtonBox.Ignore)


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

    def add_buttons(self, buttons):
        for btn in buttons:
            if btn not in BUTTONS:
                raise ValueError("button type not available")
            self.addButton(BUTTONS[btn])

    def add_accept_button(self, button):
        self.addButton(button, QtWidgets.QDialogButtonBox.AcceptRole)

    def add_reject_button(self, button):
        self.addButton(button, QtWidgets.QDialogButtonBox.RejectRole)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = DialogButtonBox()
    buttons = list(BUTTONS.keys())
    widget.add_buttons(buttons)
    widget.show()
    app.exec_()
