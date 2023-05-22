from __future__ import annotations

from prettyqt import core, gui, custom_widgets
from prettyqt.qt import QtCore


class CursorEdit(custom_widgets.EnumComboBox):
    value_changed = core.Signal(gui.Cursor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_enum_class(QtCore.Qt.CursorShape)
        self.currentIndexChanged.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> gui.Cursor:
        shape = super().get_value()
        return gui.Cursor(shape)

    def set_value(self, value: gui.Cursor):
        super().set_value(value.shape())

    value = core.Property(gui.Cursor, get_value, set_value, user=True)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = CursorEdit(window_title="Test")
    widget.set_value(gui.Cursor())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()
