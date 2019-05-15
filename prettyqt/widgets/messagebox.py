# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class MessageBox(QtWidgets.QMessageBox):
    pass


MessageBox.__bases__[0].__bases__ = (widgets.BaseDialog,)


if __name__ == "__main__":
    app = widgets.app()
    widget = MessageBox()
    widget.show()
    app.exec_()
