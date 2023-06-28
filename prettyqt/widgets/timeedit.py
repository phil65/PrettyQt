from __future__ import annotations

import datetime

from prettyqt import core, widgets
from prettyqt.utils import datatypes


class TimeEdit(widgets.DateTimeEditMixin, widgets.QTimeEdit):
    value_changed = core.Signal(datetime.datetime)

    def set_range(self, lower: datatypes.TimeType, upper: datatypes.TimeType):
        # self.setToolTip(f"{lower.toString()} <= x <= {upper.toString()}")
        self.setTimeRange(datatypes.to_time(lower), datatypes.to_time(upper))

    def get_value(self) -> datetime.time:
        return self.get_time()

    def set_value(self, value: datatypes.TimeType):
        self.set_time(value)

    def set_time(self, value: datatypes.TimeType):
        super().setTime(datatypes.to_time(value))

if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = TimeEdit()
    widget.set_time("02:04:10")
    widget.show()
    app.exec()
