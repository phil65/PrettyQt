from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QDoubleSpinBox.__bases__ = (widgets.AbstractSpinBox,)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    value_changed = core.Signal(float)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        default_value: float | None = None,
    ):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_range(*state["range"])
        self.setValue(state["value"])
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.setDecimals(state["decimals"])
        self.setSingleStep(state["single_step"])
        self.set_step_type(state["step_type"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(
            range=(self.minimum(), self.maximum()),
            prefix=self.prefix(),
            suffix=self.suffix(),
            step_type=self.get_step_type(),
            single_step=self.singleStep(),
            value=self.value(),
            decimals=self.decimals(),
        )

    def set_range(self, start: float | None, end: float | None):
        if start is None:
            start = -float("inf")
        if end is None:
            end = float("inf")
        self.setRange(start, end)


if __name__ == "__main__":
    app = widgets.app()
    widget = DoubleSpinBox()
    widget.show()
    app.main_loop()
