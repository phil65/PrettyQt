# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

from qtpy import QtWidgets


class TimeEdit(QtWidgets.QTimeEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)

    def __getstate__(self):
        return dict(calendar_popup=self.calendarPopup(),
                    time=self.get_time(),
                    display_format=self.displayFormat(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["time"])
        self.setEnabled(state["enabled"])
        self.setDisplayFormat(state["display_format"])

    def get_time(self) -> datetime.time:
        try:
            return self.time().toPython()
        except (TypeError, AttributeError):
            return self.time().toPyTime()

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = TimeEdit()
    widget.show()
    app.exec_()
