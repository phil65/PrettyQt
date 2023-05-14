from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class PushButtonMixin(widgets.AbstractButtonMixin):
    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)


class PushButton(PushButtonMixin, QtWidgets.QPushButton):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = PushButton("This is a test")
    widget.show()
    app.main_loop()
