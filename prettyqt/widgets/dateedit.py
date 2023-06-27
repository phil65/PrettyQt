from __future__ import annotations

import datetime

from prettyqt import core, widgets
from prettyqt.utils import datatypes


class DateEdit(widgets.DateTimeEditMixin, widgets.QDateEdit):
    value_changed = core.Signal(datetime.datetime)

    def set_value(self, value: datatypes.DateType):
        self.setDate(datatypes.to_date(value))

    def set_range(self, lower: datatypes.DateType, upper: datatypes.DateType):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateRange(datatypes.to_date(lower), datatypes.to_date(upper))

    def get_value(self) -> datetime.date:
        return self.get_date()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DateEdit()
    widget.show()
    app.exec()
