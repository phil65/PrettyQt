from typing import Optional

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QDial.__bases__ = (widgets.AbstractSlider,)


class Dial(QtWidgets.QDial):

    value_changed = core.Signal(int)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.valueChanged.connect(self.on_value_change)

    def serialize_fields(self):
        return dict(
            # notch_size=self.notchSize(),
            notch_target=self.notchTarget(),
            notches_visible=self.notchesVisible(),
            wrapping=self.wrapping(),
        )

    def __setstate__(self, state):
        self.set_range(*state["range"])
        self.set_value(state["value"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))
        self.setEnabled(state.get("enabled", True))
        self.setSingleStep(state["single_step"])
        self.setPageStep(state["page_step"])
        self.setTracking(state["has_tracking"])
        self.setInvertedControls(state["inverted_controls"])
        self.setInvertedAppearance(state["inverted_appearance"])
        self.setNotchTarget(state["notch_target"])
        self.setNotchesVisible(state["notches_visible"])
        self.setWrapping(state["wrapping"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()


if __name__ == "__main__":
    app = widgets.app()
    slider = Dial()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()
