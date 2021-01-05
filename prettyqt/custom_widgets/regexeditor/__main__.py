"""This module contains the editor widget implementation."""

from __future__ import annotations

from prettyqt import widgets
from prettyqt.custom_widgets import regexeditor


def run():
    app = widgets.app()
    widget = regexeditor.RegexEditorWidget()
    widget.show()
    app.main_loop()


if __name__ == "__main__":
    app = widgets.app()
    widget = regexeditor.RegexEditorWidget()
    widget.show()
    app.main_loop()
