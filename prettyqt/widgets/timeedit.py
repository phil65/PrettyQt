# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

from qtpy import QtWidgets
from prettyqt import core


class TimeEdit(QtWidgets.QTimeEdit):

    value_changed = core.Signal(datetime.time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)
        self.timeChanged.connect(self.time_changed)

    def time_changed(self, date):
        self.value_changed.emit(self.get_time())

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    time=self.get_time(),
                    display_format=self.displayFormat(),
                    range=(self.min_time(), self.max_time()),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["time"])
        self.setEnabled(state["enabled"])
        self.setDisplayFormat(state["display_format"])
        self.set_range(*state["range"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

    def set_range(self, lower: datetime.time, upper: datetime.time):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setTimeRange(lower, upper)

    def get_value(self):
        return self.get_time()

    def set_value(self, value):
        return self.setTime(value)

    def get_time(self) -> datetime.time:
        try:
            return self.time().toPython()
        except (TypeError, AttributeError):
            return self.time().toPyTime()

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def min_time(self):
        try:
            return self.minimumTime().toPython()
        except (TypeError, AttributeError):
            return self.minimumTime().toPyTime()

    def max_time(self):
        try:
            return self.maximumTime().toPython()
        except (TypeError, AttributeError):
            return self.maximumTime().toPyTime()


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = TimeEdit()
    widget.show()
    app.exec_()
