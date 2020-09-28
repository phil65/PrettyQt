# -*- coding: utf-8 -*-

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError

SLIDER_ACTIONS = bidict(
    none=QtWidgets.QAbstractSlider.SliderNoAction,
    single_step_add=QtWidgets.QAbstractSlider.SliderSingleStepAdd,
    single_step_sub=QtWidgets.QAbstractSlider.SliderSingleStepSub,
    page_step_add=QtWidgets.QAbstractSlider.SliderPageStepAdd,
    page_step_sub=QtWidgets.QAbstractSlider.SliderPageStepSub,
    to_minimum=QtWidgets.QAbstractSlider.SliderToMinimum,
    to_maximum=QtWidgets.QAbstractSlider.SliderToMaximum,
    move=QtWidgets.QAbstractSlider.SliderMove,
)

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)

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
        self.__init__()
        self.set_range(*state["range"])
        self.set_value(state["value"])
        self.setSingleStep(state["single_step"])
        self.setPageStep(state["page_step"])
        self.setTracking(state["has_tracking"])
        self.setInvertedControls(state["inverted_controls"])
        self.setInvertedAppearance(state["inverted_appearance"])

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

    def set_orientation(self, orientation: str):
        """Set the orientation of the slider.

        Allowed values are "horizontal", "vertical"

        Args:
            orientation: orientation for the slider

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise InvalidParamError(orientation, ORIENTATIONS)
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> str:
        """Return current orientation.

        Possible values: "horizontal", "vertical"

        Returns:
            orientation
        """
        return ORIENTATIONS.inv[self.orientation()]

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

    def set_repeat_action(self, action: str, threshold: int = 500, repeat_time: int = 50):
        """Set the repeat action.

        Valid values are "none", "single_step_add", "single_step_sub", "page_step_add",
        "page_step_sub", "to_minimum", "to_maximum", "move"

        Args:
            action: repeat action

        Raises:
            InvalidParamError: invalid repeat action
        """
        if action not in SLIDER_ACTIONS:
            raise InvalidParamError(action, SLIDER_ACTIONS)
        self.setRepeatAction(SLIDER_ACTIONS[action], threshold, repeat_time)

    def get_repeat_action(self) -> str:
        """Get current repeat action.

        Possible values are "none", "single_step_add", "single_step_sub", "page_step_add",
        "page_step_sub", "to_minimum", "to_maximum", "move"

        Returns:
            current repeat action
        """
        return SLIDER_ACTIONS.inv[self.repeatAction()]

    def trigger_action(self, action: str):
        """Trigger slider action.

        Possible values are "none", "single_step_add", "single_step_sub", "page_step_add",
        "page_step_sub", "to_minimum", "to_maximum", "move"

        """
        if action not in SLIDER_ACTIONS:
            raise InvalidParamError(action, SLIDER_ACTIONS)
        self.triggerAction(SLIDER_ACTIONS[action])

    def get_value(self):
        return self.value()

    def set_value(self, value: int):
        self.setValue(value)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    slider = AbstractSlider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()
