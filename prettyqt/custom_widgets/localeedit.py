from __future__ import annotations

from prettyqt import core, widgets


class LocaleEdit(widgets.Widget):
    value_changed = core.Signal(core.Locale)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Locale:
        return self._value

    def set_value(self, value: core.Locale):
        self._value = value

    value = core.Property(core.Locale, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = LocaleEdit(window_title="Test")
    widget.set_value(core.Locale())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()
