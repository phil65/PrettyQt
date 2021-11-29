from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QErrorMessage.__bases__ = (widgets.Dialog,)


class ErrorMessage(QtWidgets.QErrorMessage):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = ErrorMessage()
    widget.set_icon("mdi.timer")
    widget.show()
    app.main_loop()
