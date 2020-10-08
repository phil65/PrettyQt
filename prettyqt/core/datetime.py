# -*- coding: utf-8 -*-

from typing import Union
import datetime

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError, to_datetime

DATE_FORMATS = bidict(
    text=QtCore.Qt.TextDate,
    iso=QtCore.Qt.ISODate,
    iso_with_ms=QtCore.Qt.ISODateWithMs,
    rfc_2822=QtCore.Qt.RFC2822Date,
)

TIME_SPECS = bidict(
    local_time=QtCore.Qt.LocalTime,
    utc=QtCore.Qt.UTC,
    offset_from_utc=QtCore.Qt.OffsetFromUTC,
    timezone=QtCore.Qt.TimeZone,
)


class DateTime(QtCore.QDateTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]
        return f"DateTime({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd hh:mm:ss.zzzzzz")

    def __reduce__(self):
        return (self.__class__, (self.date(), self.time()))

    def get_value(self) -> datetime.datetime:
        return to_datetime(self)

    def get_date(self) -> core.Date:
        return core.Date(self.date())

    def get_time(self) -> core.Time:
        return core.Time(self.time())

    def get_timezone(self) -> core.TimeZone:
        return core.TimeZone(self.timeZone())

    def set_timezone(self, zone: Union[str, QtCore.QTimeZone]):
        if isinstance(zone, str):
            self.setTimeZone(core.TimeZone(zone))
        else:
            self.setTimeZone(zone)

    def set_time_spec(self, spec: str):
        """Set the time specification.

        Allowed values are "local_time", "utc", "offset_from_utc", "timezone"

        Args:
            mode: time specification to use

        Raises:
            InvalidParamError: time specification does not exist
        """
        if spec not in TIME_SPECS:
            raise InvalidParamError(spec, TIME_SPECS)
        self.setTimeSpec(TIME_SPECS[spec])

    def get_time_spec(self) -> str:
        """Return current time specification.

        Possible values: "local_time", "utc", "offset_from_utc", "timezone"

        Returns:
            time specification
        """
        return TIME_SPECS.inv[self.timeSpec()]

    def to_format(self, fmt: str):
        return self.toString(DATE_FORMATS[fmt])


if __name__ == "__main__":
    date = DateTime(2000, 11, 11, 1, 1)
    dt = DateTime(date)
    print(dt.to_format("iso"))
    print(dt.get_timezone())
    pdt = dt.get_value()
    print(pdt.isoformat())
    print(pdt.tzinfo)
