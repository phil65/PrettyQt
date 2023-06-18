from __future__ import annotations

import enum
import logging
from typing import Literal

from prettyqt import constants, core, custom_models, gui
from prettyqt.utils import colors, helpers

logger = logging.getLogger(__name__)

ColorModeStr = Literal["all", "visible", "seen", "range"]


class ColorMode(enum.IntEnum):
    All = 1
    Visible = 2
    Seen = 3
    Range = 4


class ColorValuesProxyModel(custom_models.SliceIdentityProxyModel):
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

    def data(self, index: core.ModelIndex, role=constants.EDIT_ROLE):
        if not self.indexer_contains(index):
            return super().data(index, role)
        match role, self._mode:
            case constants.BACKGROUND_ROLE, self.ColorMode.Seen:
                data = index.data(self._role)
                self._max = max(self._max, abs(data))
                value = data / self._max
                return self.get_color_for_value(abs(value))
            case constants.BACKGROUND_ROLE, self.ColorMode.Visible:
                widget = self.parent()
                h_span = widget.get_visible_section_span("horizontal")
                v_span = widget.get_visible_section_span("vertical")
                if (span := (h_span, v_span)) != self._last_span:
                    self._last_span = span
                    model = self.sourceModel()
                    delegator = model[v_span[0] : v_span[1], h_span[0] : h_span[1]]
                    data = delegator.data(self._role)
                    max_ = max(data) if data else 1.0
                    self._max = max_
                else:
                    max_ = self._max
                data = abs(index.data(self._role))
                max_ = abs(max(abs(max_), data))
                return self.get_color_for_value(data / max_)
            case _, _:
                return super().data(index, role)

    def get_color_for_value(self, value: float):
        col = helpers.get_color_percentage(
            self._low_color.getRgb(), self._high_color.getRgb(), value * 100
        )
        return gui.Color(*col).as_qt()

    def setLowColor(self, color: gui.QColor):
        self._low_color = colors.get_color(color).as_qt()

    def setHighColor(self, color: gui.QColor):
        self._high_color = colors.get_color(color).as_qt()

    def getLowColor(self) -> gui.QColor:
        return self._low_color

    def getHighColor(self) -> gui.QColor:
        return self._high_color

    def setColorMode(self, mode: ColorValuesProxyModel.ColorMode):
        self._mode = mode

    def getColorMode(self) -> ColorValuesProxyModel.ColorMode:
        return self._mode

    color_mode = core.Property(
        ColorMode,
        getColorMode,
        setColorMode,
    )

    low_color = core.Property(
        gui.QColor,
        getLowColor,
        setLowColor
    )

    color_mode = core.Property(
        gui.QColor,
        getHighColor,
        setHighColor,
    )


if __name__ == "__main__":
    from prettyqt import widgets
    import pandas as pd
    import numpy as np
    app = widgets.app()
    tuples = [
        "one",
        "two",
        "one",
        "two",
        "one",
        "two",
        "one",
        "two",
    ] * 10
    df = pd.DataFrame(np.random.randn(80, 80), index=tuples, columns=tuples)
    table = widgets.TableView()
    table.set_delegate("variant")
    table.set_model(df)
    table.proxifier[:2, :].color_values()
    table.show()
    with app.debug_mode():
        app.main_loop()
