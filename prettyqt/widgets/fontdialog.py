from __future__ import annotations

from prettyqt import gui, widgets


class FontDialog(widgets.DialogMixin, widgets.QFontDialog):
    """Dialog widget for selecting a font."""

    def get_current_font(self) -> gui.Font:
        return gui.Font(self.currentFont())


if __name__ == "__main__":
    app = widgets.app()
    widget = FontDialog.getFont()
    app.exec()
