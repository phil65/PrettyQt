from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.utils import get_repr


class LocaleEdit(widgets.ComboBox):
    value_changed = core.Signal(core.Locale)

    def __init__(
        self,
        locale: core.QLocale | None = None,
        object_name: str = "locale_edit",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        self._current_locale = core.Locale()
        for i in core.Locale.get_all_locales():
            self.addItem(i.bcp47Name())
        if locale is not None:
            self.set_current_locale(locale)
        self.currentTextChanged.connect(self.set_current_locale)

    def __repr__(self):
        return get_repr(self, self._current_locale)

    def clear(self):
        self._current_locale = core.Locale()
        super().clear()
        for i in core.Locale.get_all_locales():
            self.addItem(i.bcp47Name())

    # def _on_value_change(self):
    #     self._value = self.get_value()
    #     self.value_changed.emit(self._value)

    def set_current_locale(self, locale: core.QLocale | str):
        self._current_locale = core.Locale(locale)
        self.set_current_text(self._current_locale.bcp47Name())

    def is_valid(self) -> bool:
        return self._current_locale.isValid()

    def get_value(self) -> core.QLocale:
        return self._current_locale

    def set_value(self, value: core.QLocale | str):
        self.set_current_locale(value)

    value = core.Property(core.QLocale, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = LocaleEdit(window_title="Test")
    widget.set_value(core.Locale())
    widget.value_changed.connect(print)
    widget.show()
    app.exec()
