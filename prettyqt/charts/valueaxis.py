from typing import Literal

from qtpy.QtCharts import QtCharts

from prettyqt import charts
from prettyqt.utils import InvalidParamError, bidict


TICK_TYPES = bidict(
    dynamic=QtCharts.QValueAxis.TicksDynamic, fixed=QtCharts.QValueAxis.TicksFixed
)

TickTypeStr = Literal["dynamic", "fixed"]


QtCharts.QValueAxis.__bases__ = (charts.AbstractAxis,)


class ValueAxis(QtCharts.QValueAxis):
    def set_tick_type(self, tick_type: TickTypeStr):
        """Set the tick type of the legend.

        Args:
            tick_type: tick type for the legend

        Raises:
            InvalidParamError: tick type does not exist
        """
        if tick_type not in TICK_TYPES:
            raise InvalidParamError(tick_type, TICK_TYPES)
        self.setTickType(TICK_TYPES[tick_type])

    def get_tick_type(self) -> TickTypeStr:
        """Return current tick type.

        Returns:
            tick_type
        """
        return TICK_TYPES.inverse[self.tickType()]
