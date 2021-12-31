from __future__ import annotations

import datetime

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


QtWidgets.QTimeEdit.__bases__ = (widgets.DateTimeEdit,)


class TimeEdit(QtWidgets.QTimeEdit):

    value_changed = core.Signal(datetime.datetime)

    def serialize_fields(self):
        return dict(
            time=self.get_time(),
            range=(self.min_time(), self.max_time()),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setTime(state["time"])
        self.set_range(*state["range"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_range(self, lower: types.TimeType, upper: types.TimeType):
        if isinstance(lower, str):
            lower = core.Time.fromString(lower)
        else:
            lower = core.Time(lower)
        if isinstance(upper, str):
            upper = core.Time.fromString(upper)
        else:
            upper = core.Time(upper)
        self.setToolTip(f"{lower.toString()} <= x <= {upper.toString()}")
        self.setTimeRange(lower, upper)  # type: ignore

    def get_value(self) -> datetime.time:
        return self.get_time()

    def set_value(self, value: types.TimeType):
        if isinstance(value, str):
            value = core.Time.fromString(value)
        return self.setTime(value)  # type: ignore


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = TimeEdit()
    widget.show()
    app.main_loop()
