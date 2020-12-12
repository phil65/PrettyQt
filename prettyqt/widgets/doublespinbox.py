from typing import Optional

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QDoubleSpinBox.__bases__ = (widgets.AbstractSpinBox,)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    value_changed = core.Signal(float)

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        default_value: Optional[float] = None,
    ):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def __setstate__(self, state):
        self.set_range(*state["range"])
        self.setValue(state["value"])
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.setDecimals(state["decimals"])
        self.setSingleStep(state["single_step"])
        self.set_step_type(state["step_type"])
        self.set_correction_mode(state["correction_mode"])
        self.set_button_symbols(state["button_symbols"])

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

    def set_range(self, start, end):
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
