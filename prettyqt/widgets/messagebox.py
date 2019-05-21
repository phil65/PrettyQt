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
    def message(cls, msg, title=None, icon=None):
        m = cls(cls.NoIcon, title, msg)
        m.set_icon(icon)
        m.exec_()

    def set_icon(self, icon):
        if icon in ICONS:
            self.setIcon(ICONS[icon])
            return None
        super().set_icon(icon)


MessageBox.__bases__[0].__bases__ = (widgets.BaseDialog,)


if __name__ == "__main__":
    app = widgets.app()
    widget = MessageBox.message("Test", "header", "warning")
    widget.show()
    app.exec_()
