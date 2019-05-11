# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

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

ROLES = dict(invalid=QtWidgets.QDialogButtonBox.InvalidRole,
             accept=QtWidgets.QDialogButtonBox.AcceptRole,
             reject=QtWidgets.QDialogButtonBox.RejectRole,
             destructive=QtWidgets.QDialogButtonBox.DestructiveRole,
             action=QtWidgets.QDialogButtonBox.ActionRole,
             help=QtWidgets.QDialogButtonBox.HelpRole,
             yes=QtWidgets.QDialogButtonBox.YesRole,
             no=QtWidgets.QDialogButtonBox.NoRole,
             apply=QtWidgets.QDialogButtonBox.ApplyRole,
             reset=QtWidgets.QDialogButtonBox.ResetRole)


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    def __len__(self):
        return len(self.buttons())

    def __getitem__(self, index):
        return self.button(BUTTONS[index])

    def __iter__(self):
        return iter(self.buttons())

    def __contains__(self, item):
        return self[item] is not None

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
        self.addButton(button, self.AcceptRole)

    def add_reject_button(self, button):
        self.addButton(button, self.RejectRole)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DialogButtonBox()
    buttons = list(BUTTONS.keys())
    widget.add_buttons(buttons)
    widget.show()
    app.exec_()
