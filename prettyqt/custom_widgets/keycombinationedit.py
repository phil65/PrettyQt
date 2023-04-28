from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import get_repr


class KeyCombinationEdit(widgets.WidgetMixin, QtWidgets.QKeySequenceEdit):
    value_changed = core.Signal(QtCore.QKeyCombination)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumSequenceLength(1)

    def __repr__(self):
        return get_repr(self, self.get_value())

    def _on_value_change(self, val):
        self.value_changed.emit(val[0])

    def set_value(self, value: str | QtCore.QKeyCombination):
        if isinstance(value, str):
            seq = gui.KeySequence.fromString(value)
        else:
            seq = gui.KeySequence(value)
        if len(seq) == 0:
            self.clear()
        else:
            self.setKeySequence(gui.KeySequence(seq[0]))

    def get_value(self) -> str:
        seq = self.keySequence()
        if len(seq) > 0:
            return seq[0].toString()
        return ""

    def is_valid(self) -> bool:
        return True


if __name__ == "__main__":
    app = widgets.app()
    widget = KeyCombinationEdit()
    widget.set_value("")
    widget.show()
    app.main_loop()
