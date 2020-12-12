from typing import Optional

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QSpinBox.__bases__ = (widgets.AbstractSpinBox,)


class SpinBox(QtWidgets.QSpinBox):

    value_changed = core.Signal(int)

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        default_value: Optional[int] = None,
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
        self.set_range(*state["range"])
        self.setValue(state["value"])
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))
        self.setSingleStep(state["single_step"])
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.set_button_symbols(state["button_symbols"])
        self.set_correction_mode(state["correction_mode"])
        self.setDisplayIntegerBase(state["int_base"])
        self.set_step_type(state["step_type"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_range(self, start: Optional[int], end: Optional[int]):
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
