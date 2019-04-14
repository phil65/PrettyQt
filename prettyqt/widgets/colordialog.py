# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class ColorDialog(QtWidgets.QColorDialog):
    pass


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = ColorDialog()
    widget.show()
    app.exec_()
