# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets

from prettyqt import widgets


ICONS = bidict(dict(none=QtWidgets.QMessageBox.NoIcon,
                    information=QtWidgets.QMessageBox.Information,
                    warning=QtWidgets.QMessageBox.Warning,
                    critical=QtWidgets.QMessageBox.Critical,
                    question=QtWidgets.QMessageBox.Question))


class MessageBox(QtWidgets.QMessageBox):

    @classmethod
    def message(cls, msg, title=None, msg_type=None):
        m = cls(cls.NoIcon, title, msg)
        m.setIcon(ICONS[msg_type])
        m.exec_()


MessageBox.__bases__[0].__bases__ = (widgets.BaseDialog,)


if __name__ == "__main__":
    app = widgets.app()
    widget = MessageBox.message("Test", "header", "warning")
    widget.show()
    app.exec_()
