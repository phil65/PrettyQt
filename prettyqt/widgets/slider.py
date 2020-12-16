from typing import Literal, Optional, Union

from qtpy import QtWidgets

from prettyqt import constants, core, widgets
from prettyqt.utils import InvalidParamError, bidict


TICK_POSITION = bidict(
    none=QtWidgets.QSlider.NoTicks,
    both_sides=QtWidgets.QSlider.TicksBothSides,
    above=QtWidgets.QSlider.TicksAbove,
    below=QtWidgets.QSlider.TicksBelow,
)

TickPositionAllStr = Literal["none", "both_sides", "above", "below", "left", "right"]
TickPositionStr = Literal["none", "both_sides", "above", "below"]


QtWidgets.QSlider.__bases__ = (widgets.AbstractSlider,)


class Slider(QtWidgets.QSlider):

    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: Union[constants.OrientationStr, int] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in constants.ORIENTATION:
            orientation = constants.ORIENTATION[orientation]
        super().__init__(orientation, parent)
        self.valueChanged.connect(self.on_value_change)

    def serialize_fields(self):
        return dict(
            tick_position=self.get_tick_position(),
            tick_interval=self.tickInterval(),
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
        val = TICK_POSITION.inverse[self.tickPosition()]
        # if self.is_vertical():
        #     if val == "above":
        #         return "left"
        #     elif val == "below":
        #         return "right"
        return val


if __name__ == "__main__":
    app = widgets.app()
    slider = Slider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()
