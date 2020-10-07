# -*- coding: utf-8 -*-

from typing import Union
import datetime

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict

DATE_FORMATS = bidict(
    text=QtCore.Qt.TextDate,
    iso=QtCore.Qt.ISODate,
    iso_with_ms=QtCore.Qt.ISODateWithMs,
    rfc_2822=QtCore.Qt.RFC2822Date,
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
        try:
            return self.toPython()
        except TypeError:
            return self.toPyDateTime()

    def get_timezone(self):
        return core.TimeZone(self.timeZone())

    def set_timezone(self, zone: Union[str, QtCore.QTimeZone]):
        if isinstance(zone, str):
            self.setTimeZone(core.TimeZone(zone))
        else:
            self.setTimeZone(zone)

    def to_format(self, fmt: str):
        return self.toString(DATE_FORMATS[fmt])


if __name__ == "__main__":
    date = DateTime(2000, 11, 11, 1, 1)
    dt = DateTime(date)
    pdt = dt.get_value()
