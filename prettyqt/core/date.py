from __future__ import annotations

from prettyqt.qt import QtCore


class Date(QtCore.QDate):
    def __repr__(self):
        template = super().__repr__().split("(")[1]  # type: ignore
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd")

    def __reduce__(self):
        return type(self), (self.year(), self.month(), self.day())

    def add_days(self, days: int) -> Date:
        return Date(self.addDays(days))

    def add_months(self, months: int, calendar: QtCore.QCalendar | None = None) -> Date:
        if calendar:
            return Date(self.addMonths(months, calendar))
        else:
            return Date(self.addMonths(months))

    def add_years(self, years: int, calendar: QtCore.QCalendar | None = None) -> Date:
        if calendar:
            return Date(self.addYears(years, calendar))
        else:
            return Date(self.addYears(years))

    @classmethod
    def get_current_date(cls) -> Date:
        return Date(cls.currentDate())


if __name__ == "__main__":
    dt = Date(2000, 11, 11)
    dt.add_years(30)
