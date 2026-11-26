import datetime as dt

from prettyqt import core, widgets
from prettyqt.utils import datatypes


class DateEdit(widgets.DateTimeEditMixin, widgets.QDateEdit):
    """Widget for editing dates based on the QDateTimeEdit widget."""

    value_changed = core.Signal(dt.datetime)

    def set_value(self, value: datatypes.DateType):
        self.setDate(datatypes.to_date(value))

    def set_range(self, lower: datatypes.DateType, upper: datatypes.DateType):
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateRange(datatypes.to_date(lower), datatypes.to_date(upper))

    def get_value(self) -> dt.date:
        return self.get_date()

    @classmethod
    def setup_example(cls):
        widget = cls()
        widget.set_value("01.03.1998")
        return widget


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DateEdit.setup_example()
    widget.show()
    app.exec()
