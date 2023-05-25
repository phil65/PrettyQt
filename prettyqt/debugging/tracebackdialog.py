from __future__ import annotations

from prettyqt import gui, widgets


class TracebackDialog(widgets.Dialog):
    """A dialog box that shows Python traceback."""

    def __init__(self, parent):
        super().__init__(parent, window_title="Traceback")
        layout = widgets.VBoxLayout()
        self.setLayout(layout)
        self._text = widgets.TextEdit(self, read_only=True, line_wrap_mode="none")
        self._text.setFontFamily(gui.Font.mono().family())
        layout.addWidget(self._text)
        self.resize(600, 400)

    def setText(self, text: str):
        """Always set text as a HTML text."""
        self._text.setHtml(text)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    wnd = TracebackDialog()
    wnd.show()
    with app.debug_mode():
        app.main_loop()
