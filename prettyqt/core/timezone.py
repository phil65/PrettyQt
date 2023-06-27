from __future__ import annotations

from typing import Literal

from prettyqt import constants, core
from prettyqt.utils import bidict, get_repr


NameTypeStr = Literal["default", "long", "short", "offset"]

NAME_TYPE: bidict[NameTypeStr, core.QTimeZone.NameType] = bidict(
    default=core.QTimeZone.NameType.DefaultName,
    long=core.QTimeZone.NameType.LongName,
    short=core.QTimeZone.NameType.ShortName,
    offset=core.QTimeZone.NameType.OffsetName,
)

TimeTypeStr = Literal["standard", "daylight", "generic"]

TIME_TYPE: bidict[TimeTypeStr, core.QTimeZone.TimeType] = bidict(
    standard=core.QTimeZone.TimeType.StandardTime,
    daylight=core.QTimeZone.TimeType.DaylightTime,
    generic=core.QTimeZone.TimeType.GenericTime,
)


class TimeZone(core.QTimeZone):
    def __init__(self, *args):
        match args:
            case (str() as string,):
                super().__init__(core.QByteArray(string.encode()))
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
        date_time: core.QDateTime | TimeTypeStr,
        name_type: NameTypeStr | core.QTimeZone.NameType = "default",
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
