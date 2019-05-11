# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class DateEdit(QtWidgets.QDateEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    date=self.get_date(),
                    display_format=self.displayFormat(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__init__(state["date"])
        self.setEnabled(state["enabled"])
        self.setDisplayFormat(state["display_format"])

    def get_date(self):
        try:
            return self.date().toPython()
        except (TypeError, AttributeError):
            return self.date().toPyDate()

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DateEdit()
    widget.show()
    app.exec_()
