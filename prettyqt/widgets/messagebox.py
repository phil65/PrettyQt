# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets

from prettyqt import widgets


class MessageBox(QtWidgets.QMessageBox):

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = MessageBox()
    widget.show()
    app.exec_()
