from __future__ import annotations

import builtins

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
            case builtins.int:
                self.set_validator("int_list", allow_single=allow_single)
            case builtins.float:
                self.set_validator("float_list", allow_single=allow_single)
            case _:
                msg = f"Invalid type {typ}"
                raise ValueError(msg)
        self.set_value(value)

    def get_value(self) -> list[float | int]:  # type: ignore[override]
        # TODO: is this best place to deal with exception?
        try:
            return helpers.string_to_num_array(self.text())
        except ValueError:
            return []

    def set_value(self, value: list[float] | str):
        if isinstance(value, list):
            value = str(value)[1:-1].replace(" ", "")
        self.set_text(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = ListInput(typ=int)
    widget.show()
    app.exec()
