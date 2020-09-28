# -*- coding: utf-8 -*-

from typing import Optional, Union

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError


TICK_POSITIONS = bidict(
    none=QtWidgets.QSlider.NoTicks,
    both_sides=QtWidgets.QSlider.TicksBothSides,
    above=QtWidgets.QSlider.TicksAbove,
    below=QtWidgets.QSlider.TicksBelow,
)

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)


QtWidgets.QSlider.__bases__ = (widgets.AbstractSlider,)


class Slider(QtWidgets.QSlider):

    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: Union[str, int] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in ORIENTATIONS:
            orientation = ORIENTATIONS[orientation]
        super().__init__(orientation, parent)
        self.valueChanged.connect(self.on_value_change)

    def serialize_fields(self):
        return dict(
            tick_position=self.get_tick_position(),
            tick_interval=self.tickInterval(),
        )

    def __setstate__(self, state):
        self.__init__()
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
        self.set_tick_position(state["tick_position"])
        self.setTickInterval(state["tick_interval"])

    def set_tick_position(self, position: str):
        """Set the tick position for the slider.

        allowed values are "none", "both_sides", "above", "below", "left", "right"
        for vertical orientation of the slider,
        "above" equals to "left" and "below" to "right"

        Args:
            position: position for the ticks
        """
        if position == "left":
            position = "above"
        elif position == "right":
            position = "below"
        elif position not in TICK_POSITIONS:
            raise InvalidParamError(position, TICK_POSITIONS)
        self.setTickPosition(TICK_POSITIONS[position])

    def get_tick_position(self) -> str:
        """Return tick position.

        possible values are "none", "both_sides", "above", "below"

        Returns:
            tick position
        """
        val = TICK_POSITIONS.inv[self.tickPosition()]
        # if self.is_vertical():
        #     if val == "above":
        #         return "left"
        #     elif val == "below":
        #         return "right"
        return val


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    slider = Slider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()
