from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.utils import get_repr


class KeySequenceEdit(widgets.WidgetMixin, widgets.QKeySequenceEdit):
    """Allows to input a QKeySequence."""

    value_changed = core.Signal(gui.QKeySequence)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keySequenceChanged.connect(self._on_value_change)
        self.setClearButtonEnabled(True)

    def __repr__(self):
        return get_repr(self, self.get_value())

    def _on_value_change(self, val):
        self.value_changed.emit(val)

    def set_value(self, value: str | gui.QKeySequence):
        if isinstance(value, str):
            value = gui.KeySequence.fromString(value)
        self.setKeySequence(value)

    def get_value(self) -> gui.QKeySequence:
        return self.keySequence()

    def is_valid(self) -> bool:
        return True

    def get_finishing_key_combinations(self) -> list[core.KeyCombination]:
        return [core.KeyCombination(i) for i in self.finishingKeyCombinations()]

    def get_key_combinations(self) -> list[core.KeyCombination]:
        return [core.KeyCombination(i) for i in self.keySequence()]


if __name__ == "__main__":
    app = widgets.app()
    widget = KeySequenceEdit()
    widget.show()
    app.exec()
