from __future__ import annotations

from prettyqt import core, widgets


class StringOrNumberWidget(widgets.GroupBox):
    value_changed = core.Signal(object)

    def __init__(self, *args, object_name: str = "string_or_number_widget", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_layout("vertical")
        self.rb_lineedit = widgets.RadioButton("String", checked=True)
        self.lineedit = widgets.LineEdit()
        self.rb_spinbox = widgets.RadioButton("Number")
        self.spinbox = widgets.DoubleSpinBox()
        layout_lineedit = widgets.HBoxLayout()
        layout_lineedit.add(self.rb_lineedit)
        layout_lineedit.add(self.lineedit)
        layout_spinbox = widgets.HBoxLayout()
        layout_spinbox.add(self.rb_spinbox)
        layout_spinbox.add(self.spinbox)
        self.box.add(layout_lineedit)
        self.box.add(layout_spinbox)
        self.rb_spinbox.toggled.connect(self.spinbox.setEnabled)
        self.rb_spinbox.toggled.connect(self.lineedit.setDisabled)
        self.rb_lineedit.toggled.connect(self.lineedit.setEnabled)
        self.rb_lineedit.toggled.connect(self.spinbox.setDisabled)
        self.spinbox.value_changed.connect(self.on_value_change)
        self.lineedit.value_changed.connect(self.on_value_change)

    def on_value_change(self):
        value = self.get_value()
        self.value_changed.emit(value)

    def get_value(self) -> float | str:
        if not self.rb_spinbox.isChecked():
            return self.lineedit.get_value()
        val = self.spinbox.get_value()
        return int(val) if val.is_integer() else val

    def set_value(self, value: float | str):
        match value:
            case str():
                self.rb_lineedit.setChecked(True)
                self.lineedit.set_value(value)
            case int() | float():
                self.rb_spinbox.setChecked(True)
                self.spinbox.set_value(value)
            case _:
                raise TypeError(f"Invalid Type for set_value: {type(value)}")


if __name__ == "__main__":
    app = widgets.app()
    widget = StringOrNumberWidget("Test")
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()
