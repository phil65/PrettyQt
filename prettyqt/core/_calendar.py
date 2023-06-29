from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict, get_repr


SystemStr = Literal["gregorian", "julian", "milankovic", "jalali", "islamic_civil"]

SYSTEM: bidict[SystemStr, core.QCalendar.System] = bidict(
    gregorian=core.QCalendar.System.Gregorian,
    julian=core.QCalendar.System.Julian,
    milankovic=core.QCalendar.System.Milankovic,
    jalali=core.QCalendar.System.Jalali,
    islamic_civil=core.QCalendar.System.IslamicCivil,
)


class Calendar(core.QCalendar):
    def __init__(self, system: str | core.QCalendar.System = "gregorian"):
        typ = system if isinstance(system, core.QCalendar.System) else SYSTEM[system]
        super().__init__(typ)

    def __repr__(self):
        return get_repr(self, self.name())

    def __reduce__(self):
        return type(self), (self.name(),)

    # def __bool__(self):
    #     return self.isValid()

    def get_date_from_parts(self, year: int, month: int, day: int) -> core.Date:
        return core.Date(self.dateFromParts(year, month, day))


if __name__ == "__main__":
    cal = Calendar("gregorian")
