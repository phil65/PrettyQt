# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QErrorMessage.__bases__ = (widgets.BaseDialog,)


class ErrorMessage(QtWidgets.QErrorMessage):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = ErrorMessage()
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec_()
