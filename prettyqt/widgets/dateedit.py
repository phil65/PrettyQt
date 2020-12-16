import datetime
from typing import Union

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets


QtWidgets.QDateEdit.__bases__ = (widgets.DateTimeEdit,)


class DateEdit(QtWidgets.QDateEdit):

    value_changed = core.Signal(datetime.datetime)

    def __setstate__(self, state):
        self.setDate(state["date"])
        self.setEnabled(state.get("enabled", True))
        self.setDisplayFormat(state["display_format"])
        self.set_range(*state["range"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(
            calendar_popup=self.calendarPopup(),
            date=self.get_date(),
            display_format=self.displayFormat(),
            range=(self.min_date(), self.max_date()),
        )

    def set_value(self, value):
        return self.setDate(value)

    def set_range(
        self,
        lower: Union[QtCore.QDate, datetime.date],
        upper: Union[QtCore.QDate, datetime.date],
    ):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateRange(lower, upper)

    def get_value(self) -> datetime.date:
        return self.get_date()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DateEdit()
    widget.show()
    app.main_loop()
