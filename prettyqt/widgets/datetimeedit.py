# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

from qtpy import QtWidgets

from prettyqt import core


class DateTimeEdit(QtWidgets.QDateTimeEdit):

    value_changed = core.Signal(datetime.datetime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self.datetime_changed)

    def datetime_changed(self, date):
        self.value_changed.emit(self.get_datetime())

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
        self.setEnabled(state["enabled"])
        self.set_range(*state["range"])
        self.setDisplayFormat(state["display_format"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_range(self, lower: datetime.datetime, upper: datetime.datetime):
        self.setToolTip(f"{lower} <= x <= {upper}")
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

    def min_datetime(self):
        try:
            return self.minimumDateTime().toPython()
        except (TypeError, AttributeError):
            return self.minimumDateTime().toPyDateTime()

    def max_datetime(self):
        try:
            return self.maximumDateTime().toPython()
        except (TypeError, AttributeError):
            return self.maximumDateTime().toPyDateTime()


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DateTimeEdit()
    print(widget.__getstate__())
    widget.show()
    app.exec_()
