from __future__ import annotations

import datetime

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtWidgets


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

    def set_range(
        self,
        lower: QtCore.QTime | datetime.time,
        upper: QtCore.QTime | datetime.time,
    ):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setTimeRange(lower, upper)  # type: ignore

    def get_value(self) -> datetime.time:
        return self.get_time()

    def set_value(self, value: datetime.time | QtCore.QTime):
        return self.setTime(value)  # type: ignore


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = TimeEdit()
    widget.show()
    app.main_loop()
