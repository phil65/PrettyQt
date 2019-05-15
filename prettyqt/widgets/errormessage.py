# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class ErrorMessage(QtWidgets.QErrorMessage):
    pass


ErrorMessage.__bases__[0].__bases__ = (widgets.BaseDialog,)


if __name__ == "__main__":
    app = widgets.app()
    widget = ErrorMessage()
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec_()
