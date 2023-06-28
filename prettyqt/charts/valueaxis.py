from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.utils import bidict


TICK_TYPES = bidict(
    dynamic=charts.QValueAxis.TickType.TicksDynamic,
    fixed=charts.QValueAxis.TickType.TicksFixed,
)

TickTypeStr = Literal["dynamic", "fixed"]


class ValueAxisMixin(charts.AbstractAxisMixin):
    def set_tick_type(self, tick_type: TickTypeStr | charts.QValueAxis.TickType):
        """Set the tick type of the legend.

        Args:
            tick_type: tick type for the legend
        """
        self.setTickType(TICK_TYPES.get_enum_value(tick_type))

    def get_tick_type(self) -> TickTypeStr:
        """Return current tick type.

        Returns:
            tick_type
        """
        return TICK_TYPES.inverse[self.tickType()]


class ValueAxis(ValueAxisMixin, charts.QValueAxis):
    pass
