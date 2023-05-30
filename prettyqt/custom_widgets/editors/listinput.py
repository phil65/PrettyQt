from __future__ import annotations

from prettyqt import custom_validators, widgets
from prettyqt.utils import helpers


class ListInput(widgets.LineEdit):
    def __init__(
        self,
        value: list[float] | str = "",
        typ: type = int,
        allow_single: bool = False,
        object_name: str = "list_input",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        if typ is int:
            val = custom_validators.IntListValidator(allow_single=allow_single)
        elif typ is float:
            val = custom_validators.FloatListValidator(allow_single=allow_single)
        else:
            raise ValueError(f"Invalid type {typ}")
        self.set_validator(val)
        self.set_value(value)

    def get_value(self) -> list[float]:  # type: ignore[override]
        return helpers.string_to_num_array(self.text())

    def set_value(self, value: list[float] | str):
        if isinstance(value, list):
            value = str(value)[1:-1].replace(" ", "")
        self.set_text(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = ListInput()
    widget.show()
    app.main_loop()
