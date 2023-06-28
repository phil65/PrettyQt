from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict


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

SLIDER_ACTION: bidict[SliderActionStr, widgets.QAbstractSlider.SliderAction] = bidict(
    none=widgets.QAbstractSlider.SliderAction.SliderNoAction,
    single_step_add=widgets.QAbstractSlider.SliderAction.SliderSingleStepAdd,
    single_step_sub=widgets.QAbstractSlider.SliderAction.SliderSingleStepSub,
    page_step_add=widgets.QAbstractSlider.SliderAction.SliderPageStepAdd,
    page_step_sub=widgets.QAbstractSlider.SliderAction.SliderPageStepSub,
    to_minimum=widgets.QAbstractSlider.SliderAction.SliderToMinimum,
    to_maximum=widgets.QAbstractSlider.SliderAction.SliderToMaximum,
    move=widgets.QAbstractSlider.SliderAction.SliderMove,
)


class AbstractSliderMixin(widgets.WidgetMixin):
    value_changed = core.Signal(int)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "orientation": constants.ORIENTATION,
        }
        return maps

    def on_value_change(self):
        self.value_changed.emit(self.value())

    def is_horizontal(self) -> bool:
        """Check if silder is horizontal.

        Returns:
            True if horizontal, else False
        """
        return self.orientation() == constants.HORIZONTAL

    def is_vertical(self) -> bool:
        """Check if silder is vertical.

        Returns:
            True if vertical, else False
        """
        return self.orientation() == constants.VERTICAL

    def set_horizontal(self):
        """Set slider orientation to horizontal."""
        self.setOrientation(constants.HORIZONTAL)

    def set_vertical(self):
        """Set slider orientation to vertical."""
        self.setOrientation(constants.VERTICAL)

    def set_orientation(
        self, orientation: constants.OrientationStr | constants.Orientation
    ):
        """Set the orientation of the slider.

        Args:
            orientation: orientation for the slider
        """
        self.setOrientation(constants.ORIENTATION.get_enum_value(orientation))

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
        self,
        action: SliderActionStr | widgets.QAbstractSlider.SliderAction,
        threshold: int = 500,
        repeat_time: int = 50,
    ):
        """Set the repeat action.

        Args:
            action: repeat action
            threshold: initial delay in ms
            repeat_time: repeat time in ms
        """
        self.setRepeatAction(SLIDER_ACTION.get_enum_value(action), threshold, repeat_time)

    def get_repeat_action(self) -> SliderActionStr:
        """Get current repeat action.

        Returns:
            current repeat action
        """
        return SLIDER_ACTION.inverse[self.repeatAction()]

    def trigger_action(
        self, action: SliderActionStr | widgets.QAbstractSlider.SliderAction
    ):
        """Trigger slider action."""
        self.triggerAction(SLIDER_ACTION.get_enum_value(action))

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: int):
        self.setValue(value)

    def on_scrollbar_range_changed(self, minval: int, maxval: int):
        if self.value() >= self.maximum() - 1:
            self.setValue(maxval)

    def set_auto_scroll_to_end(self, scroll: bool = True):
        """Set to always scroll to the end when range changes."""
        if scroll:
            self.rangeChanged.connect(self.on_scrollbar_range_changed)
        else:
            self.rangeChanged.disconnect(self.on_scrollbar_range_changed)


class AbstractSlider(AbstractSliderMixin, widgets.QAbstractSlider):
    pass


if __name__ == "__main__":
    app = widgets.app()
    slider = AbstractSlider()
    slider.setRange(0, 100)
    slider.show()
    app.exec()
