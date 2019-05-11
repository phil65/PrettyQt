# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets


class FontDialog(QtWidgets.QFontDialog):

    def current_font(self):
        return gui.Font(self.currentFont())


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = FontDialog.getFont()
    app.exec_()
