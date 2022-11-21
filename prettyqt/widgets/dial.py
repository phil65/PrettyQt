from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QDial.__bases__ = (widgets.AbstractSlider,)


class Dial(QtWidgets.QDial):

    value_changed = core.Signal(int)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
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
        super().__setstate__(state)
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
