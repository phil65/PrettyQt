from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


NAME_TYPE = bidict(
    default=QtCore.QTimeZone.NameType.DefaultName,
    long=QtCore.QTimeZone.NameType.LongName,
    short=QtCore.QTimeZone.NameType.ShortName,
    offset=QtCore.QTimeZone.NameType.OffsetName,
)

NameTypeStr = Literal["default", "long", "short", "offset"]

TIME_TYPE = bidict(
    standard=QtCore.QTimeZone.TimeType.StandardTime,
    daylight=QtCore.QTimeZone.TimeType.DaylightTime,
    generic=QtCore.QTimeZone.TimeType.GenericTime,
)

TimeTypeStr = Literal["standard", "daylight", "generic"]


class TimeZone(QtCore.QTimeZone):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            super().__init__(QtCore.QByteArray(args[0].encode()))
        else:
            super().__init__(*args)

    def __repr__(self):
        return f"{type(self).__name__}({self.get_id()!r})"

    def __str__(self):
        return self.get_id()

    def __reduce__(self):
        return type(self), (self.get_id(),)

    def get_id(self) -> str:
        return bytes(self.id()).decode()

    def get_display_name(
        self,
        datetime: QtCore.QDateTime | TimeTypeStr,
        name_type: NameTypeStr = "default",
        locale: core.Locale | None = None,
    ) -> str:
        if isinstance(datetime, str):
            if datetime not in TIME_TYPE:
                raise InvalidParamError(datetime, TIME_TYPE)
            datetime = TIME_TYPE[datetime]
        if name_type not in NAME_TYPE:
            raise InvalidParamError(name_type, NAME_TYPE)
        if locale is None:
            locale = core.Locale()
        return self.displayName(datetime, NAME_TYPE[name_type], locale)

    # def get_value(self) -> datetime.datetime:
    #     try:
    #         return self.toPython()
    #     except TypeError:
    #         return self.toPyTimeZone()


if __name__ == "__main__":
    date = core.TimeZone(2000, 11, 11)
    dt = TimeZone(date)
