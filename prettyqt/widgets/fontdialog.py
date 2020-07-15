# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QFontDialog.__bases__ = (widgets.BaseDialog,)


class FontDialog(QtWidgets.QFontDialog):
    def get_current_font(self) -> gui.Font:
        return gui.Font(self.currentFont())


if __name__ == "__main__":
    app = widgets.app()
    widget = FontDialog.getFont()
    app.exec_()
