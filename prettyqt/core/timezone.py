from __future__ import annotations

from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


NameTypeStr = Literal["default", "long", "short", "offset"]

NAME_TYPE: bidict[NameTypeStr, QtCore.QTimeZone.NameType] = bidict(
    default=QtCore.QTimeZone.NameType.DefaultName,
    long=QtCore.QTimeZone.NameType.LongName,
    short=QtCore.QTimeZone.NameType.ShortName,
    offset=QtCore.QTimeZone.NameType.OffsetName,
)

TimeTypeStr = Literal["standard", "daylight", "generic"]

TIME_TYPE: bidict[TimeTypeStr, QtCore.QTimeZone.TimeType] = bidict(
    standard=QtCore.QTimeZone.TimeType.StandardTime,
    daylight=QtCore.QTimeZone.TimeType.DaylightTime,
    generic=QtCore.QTimeZone.TimeType.GenericTime,
)


class TimeZone(QtCore.QTimeZone):
    def __init__(self, *args):
        match args:
            case (str() as string,):
                super().__init__(QtCore.QByteArray(string.encode()))
            case _:
                super().__init__(*args)

    def __repr__(self):
        return get_repr(self, self.get_id())

    def __str__(self):
        return self.get_id()

    def __reduce__(self):
        return type(self), (self.get_id(),)

    def get_id(self) -> str:
        return self.id().data().decode()

    def get_display_name(
        self,
        date_time: QtCore.QDateTime | TimeTypeStr,
        name_type: NameTypeStr | QtCore.QTimeZone.NameType = "default",
        locale: core.Locale | None = None,
    ) -> str:
        dt = TIME_TYPE.get_enum_value(date_time)
        name_val = NAME_TYPE.get_enum_value(name_type)
        if locale is None:
            locale = core.Locale()
        return self.displayName(dt, name_val, locale)

    def get_time_spec(self) -> constants.TimeSpecStr:
        return constants.TIME_SPEC.inverse[self.timeSpec()]

    # def get_value(self) -> datetime.datetime:
    #     try:
    #         return self.toPython()
    #     except TypeError:
    #         return self.toPyTimeZone()


if __name__ == "__main__":
    date = core.TimeZone(2000, 11, 11)
    dt = TimeZone(date)
