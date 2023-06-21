from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


class MappedCheckBox(widgets.CheckBox):
    def __init__(
        self,
        *args,
        true_value=True,
        false_value=False,
        object_name: str = "mapped_checkbox",
        **kwargs,
    ):
        super().__init__(*args, object_name=object_name, **kwargs)
        dct = {True: true_value, False: false_value}
        self.map = bidict(dct)

    def get_value(self):
        return self.map[self.isChecked()]

    def set_value(self, value):
        val = self.map.inverse[value]
        super().set_value(val)


if __name__ == "__main__":
    app = widgets.app()
    widget = MappedCheckBox("Test")
    widget.show()
    app.exec()
    print(widget.get_value())
