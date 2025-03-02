from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core, widgets


if TYPE_CHECKING:
    from collections.abc import Sequence


class IntLineEdit(widgets.LineEdit):
    value_changed = core.Signal(int)

    def __init__(self, *args, object_name: str = "int_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_validator("integer", bottom=0, top=1000000000)

    def get_value(self) -> int:
        val = super().get_value()
        return int(val) if val and val.isnumeric() else 0

    def set_value(self, value: int | str):
        super().set_value(str(value))

    value = core.Property(
        int,
        get_value,
        set_value,
        doc="Current Value as integer",
    )


class FloatLineEdit(widgets.LineEdit):
    value_changed = core.Signal(float)

    def __init__(self, *args, object_name: str = "float_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_validator("double", bottom=0.0)

    def get_value(self) -> float:
        val = super().get_value()
        try:
            return float(val)
        except ValueError:
            return 0.0

    def set_value(self, value: float | str):
        super().set_value(str(value))

    value = core.Property(
        float,
        get_value,
        set_value,
        doc="Current Value as float",
    )


class UrlLineEdit(widgets.LineEdit):
    value_changed = core.Signal(core.QUrl)

    def __init__(self, *args, object_name: str = "float_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_validator("website")

    def get_value(self) -> core.QUrl:
        val = super().get_value()
        return core.QUrl.fromUserInput(val)

    def set_value(self, value: core.QUrl | str):
        super().set_value(value.toString() if isinstance(value, core.QUrl) else value)

    value = core.Property(
        core.QUrl,
        get_value,
        set_value,
        doc="Current Value as QUrl",
    )


class StringListEdit(widgets.LineEdit):
    value_changed = core.Signal(list)

    def __init__(self, *args, object_name: str = "str_list_lineedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)

    def _on_value_change(self):
        value = self.get_value()
        self.value_changed.emit(value)

    def get_value(self) -> list[str]:
        val = super().get_value()
        return val.split(",")

    def set_value(self, value: Sequence[str]):
        super().set_value(",".join(value))

    value = core.Property(
        list,
        get_value,
        set_value,
        doc="Current Value as list",
    )


if __name__ == "__main__":
    app = widgets.app()
    widget = FloatLineEdit(window_title="Test")
    widget.set_value("")
    widget.show()
    app.exec()
