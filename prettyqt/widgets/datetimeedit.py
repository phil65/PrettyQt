# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class DateTimeEdit(QtWidgets.QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    datetime=self.get_date(),
                    display_format=self.displayFormat(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__init__(state["datetime"])
        self.setDateTime(state["datetime"])
        self.setEnabled(state["enabled"])
        self.setDisplayFormat(state["display_format"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def get_date(self):
        try:
            return self.dateTime().toPython()
        except TypeError:
            return self.dateTime().toPyDateTime()


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DateTimeEdit()
    print(widget.get_date())
    widget.show()
    app.exec_()
