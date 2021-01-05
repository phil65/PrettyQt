from __future__ import annotations

import datetime
from typing import Union

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtWidgets


QtWidgets.QDateEdit.__bases__ = (widgets.DateTimeEdit,)


class DateEdit(QtWidgets.QDateEdit):

    value_changed = core.Signal(datetime.datetime)

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setDate(state["date"])
        self.set_range(*state["range"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(
            date=self.get_date(),
            range=(self.min_date(), self.max_date()),
        )

    def set_value(self, value: Union[QtCore.QDate, datetime.date]):
        self.setDate(value)  # type: ignore

    def set_range(
        self,
        lower: Union[QtCore.QDate, datetime.date],
        upper: Union[QtCore.QDate, datetime.date],
    ):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateRange(lower, upper)  # type: ignore

    def get_value(self) -> datetime.date:
        return self.get_date()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DateEdit()
    widget.show()
    app.main_loop()
