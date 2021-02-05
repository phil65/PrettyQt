from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class StringOrNumberWidget(widgets.GroupBox):

    value_changed = core.Signal(object)

    def __init__(self, title: str = "", parent: QtWidgets.QWidget | None = None):
        super().__init__(checkable=False, title=title)
        self.set_layout("vertical")
        self.rb_lineedit = widgets.RadioButton("String")
        self.lineedit = widgets.LineEdit()
        self.rb_spinbox = widgets.RadioButton("Number")
        self.spinbox = widgets.DoubleSpinBox()
        layout_lineedit = widgets.BoxLayout("horizontal")
        layout_lineedit.add(self.rb_lineedit)
        layout_lineedit.add(self.lineedit)
        layout_spinbox = widgets.BoxLayout("horizontal")
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
        self.rb_lineedit.setChecked(True)

    def on_value_change(self):
        value = self.get_value()
        self.value_changed.emit(value)

    def get_value(self) -> float | str:
        if self.rb_spinbox.isChecked():
            val = self.spinbox.get_value()
            return int(val) if val.is_integer() else val
        else:
            return self.lineedit.get_value()

    def set_value(self, value: float | str):
        if isinstance(value, str):
            self.rb_lineedit.setChecked(True)
            self.lineedit.set_value(value)
        elif isinstance(value, (int, float)):
            self.rb_spinbox.setChecked(True)
            self.spinbox.set_value(value)
        else:
            raise TypeError(f"Invalid Type for set_value: {type(value)}")


if __name__ == "__main__":
    app = widgets.app()
    widget = StringOrNumberWidget("Test")
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()
    print(widget.enabled)
