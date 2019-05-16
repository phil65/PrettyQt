# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class MdiSubWindow(QtWidgets.QMdiSubWindow):
    pass


MdiSubWindow.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiSubWindow()
    widget.show()
    app.exec_()
