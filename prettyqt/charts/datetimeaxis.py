from __future__ import annotations

import datetime

from prettyqt import charts
from prettyqt.utils import datatypes


class DateTimeAxis(charts.AbstractAxisMixin, charts.QDateTimeAxis):
    def set_min(self, minimum: datatypes.DateTimeType):
        minimum = datatypes.to_datetime(minimum)
        self.setMin(minimum)

    def get_min(self) -> datetime.datetime:
        return self.min().toPython()

    def set_max(self, maximum: datatypes.DateTimeType):
        maximum = datatypes.to_datetime(maximum)
        self.setMax(maximum)

    def get_max(self) -> datetime.datetime:
        return self.max().toPython()

    def set_range(self, minimum: datatypes.DateTimeType, maximum: datatypes.DateTimeType):
        self.setRange(datatypes.to_datetime(minimum), datatypes.to_datetime(maximum))
