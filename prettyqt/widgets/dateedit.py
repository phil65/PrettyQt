# -*- coding: utf-8 -*-

import datetime

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QDateEdit.__bases__ = (widgets.DateTimeEdit,)


class DateEdit(QtWidgets.QDateEdit):

    value_changed = core.Signal(datetime.datetime)

    def serialize_fields(self):
        return dict(
            calendar_popup=self.calendarPopup(),
            date=self.get_date(),
            display_format=self.displayFormat(),
            range=(self.min_date(), self.max_date()),
        )

    def __setstate__(self, state):
        self.__init__(state["date"])
        self.setEnabled(state.get("enabled", True))
        self.setDisplayFormat(state["display_format"])
        self.set_range(*state["range"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def set_value(self, value):
        return self.setDate(value)

    def set_range(self, lower: datetime.date, upper: datetime.date):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateRange(lower, upper)

    def get_value(self) -> datetime.date:
        return self.get_date()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DateEdit()
    widget.show()
    app.exec_()
