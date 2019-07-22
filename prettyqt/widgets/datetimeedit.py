# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

from qtpy import QtWidgets

from prettyqt import core, widgets


SECTIONS = dict(none=QtWidgets.QDateTimeEdit.NoSection,
                am_pm=QtWidgets.QDateTimeEdit.AmPmSection,
                msec=QtWidgets.QDateTimeEdit.MSecSection,
                second=QtWidgets.QDateTimeEdit.SecondSection,
                minute=QtWidgets.QDateTimeEdit.MinuteSection,
                hour=QtWidgets.QDateTimeEdit.HourSection,
                day=QtWidgets.QDateTimeEdit.DaySection,
                month=QtWidgets.QDateTimeEdit.MonthSection,
                year=QtWidgets.QDateTimeEdit.YearSection)

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

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    datetime=self.get_datetime(),
                    range=(self.min_datetime(), self.max_datetime()),
                    display_format=self.displayFormat(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["datetime"])
        self.setDateTime(state["datetime"])
        self.setEnabled(state.get("enabled", True))
        self.set_range(*state["range"])
        self.setDisplayFormat(state["display_format"])
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))

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
        try:
            return self.dateTime().toPython()
        except TypeError:
            return self.dateTime().toPyDateTime()

    def min_datetime(self) -> datetime.datetime:
        try:
            return self.minimumDateTime().toPython()
        except (TypeError, AttributeError):
            return self.minimumDateTime().toPyDateTime()

    def max_datetime(self) -> datetime.datetime:
        try:
            return self.maximumDateTime().toPython()
        except (TypeError, AttributeError):
            return self.maximumDateTime().toPyDateTime()

    def min_date(self) -> datetime.date:
        try:
            return self.minimumDate().toPython()
        except (TypeError, AttributeError):
            return self.minimumDate().toPyDate()

    def max_date(self) -> datetime.date:
        try:
            return self.maximumDate().toPython()
        except (TypeError, AttributeError):
            return self.maximumDate().toPyDate()

    def get_date(self) -> datetime.date:
        try:
            return self.date().toPython()
        except (TypeError, AttributeError):
            return self.date().toPyDate()

    def min_time(self) -> datetime.time:
        try:
            return self.minimumTime().toPython()
        except (TypeError, AttributeError):
            return self.minimumTime().toPyTime()

    def max_time(self) -> datetime.time:
        try:
            return self.maximumTime().toPython()
        except (TypeError, AttributeError):
            return self.maximumTime().toPyTime()

    def get_time(self) -> datetime.time:
        try:
            return self.time().toPython()
        except (TypeError, AttributeError):
            return self.time().toPyTime()


if __name__ == "__main__":
    app = widgets.app()
    widget = DateTimeEdit()
    widget.show()
    app.exec_()
