from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


TICK_POSITION = bidict(
    none=QtWidgets.QSlider.TickPosition.NoTicks,
    both_sides=QtWidgets.QSlider.TickPosition.TicksBothSides,
    above=QtWidgets.QSlider.TickPosition.TicksAbove,
    below=QtWidgets.QSlider.TickPosition.TicksBelow,
)

TickPositionAllStr = Literal["none", "both_sides", "above", "below", "left", "right"]
TickPositionStr = Literal["none", "both_sides", "above", "below"]


class Slider(widgets.AbstractSliderMixin, QtWidgets.QSlider):
    value_changed = core.Signal(int)
    clicked = core.Signal(int)

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
        # self.setStyle(HollowHandleStyle())

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.clicked.emit(self.value())
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            value = e.pos().x() / self.width() * self.maximum()
        else:
            value = (self.height() - e.pos().y()) / self.height() * self.maximum()

        self.setValue(int(value))
        super().mousePressEvent(e)

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
