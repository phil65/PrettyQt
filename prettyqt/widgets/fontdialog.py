# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets


class FontDialog(QtWidgets.QFontDialog):

    def current_font(self):
        return gui.Font(self.currentFont())


FontDialog.__bases__[0].__bases__ = (widgets.BaseDialog,)


if __name__ == "__main__":
    app = widgets.app()
    widget = FontDialog.getFont()
    app.exec_()
