# -*- coding: utf-8 -*-

from qtpy.QtCharts import QtCharts

from prettyqt import charts
from prettyqt.utils import bidict, InvalidParamError


TICK_TYPES = bidict(
    dynamic=QtCharts.QValueAxis.TicksDynamic, fixed=QtCharts.QValueAxis.TicksFixed
)


QtCharts.QValueAxis.__bases__ = (charts.AbstractAxis,)


class ValueAxis(QtCharts.QValueAxis):
    def set_tick_type(self, tick_type: str):
        """Set the tick type of the legend.

        Allowed values are "left", "right", "top", "bottom"

        Args:
            tick_type: tick type for the legend

        Raises:
            InvalidParamError: tick type does not exist
        """
        if tick_type not in TICK_TYPES:
            raise InvalidParamError(tick_type, TICK_TYPES)
        self.setTickType(TICK_TYPES[tick_type])

    def get_tick_type(self) -> str:
        """Return current tick type.

        Possible values: "left", "right", "top", "bottom"

        Returns:
            tick_type
        """
        return TICK_TYPES.inv[self.tickType()]
