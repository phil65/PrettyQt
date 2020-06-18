# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime
from typing import Optional

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict

SELECTION_MODES = bidict(none=QtWidgets.QCalendarWidget.NoSelection,
                         single=QtWidgets.QCalendarWidget.SingleSelection)

HEADER_FORMATS = bidict(none=QtWidgets.QCalendarWidget.NoVerticalHeader,
                        week_numbers=QtWidgets.QCalendarWidget.ISOWeekNumbers)


QtWidgets.QCalendarWidget.__bases__ = (widgets.Widget,)


class CalendarWidget(QtWidgets.QCalendarWidget):

    def __getstate__(self):
        return dict(date=self.selectedDate())

    def __setstate__(self, state):
        self.__init__()
        self.setSelectedDate(state["date"])

    def get_date(self) -> datetime.date:
        try:
            return self.selectedDate().toPyDate()  # pyqt5
        except (TypeError, AttributeError):
            return self.selectedDate().toPython()

    def get_value(self) -> datetime.date:
        return self.get_date()

    def set_value(self, value):
        self.setSelectedDate(value)

    def set_selection_mode(self, mode: Optional[str]):
        """set selection mode for given calendar widget

        Allowed values are "single" or "none"

        Args:
            mode: selection mode to use

        Raises:
            ValueError: mode does not exist
        """
        if mode is None:
            mode = "none"
        if mode not in SELECTION_MODES:
            raise ValueError("Format must be either 'single' or 'None'")
        self.setSelectionMode(SELECTION_MODES[mode])

    def get_selection_mode(self) -> str:
        """returns current selection mode

        Possible values: "single" or "none"

        Returns:
            selection mode
        """
        return SELECTION_MODES.inv[self.selectionMode()]


if __name__ == "__main__":
    app = widgets.app()
    w = CalendarWidget()
    w.show()
    app.exec_()
