from __future__ import annotations

import datetime

from typing_extensions import Self

from prettyqt import constants, core


class DateTime(core.QDateTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd hh:mm:ss.zzzzzz")

    def __reduce__(self):
        return type(self), (self.date(), self.time(), self.get_timezone())

    def __format__(self, format_spec: constants.DateFormatStr):
        if format_spec in constants.DATE_FORMAT:
            return self.to_format(format_spec)
        return self.toString(format_spec)

    @classmethod
    def from_seconds(cls, seconds: float) -> Self:
        new = cls()
        new.setMSecsSinceEpoch(int(seconds * 1000))
        return new

    def get_value(self) -> datetime.datetime:
        return self.toPython()

    def get_date(self) -> core.Date:
        return core.Date(self.date())

    def get_time(self) -> core.Time:
        return core.Time(self.time())

    def get_timezone(self) -> core.TimeZone:
        return core.TimeZone(self.timeZone())

    def set_timezone(self, zone: str | core.QTimeZone):
        if isinstance(zone, str):
            self.setTimeZone(core.TimeZone(zone))
        else:
            self.setTimeZone(zone)

    def set_time_spec(self, spec: constants.TimeSpecStr | constants.TimeSpec):
        """Set the time specification.

        Args:
            spec: time specification to use
        """
        self.setTimeSpec(constants.TIME_SPEC[spec])

    def get_time_spec(self) -> constants.TimeSpecStr:
        """Return current time specification.

        Returns:
            time specification
        """
        return constants.TIME_SPEC.inverse[self.timeSpec()]

    def to_format(self, fmt: constants.DateFormatStr):
        return self.toString(constants.DATE_FORMAT[fmt])


if __name__ == "__main__":
    date = DateTime(2000, 11, 11, 1, 1, 1)
    dt = DateTime(date)
    pdt = dt.get_value()
