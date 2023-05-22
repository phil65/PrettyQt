from __future__ import annotations

import datetime

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes


class TimeEdit(widgets.DateTimeEditMixin, QtWidgets.QTimeEdit):
    value_changed = core.Signal(datetime.datetime)

    def set_range(self, lower: datatypes.TimeType, upper: datatypes.TimeType):
        if isinstance(lower, str):
            lower = core.Time.fromString(lower)
        else:
            lower = core.Time(lower)
        if isinstance(upper, str):
            upper = core.Time.fromString(upper)
        else:
            upper = core.Time(upper)
        self.setToolTip(f"{lower.toString()} <= x <= {upper.toString()}")
        self.setTimeRange(lower, upper)

    def get_value(self) -> datetime.time:
        return self.get_time()

    def set_value(self, value: datatypes.TimeType):
        if isinstance(value, str):
            value = core.Time.fromString(value)
        return self.setTime(value)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = TimeEdit()
    widget.show()
    app.main_loop()
