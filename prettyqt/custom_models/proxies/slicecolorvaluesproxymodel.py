from __future__ import annotations

import enum
import logging

from typing import Literal

from prettyqt import constants, core, custom_models, gui
from prettyqt.utils import colors, datatypes, helpers


logger = logging.getLogger(__name__)

ColorModeStr = Literal["all", "visible", "seen", "range"]


class ColorMode(enum.IntEnum):
    All = 1
    Visible = 2
    Seen = 3
    Range = 4


class SliceColorValuesProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "color_values"
    ColorMode = ColorMode
    core.Enum(ColorMode)

    def __init__(self, *args, mode: ColorMode = ColorMode.Visible, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = mode
        self._max = 0.0
        self._role = constants.USER_ROLE
        self._last_span = ((-1, -1), (-1, -1))
        self._low_color = gui.QColor("green")
        self._high_color = gui.QColor("red")

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not self.indexer_contains(index):
            return super().data(index, role)
        match role:
            case constants.BACKGROUND_ROLE:
                return self.get_color_for_index(index)
            case _:
                return super().data(index, role)

    def get_color_for_index(self, index: core.ModelIndex) -> gui.QColor:
        match self._mode:
            case self.ColorMode.Seen:
                data = index.data(self._role)
                new_max = max(self._max, abs(data))
                if new_max != self._max:
                    self._max = new_max
                    self.update_all()
                value = data / self._max
                return self.get_color_for_value(abs(value))
            case self.ColorMode.Visible:
                widget = self.parent()
                h_span = widget.get_visible_section_span("horizontal")
                v_span = widget.get_visible_section_span("vertical")
                if (span := (h_span, v_span)) != self._last_span:
                    self._last_span = span
                    model = self.sourceModel()
                    # TODO: we probably should clamp based on self._indexer.
                    delegator = model[v_span[0] : v_span[1], h_span[0] : h_span[1]]
                    data = delegator.data(self._role)
                    max_ = max(data) if data else 1.0
                    self._max = max_
                    top_left = self.index(v_span[0], h_span[0])
                    bottom_right = self.index(v_span[1], h_span[1])
                    # or do we need to update_all()?
                    self.dataChanged.emit(top_left, bottom_right)
                else:
                    max_ = self._max
                data = abs(index.data(self._role))
                max_ = abs(max(abs(max_), data))
                return self.get_color_for_value(data / max_)

    def get_color_for_value(self, value: float) -> gui.QColor:
        col = helpers.get_color_percentage(
            self._low_color.getRgb(), self._high_color.getRgb(), value * 100
        )
        return gui.QColor(*col)

    def setLowColor(self, color: datatypes.ColorType):
        self._low_color = colors.get_color(color).as_qt()

    def setHighColor(self, color: datatypes.ColorType):
        self._high_color = colors.get_color(color).as_qt()

    def getLowColor(self) -> gui.QColor:
        return self._low_color

    def getHighColor(self) -> gui.QColor:
        return self._high_color

    def setColorMode(self, mode: SliceColorValuesProxyModel.ColorMode):
        self._mode = mode

    def getColorMode(self) -> SliceColorValuesProxyModel.ColorMode:
        return self._mode

    color_mode = core.Property(
        ColorMode,
        getColorMode,
        setColorMode,
    )

    low_color = core.Property(gui.QColor, getLowColor, setLowColor)

    color_mode = core.Property(
        gui.QColor,
        getHighColor,
        setHighColor,
    )


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()

    table = debugging.example_table()
    table.proxifier[1:4, :].color_values()
    table.show()
    with app.debug_mode():
        app.exec()
