from __future__ import annotations

import datetime

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import datatypes


class DateEdit(widgets.DateTimeEditMixin, QtWidgets.QDateEdit):
    value_changed = core.Signal(datetime.datetime)

    def set_value(self, value: datatypes.DateType):
        if isinstance(value, str):
            value = QtCore.QDate.fromString(value)
        self.setDate(value)

    def set_range(self, lower: datatypes.DateType, upper: datatypes.DateType):
        if isinstance(lower, str):
            lower = QtCore.QDate.fromString(lower)
        if isinstance(upper, str):
            upper = QtCore.QDate.fromString(upper)
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
