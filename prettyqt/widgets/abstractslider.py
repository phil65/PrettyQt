from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


SLIDER_ACTION = bidict(
    none=QtWidgets.QAbstractSlider.SliderNoAction,
    single_step_add=QtWidgets.QAbstractSlider.SliderSingleStepAdd,
    single_step_sub=QtWidgets.QAbstractSlider.SliderSingleStepSub,
    page_step_add=QtWidgets.QAbstractSlider.SliderPageStepAdd,
    page_step_sub=QtWidgets.QAbstractSlider.SliderPageStepSub,
    to_minimum=QtWidgets.QAbstractSlider.SliderToMinimum,
    to_maximum=QtWidgets.QAbstractSlider.SliderToMaximum,
    move=QtWidgets.QAbstractSlider.SliderMove,
)

SliderActionStr = Literal[
    "none",
    "single_step_add",
    "single_step_sub",
    "page_step_add",
    "page_step_sub",
    "to_minimum",
    "to_maximum",
    "move",
]

QtWidgets.QAbstractSlider.__bases__ = (widgets.Widget,)


class AbstractSlider(QtWidgets.QAbstractSlider):

    value_changed = core.Signal(int)

    def on_value_change(self):
        self.value_changed.emit(self.value())

    def serialize_fields(self):
        return dict(
            range=(self.minimum(), self.maximum()),
            value=self.value(),
            has_tracking=self.hasTracking(),
            inverted_controls=self.invertedControls(),
            inverted_appearance=self.invertedAppearance(),
            single_step=self.singleStep(),
            page_step=self.pageStep(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_range(*state["range"])
        self.set_value(state["value"])
        self.setSingleStep(state["single_step"])
        self.setPageStep(state["page_step"])
        self.setTracking(state["has_tracking"])
        self.setInvertedControls(state["inverted_controls"])
        self.setInvertedAppearance(state["inverted_appearance"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def is_horizontal(self) -> bool:
        """Check if silder is horizontal.

        Returns:
            True if horizontal, else False
        """
        return self.orientation() == QtCore.Qt.Horizontal

    def is_vertical(self) -> bool:
        """Check if silder is vertical.

        Returns:
            True if vertical, else False
        """
        return self.orientation() == QtCore.Qt.Vertical

    def set_horizontal(self):
        """Set slider orientation to horizontal."""
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        """Set slider orientation to vertical."""
        self.setOrientation(QtCore.Qt.Vertical)

    def set_orientation(self, orientation: constants.OrientationStr):
        """Set the orientation of the slider.

        Args:
            orientation: orientation for the slider

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.setOrientation(constants.ORIENTATION[orientation])

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def scroll_to_min(self):
        """Scroll to the minimum value of the slider."""
        self.setValue(self.minimum())

    def scroll_to_max(self):
        """Scroll to the maximum value of the slider."""
        self.setValue(self.maximum())

    def set_range(self, min_val: int, max_val: int):
        self.setRange(min_val, max_val)

    def set_step_size(self, step_size: int):
        self.setSingleStep(step_size)

    def set_repeat_action(
        self, action: SliderActionStr, threshold: int = 500, repeat_time: int = 50
    ):
        """Set the repeat action.

        Args:
            action: repeat action

        Raises:
            InvalidParamError: invalid repeat action
        """
        if action not in SLIDER_ACTION:
            raise InvalidParamError(action, SLIDER_ACTION)
        self.setRepeatAction(SLIDER_ACTION[action], threshold, repeat_time)

    def get_repeat_action(self) -> SliderActionStr:
        """Get current repeat action.

        Returns:
            current repeat action
        """
        return SLIDER_ACTION.inverse[self.repeatAction()]

    def trigger_action(self, action: SliderActionStr):
        """Trigger slider action."""
        if action not in SLIDER_ACTION:
            raise InvalidParamError(action, SLIDER_ACTION)
        self.triggerAction(SLIDER_ACTION[action])

    def get_value(self):
        return self.value()

    def set_value(self, value: int):
        self.setValue(value)

    def on_scrollbar_range_changed(self, minval, maxval):
        if self.value() >= self.maximum() - 1:
            self.setValue(maxval)

    def set_auto_scroll_to_end(self, scroll: bool = True):
        """Set to always scroll to the end when range changes."""
        if scroll:
            self.rangeChanged.connect(self.on_scrollbar_range_changed)
        else:
            self.rangeChanged.disconnect(self.on_scrollbar_range_changed)


if __name__ == "__main__":
    app = widgets.app()
    slider = AbstractSlider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()
