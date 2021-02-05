from __future__ import annotations

import datetime

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


class DateTime(QtCore.QDateTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd hh:mm:ss.zzzzzz")

    def __reduce__(self):
        return type(self), (self.date(), self.time(), self.get_timezone())

    def get_value(self) -> datetime.datetime:
        return self.toPython()

    def get_date(self) -> core.Date:
        return core.Date(self.date())

    def get_time(self) -> core.Time:
        return core.Time(self.time())

    def get_timezone(self) -> core.TimeZone:
        return core.TimeZone(self.timeZone())

    def set_timezone(self, zone: str | QtCore.QTimeZone):
        if isinstance(zone, str):
            self.setTimeZone(core.TimeZone(zone))
        else:
            self.setTimeZone(zone)

    def set_time_spec(self, spec: constants.TimeSpecStr):
        """Set the time specification.

        Args:
            spec: time specification to use

        Raises:
            InvalidParamError: time specification does not exist
        """
        if spec not in constants.TIME_SPEC:
            raise InvalidParamError(spec, constants.TIME_SPEC)
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
    date = DateTime(2000, 11, 11, 1, 1)
    dt = DateTime(date)
    print(dt.to_format("iso"))
    print(dt.get_timezone())
    pdt = dt.get_value()
    print(pdt.isoformat())
    print(pdt.tzinfo)
