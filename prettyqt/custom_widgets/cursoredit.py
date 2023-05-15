from __future__ import annotations

from prettyqt import core, gui, widgets


class CursorEdit(widgets.Widget):
    value_changed = core.Signal(gui.Cursor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> gui.Cursor:
        return self._value

    def set_value(self, value: gui.Cursor):
        self._value = value

    value = core.Property(gui.Cursor, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = CursorEdit(window_title="Test")
    widget.set_value(gui.Cursor())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()
