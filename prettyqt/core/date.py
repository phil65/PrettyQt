from __future__ import annotations

from typing_extensions import Self

from prettyqt import constants
from prettyqt.qt import QtCore


class Date(QtCore.QDate):
    def __repr__(self):
        template = super().__repr__().split("(")[1]  # type: ignore
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd")

    def __format__(self, format_spec: str):
        return self.toString(format_spec)

    @property
    def _year(self) -> int:
        return self.year()

    @property
    def _month(self) -> int:
        return self.month()

    @property
    def _day(self) -> int:
        return self.day()

    __match_args__ = ("_year", "_month", "_day")

    def __reduce__(self):
        return type(self), (self.year(), self.month(), self.day())

    def add_days(self, days: int) -> Self:
        return type(self)(self.addDays(days))

    def add_months(self, months: int, calendar: QtCore.QCalendar | None = None) -> Self:
        if calendar:
            return type(self)(self.addMonths(months, calendar))
        else:
            return type(self)(self.addMonths(months))

    def add_years(self, years: int, calendar: QtCore.QCalendar | None = None) -> Self:
        if calendar:
            return type(self)(self.addYears(years, calendar))
        else:
            return type(self)(self.addYears(years))

    @classmethod
    def get_current_date(cls) -> Self:
        return cls(cls.currentDate())

    @classmethod
    def from_string(cls, text: str, date_format: constants.DateFormatStr | str) -> Self:
        if date_format in constants.DATE_FORMAT:
            date_format = constants.DATE_FORMAT[date_format]
        return cls(cls.fromString(text, date_format))

    def replace(
        self, year: int | None = None, month: int | None = None, day: int | None = None
    ):
        self.setDate(
            year if year is not None else self.year(),
            month if month is not None else self.month(),
            day if day is not None else self.day(),
        )


if __name__ == "__main__":
    dt = Date(2000, 11, 11)
    dt.add_years(30)
