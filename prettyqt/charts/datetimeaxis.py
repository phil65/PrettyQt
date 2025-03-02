from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import charts
from prettyqt.utils import datatypes


if TYPE_CHECKING:
    import datetime


class DateTimeAxis(charts.AbstractAxisMixin, charts.QDateTimeAxis):
    def set_min(self, minimum: datatypes.DateTimeType):
        """Set minimum value for axis."""
        minimum = datatypes.to_datetime(minimum)
        self.setMin(minimum)

    def get_min(self) -> datetime.datetime:
        return self.min().toPython()

    def set_max(self, maximum: datatypes.DateTimeType):
        """Set maximum value for axis."""
        maximum = datatypes.to_datetime(maximum)
        self.setMax(maximum)

    def get_max(self) -> datetime.datetime:
        return self.max().toPython()

    def set_range(self, minimum: datatypes.DateTimeType, maximum: datatypes.DateTimeType):
        """Set value range of datetime axis."""
        self.setRange(datatypes.to_datetime(minimum), datatypes.to_datetime(maximum))
