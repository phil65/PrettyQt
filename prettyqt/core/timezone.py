# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict


NAME_TYPES = bidict(
    default=QtCore.QTimeZone.DefaultName,
    long=QtCore.QTimeZone.LongName,
    short=QtCore.QTimeZone.ShortName,
    offset=QtCore.QTimeZone.OffsetName,
)

TIME_TYPES = bidict(
    standard=QtCore.QTimeZone.StandardTime,
    daylight=QtCore.QTimeZone.DaylightTime,
    generic=QtCore.QTimeZone.GenericTime,
)


class TimeZone(QtCore.QTimeZone):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            super().__init__(args[0].encode())
        else:
            super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"TimeZone({self.get_id()!r})"

    def __str__(self):
        return self.get_id()

    def __reduce__(self):
        return (self.__class__, (self.get_id(),))

    def get_id(self) -> str:
        return bytes(self.id()).decode()

    # def get_value(self) -> datetime.datetime:
    #     try:
    #         return self.toPython()
    #     except TypeError:
    #         return self.toPyTimeZone()


if __name__ == "__main__":
    date = core.TimeZone(2000, 11, 11)
    dt = TimeZone(date)
