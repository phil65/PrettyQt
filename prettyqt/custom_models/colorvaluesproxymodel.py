from __future__ import annotations

import enum
import logging
from typing import Literal

from prettyqt import constants, core, gui
from prettyqt.utils import colors, helpers

logger = logging.getLogger(__name__)

ColorModeStr = Literal["all", "visible", "seen", "range"]


class ColorMode(enum.IntEnum):
    All = 1
    Visible = 2
    Seen = 3
    Range = 4


class ColorValuesProxyModel(core.IdentityProxyModel):
    ID = "color_values"
    ColorMode = ColorMode
    core.Enum(ColorMode)

    def __init__(self, *args, mode: ColorMode = ColorMode.Visible, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = mode
        self._max = 0.0
        self._last_span = ((-1, -1), (-1, -1))
        self._low_color = gui.QColor("green")
        self._high_color = gui.QColor("red")

    def data(self, index: core.ModelIndex, role=constants.EDIT_ROLE):
        match role, self._mode:
            case constants.BACKGROUND_ROLE, self.ColorMode.Seen:
                data = index.data(constants.USER_ROLE)
                self._max = max(self._max, abs(data))
                value = abs(data / self._max)
                return gui.Color.from_cmyk(0, value, value, 0).as_qt()
            case constants.BACKGROUND_ROLE, self.ColorMode.Visible:
                widget = self.parent()
                hor_span = widget.get_visible_section_span("horizontal")
                ver_span = widget.get_visible_section_span("vertical")
                if (span := (hor_span, ver_span)) != self._last_span:
                    self._last_span = span
                    model = self.sourceModel()
                    delegator = model[
                        ver_span[0] : ver_span[1], hor_span[0] : hor_span[1]
                    ]
                    data = delegator.data(constants.USER_ROLE)
                    max_ = max(data) if data else 1.0
                    self._max = max_
                else:
                    max_ = self._max
                data = abs(index.data(constants.USER_ROLE))
                max_ = abs(max(abs(max_), data))
                value = data / max_
                col = helpers.get_color_percentage(
                    self._low_color.getRgb(), self._high_color.getRgb(), value * 100
                )
                return gui.Color(*col).as_qt()
        return super().data(index, role)

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
    table.proxifier.color_values()
    table.show()
    with app.debug_mode():
        app.main_loop()
