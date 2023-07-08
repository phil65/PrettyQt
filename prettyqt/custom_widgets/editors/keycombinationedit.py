from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.utils import datatypes, get_repr


class KeyCombinationEdit(widgets.WidgetMixin, widgets.QKeySequenceEdit):
    value_changed = core.Signal(core.QKeyCombination)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumSequenceLength(1)

    def __repr__(self):
        return get_repr(self, self.get_value())

    def _on_value_change(self, val):
        self.value_changed.emit(val[0])

    def set_value(self, value: datatypes.KeyCombinationType):
        if not isinstance(value, gui.QKeySequence):
            value = gui.KeySequence(value)
        if len(value) == 0:
            self.clear()
        else:
            self.setKeySequence(gui.KeySequence(value[0]))

    def get_value(self) -> str:
        seq = self.keySequence()
        return seq[0].toString() if seq.count() > 0 else ""

    def is_valid(self) -> bool:
        return True


if __name__ == "__main__":
    app = widgets.app()
    widget = KeyCombinationEdit()
    widget.set_value("")
    widget.show()
    app.exec()
