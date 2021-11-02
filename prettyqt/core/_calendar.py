from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


SYSTEM = bidict(
    gregorian=QtCore.QCalendar.System.Gregorian,
    julian=QtCore.QCalendar.System.Julian,
    milankovic=QtCore.QCalendar.System.Milankovic,
    jalali=QtCore.QCalendar.System.Jalali,
    islamic_civil=QtCore.QCalendar.System.IslamicCivil,
)


class Calendar(QtCore.QCalendar):
    def __init__(self, system: str | QtCore.QCalendar.System = "gregorian"):
        if isinstance(system, QtCore.QCalendar.System):
            typ = system
        else:
            typ = SYSTEM[system]
        super().__init__(typ)

    def __repr__(self):
        return f"{type(self).__name__}({self.name()!r})"

    def __reduce__(self):
        return type(self), (self.name(),)

    # def __bool__(self):
    #     return self.isValid()

    def get_date_from_parts(self, year: int, month: int, day: int) -> core.Date:
        return core.Date(self.dateFromParts(year, month, day))


if __name__ == "__main__":
    cal = Calendar("gregorian")
    print(repr(cal))
