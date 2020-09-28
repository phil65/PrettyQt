# -*- coding: utf-8 -*-

import datetime

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QTimeEdit.__bases__ = (widgets.DateTimeEdit,)


class TimeEdit(QtWidgets.QTimeEdit):

    value_changed = core.Signal(datetime.datetime)

    def serialize_fields(self):
        return dict(
            calendar_popup=self.calendarPopup(),
            time=self.get_time(),
            display_format=self.displayFormat(),
            range=(self.min_time(), self.max_time()),
        )

    def __setstate__(self, state):
        self.__init__(state["time"])
        self.setEnabled(state.get("enabled", True))
        self.setDisplayFormat(state["display_format"])
        self.set_range(*state["range"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def set_range(self, lower: datetime.time, upper: datetime.time):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setTimeRange(lower, upper)

    def get_value(self) -> datetime.time:
        return self.get_time()

    def set_value(self, value: datetime.time):
        return self.setTime(value)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = TimeEdit()
    widget.show()
    app.main_loop()
