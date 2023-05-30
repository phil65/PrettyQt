from __future__ import annotations

from prettyqt import core, gui, widgets


class IconEdit(widgets.Widget):
    value_changed = core.Signal(gui.Icon)

    def __init__(self, *args, object_name: str = "icon_edit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> gui.Icon:
        return self._value

    def set_value(self, value: gui.Icon):
        self._value = value

    value = core.Property(gui.Icon, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = IconEdit(window_title="Test")
    widget.set_value(gui.Icon())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()
