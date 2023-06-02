from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtCore


class IntLineEdit(widgets.LineEdit):
    value_changed = core.Signal(int)

    def __init__(self, *args, object_name: str = "int_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_validator("integer", bottom=0, top=1000000000)

    def _on_value_change(self):
        value = self.get_value()
        self._set_validation_color(None)
        self.value_changed.emit(value)

    def get_value(self) -> int:
        val = super().get_value()
        return int(val) if val and val.isnumeric() else 0

    def set_value(self, value: int | str):
        super().set_value(str(value))


class FloatLineEdit(widgets.LineEdit):
    value_changed = core.Signal(float)

    def __init__(self, *args, object_name: str = "float_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_validator("double", bottom=0.0)

    def _on_value_change(self):
        value = self.get_value()
        self._set_validation_color(None)
        self.value_changed.emit(value)

    def get_value(self) -> float:
        val = super().get_value()
        try:
            return float(val)
        except ValueError:
            return 0.0

    def set_value(self, value: float | str):
        super().set_value(str(value))


class UrlLineEdit(widgets.LineEdit):
    value_changed = core.Signal(QtCore.QUrl)

    def __init__(self, *args, object_name: str = "float_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_validator("website")

    def _on_value_change(self):
        value = self.get_value()
        self._set_validation_color(None)
        self.value_changed.emit(value)

    def get_value(self) -> QtCore.QUrl:
        val = super().get_value()
        return QtCore.QUrl.fromUserInput(val)

    def set_value(self, value: QtCore.QUrl | str):
        super().set_value(value.toString() if isinstance(value, QtCore.QUrl) else value)


if __name__ == "__main__":
    app = widgets.app()
    widget = FloatLineEdit(window_title="Test")
    widget.set_value("")
    widget.show()
    app.main_loop()
