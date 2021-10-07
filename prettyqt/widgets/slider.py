from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


TICK_POSITION = bidict(
    none=QtWidgets.QSlider.TickPosition.NoTicks,
    both_sides=QtWidgets.QSlider.TickPosition.TicksBothSides,
    above=QtWidgets.QSlider.TickPosition.TicksAbove,
    below=QtWidgets.QSlider.TickPosition.TicksBelow,
)

TickPositionAllStr = Literal["none", "both_sides", "above", "below", "left", "right"]
TickPositionStr = Literal["none", "both_sides", "above", "below"]


QtWidgets.QSlider.__bases__ = (widgets.AbstractSlider,)


class Slider(QtWidgets.QSlider):

    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: (constants.OrientationStr | QtCore.Qt.Orientation) = "horizontal",
        parent: QtWidgets.QWidget | None = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)
        self.valueChanged.connect(self.on_value_change)

    def serialize_fields(self):
        return dict(
            tick_position=self.get_tick_position(),
            tick_interval=self.tickInterval(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_tick_position(state["tick_position"])
        self.setTickInterval(state["tick_interval"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_tick_position(self, position: TickPositionAllStr):
        """Set the tick position for the slider.

        For vertical orientation, "above" equals to "left" and "below" to "right".

        Args:
            position: position for the ticks
        """
        if position == "left":
            position = "above"
        elif position == "right":
            position = "below"
        elif position not in TICK_POSITION:
            raise InvalidParamError(position, TICK_POSITION)
        self.setTickPosition(TICK_POSITION[position])

    def get_tick_position(self) -> TickPositionStr:
        """Return tick position.

        Returns:
            tick position
        """
        return TICK_POSITION.inverse[self.tickPosition()]
        # if self.is_vertical():
        #     if val == "above":
        #         return "left"
        #     elif val == "below":
        #         return "right"


if __name__ == "__main__":
    app = widgets.app()
    slider = Slider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()
