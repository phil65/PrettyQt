from __future__ import annotations

from typing import Callable

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class PushButtonMixin:

    value_changed = core.Signal(bool)

    def __init__(
        self,
        label: str | None = None,
        parent: QtWidgets.QWidget | None = None,
        callback: Callable | None = None,
    ):
        if label is None:
            label = ""
        super().__init__(label, parent)
        if callback:
            self.clicked.connect(callback)
        self.toggled.connect(self.value_changed)


class PushButton(PushButtonMixin, QtWidgets.QPushButton, widgets.AbstractButton):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = PushButton("This is a test")
    widget.show()
    app.main_loop()
