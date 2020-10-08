# -*- coding: utf-8 -*-

import datetime

from qtpy import QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import to_datetime, to_date, to_time


SECTIONS = dict(
    none=QtWidgets.QDateTimeEdit.NoSection,
    am_pm=QtWidgets.QDateTimeEdit.AmPmSection,
    msec=QtWidgets.QDateTimeEdit.MSecSection,
    second=QtWidgets.QDateTimeEdit.SecondSection,
    minute=QtWidgets.QDateTimeEdit.MinuteSection,
    hour=QtWidgets.QDateTimeEdit.HourSection,
    day=QtWidgets.QDateTimeEdit.DaySection,
    month=QtWidgets.QDateTimeEdit.MonthSection,
    year=QtWidgets.QDateTimeEdit.YearSection,
)

QtWidgets.QDateTimeEdit.__bases__ = (widgets.AbstractSpinBox,)


class DateTimeEdit(QtWidgets.QDateTimeEdit):

    value_changed = core.Signal(datetime.datetime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self.datetime_changed)

    def datetime_changed(self, date):
        dt = self.get_datetime()
        self.value_changed.emit(dt)

    def serialize_fields(self):
        return dict(
            calendar_popup=self.calendarPopup(),
            datetime=self.get_datetime(),
            range=(self.min_datetime(), self.max_datetime()),
            display_format=self.displayFormat(),
        )

    def __setstate__(self, state):
        self.__init__(state["datetime"])
        self.setDateTime(state["datetime"])
        self.setEnabled(state.get("enabled", True))
        self.set_range(*state["range"])
        self.setDisplayFormat(state["display_format"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def set_range(self, lower: datetime.datetime, upper: datetime.datetime):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateTimeRange(lower, upper)

    def set_format(self, fmt: str):
        self.setDisplayFormat(fmt)

    def get_value(self) -> datetime.datetime:
        return self.get_datetime()

    def set_value(self, value: datetime.datetime):
        self.setDateTime(value)

    def get_datetime(self) -> datetime.datetime:
        return to_datetime(self.dateTime())

    def min_datetime(self) -> datetime.datetime:
        return to_datetime(self.minimumDateTime())

    def max_datetime(self) -> datetime.datetime:
        return to_datetime(self.maximumDateTime())

    def min_date(self) -> datetime.date:
        return to_date(self.minimumDate())

    def max_date(self) -> datetime.date:
        return to_date(self.maximumDate())

    def get_date(self) -> datetime.date:
        return to_date(self.date())

    def min_time(self) -> datetime.time:
        return to_time(self.minimumTime())

    def max_time(self) -> datetime.time:
        return to_time(self.maximumTime())

    def get_time(self) -> datetime.time:
        return to_time(self.time())


if __name__ == "__main__":
    app = widgets.app()
    widget = DateTimeEdit()
    widget.show()
    app.main_loop()
