from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import get_repr


class KeySequenceEdit(widgets.WidgetMixin, QtWidgets.QKeySequenceEdit):
    value_changed = core.Signal(QtGui.QKeySequence)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keySequenceChanged.connect(self.value_changed)

    def __repr__(self):
        return get_repr(self, self.get_value())

    def set_value(self, value: str):
        seq = gui.KeySequence.fromString(value)
        self.setKeySequence(seq)

    def get_value(self) -> str:
        return self.keySequence().toString()

    def is_valid(self) -> bool:
        return True


if __name__ == "__main__":
    app = widgets.app()
    widget = KeySequenceEdit()
    widget.show()
    app.main_loop()
