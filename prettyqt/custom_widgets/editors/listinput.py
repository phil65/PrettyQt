from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.utils import helpers


class ListInput(widgets.LineEdit):
    value_changed = core.Signal(list)

    def __init__(
        self,
        value: list[float] | str = "",
        typ: type = int,
        allow_single: bool = False,
        object_name: str = "list_input",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        match typ:
            case __builtins__.int:
                self.set_validator("int_list", allow_single=allow_single)
            case __builtins__.float:
                self.set_validator("float_list", allow_single=allow_single)
            case _:
                raise ValueError(f"Invalid type {typ}")
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
