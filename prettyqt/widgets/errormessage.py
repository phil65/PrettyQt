from __future__ import annotations

from prettyqt import widgets


class ErrorMessage(widgets.DialogMixin, widgets.QErrorMessage):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = ErrorMessage()
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec()
