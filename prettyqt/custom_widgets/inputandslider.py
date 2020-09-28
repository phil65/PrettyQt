# -*- coding: utf-8 -*-

from typing import Optional
import pathlib

from qtpy import QtWidgets

from prettyqt import core, widgets


class InputAndSlider(widgets.Widget):

    value_changed = core.Signal(pathlib.Path)

    def __init__(
        self, bounds: Optional[tuple] = None, parent: Optional[QtWidgets.QWidget] = None
    ):
        super().__init__(parent)
        self.path = None
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.spinbox = widgets.SpinBox()
        layout += self.spinbox
        self.slider = widgets.Slider()
        layout += self.slider
        if bounds:
            self.set_range(*bounds)
        self.spinbox.valueChanged.connect(self.slider.set_value)
        self.slider.valueChanged.connect(self.spinbox.set_value)

    def serialize_fields(self):
        return dict(path=self.path)

    # def __setstate__(self, state):
    #     self.__init__(state["extensions"])
    #     self.set_path(state["path"])
    #     self.set_enabled(state.get("enabled", True))

    def set_range(self, min_val: int, max_val: int):
        self.spinbox.set_range(min_val, max_val)
        self.slider.set_range(min_val, max_val)

    def get_value(self) -> int:
        return self.spinbox.get_value()

    def set_value(self, value: int):
        self.spinbox.set_value(value)
        self.slider.set_value(value)

    def is_valid(self) -> bool:
        return self.spinbox.is_valid()

    def set_step_size(self, step_size: int):
        self.spinbox.set_step_size(step_size)
        self.slider.set_step_size(step_size)
        self.slider.setTickInterval(step_size)


if __name__ == "__main__":
    app = widgets.app()
    btn = InputAndSlider()
    btn.set_step_size(2)
    btn.slider.set_tick_position("below")
    btn.set_value(4)
    btn.show()
    app.main_loop()
