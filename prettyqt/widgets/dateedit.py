# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

from qtpy import QtWidgets

from prettyqt import core


class DateEdit(QtWidgets.QDateEdit):

    value_changed = core.Signal(datetime.date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)
        self.dateChanged.connect(self.date_changed)

    def date_changed(self, date):
        self.value_changed.emit(self.get_date())

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    date=self.get_date(),
                    display_format=self.displayFormat(),
                    range=(self.min_date(), self.max_date()),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["date"])
        self.setEnabled(state["enabled"])
        self.setDisplayFormat(state["display_format"])
        self.set_range(*state["range"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

    def set_value(self, value):
        return self.setDate(value)

    def set_range(self, lower: datetime.date, upper: datetime.date):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateRange(lower, upper)

    def get_value(self):
        return self.get_date()

    def get_date(self) -> datetime.date:
        try:
            return self.date().toPython()
        except (TypeError, AttributeError):
            return self.date().toPyDate()

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def min_date(self):
        try:
            return self.minimumDate().toPython()
        except (TypeError, AttributeError):
            return self.minimumDate().toPyDate()

    def max_date(self):
        try:
            return self.maximumDate().toPython()
        except (TypeError, AttributeError):
            return self.maximumDate().toPyDate()


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DateEdit()
    widget.show()
    app.exec_()
