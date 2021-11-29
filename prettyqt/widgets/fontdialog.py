from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QFontDialog.__bases__ = (widgets.Dialog,)


class FontDialog(QtWidgets.QFontDialog):
    def get_current_font(self) -> gui.Font:
        return gui.Font(self.currentFont())


if __name__ == "__main__":
    app = widgets.app()
    widget = FontDialog.getFont()
    app.main_loop()
