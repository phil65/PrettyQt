from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QSpinBox.__bases__ = (widgets.AbstractSpinBox,)


class SpinBox(QtWidgets.QSpinBox):

    value_changed = core.Signal(int)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        default_value: int | None = None,
    ):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def serialize_fields(self):
        return dict(
            range=(self.minimum(), self.maximum()),
            value=self.value(),
            prefix=self.prefix(),
            suffix=self.suffix(),
            step_type=self.get_step_type(),
            single_step=self.singleStep(),
            int_base=self.displayIntegerBase(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_range(*state["range"])
        self.setValue(state["value"])
        self.setSingleStep(state["single_step"])
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.setDisplayIntegerBase(state["int_base"])
        self.set_step_type(state["step_type"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_range(self, start: int | None, end: int | None):
        if start is None:
            start = -2147483647
        if end is None:
            end = 2147483647
        self.setRange(start, end)

    def set_step_size(self, step_size):
        self.setSingleStep(step_size)


if __name__ == "__main__":
    app = widgets.app()
    widget = SpinBox()
    widget.show()
    app.main_loop()
