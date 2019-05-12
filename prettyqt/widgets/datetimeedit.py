# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

from qtpy import QtWidgets


class DateTimeEdit(QtWidgets.QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    datetime=self.get_date(),
                    datetime_range=(self.minimumDateTime(), self.maximumDateTime()),
                    display_format=self.displayFormat(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["datetime"])
        self.setDateTime(state["datetime"])
        self.setEnabled(state["enabled"])
        self.setDateTimeRange(*state["datetime_range"])
        self.setDisplayFormat(state["display_format"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_range(self, lower: int, upper: int):
        self.setDateTimeRange(lower, upper)

    def set_format(self, fmt: str):
        self.setDisplayFormat(fmt)

    def get_value(self) -> datetime.datetime:
        return self.get_datetime()

    def set_value(self, value):
        self.setDateTime(value)

    def get_datetime(self) -> datetime.datetime:
        try:
            return self.dateTime().toPython()
        except TypeError:
            return self.dateTime().toPyDateTime()


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DateTimeEdit()
    print(widget.get_datetime())
    widget.show()
    app.exec_()
