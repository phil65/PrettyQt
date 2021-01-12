from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QRadioButton.__bases__ = (widgets.AbstractButton,)


class RadioButton(QtWidgets.QRadioButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)


if __name__ == "__main__":
    app = widgets.app()
    widget = RadioButton("This is a test")
    widget.set_icon("mdi.timer")
    widget.show()
    app.main_loop()
