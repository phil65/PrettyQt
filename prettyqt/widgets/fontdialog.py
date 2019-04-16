# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from prettyqt import widgets


class FontDialog(QtWidgets.QFontDialog):
    pass


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = FontDialog.getFont()
    app.exec_()
