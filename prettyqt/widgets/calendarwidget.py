# -*- coding: utf-8 -*-

import datetime
from typing import Optional

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError, to_date


SELECTION_MODES = bidict(
    none=QtWidgets.QCalendarWidget.NoSelection,
    single=QtWidgets.QCalendarWidget.SingleSelection,
)

HEADER_FORMATS = bidict(
    none=QtWidgets.QCalendarWidget.NoVerticalHeader,
    week_numbers=QtWidgets.QCalendarWidget.ISOWeekNumbers,
)


QtWidgets.QCalendarWidget.__bases__ = (widgets.Widget,)


class CalendarWidget(QtWidgets.QCalendarWidget):
    def serialize_fields(self):
        return dict(date=self.get_date())

    def __setstate__(self, state):
        self.__init__()
        self.setSelectedDate(state["date"])

    def get_date(self) -> datetime.date:
        return to_date(self.selectedDate())

    def get_value(self) -> datetime.date:
        return self.get_date()

    def set_value(self, value):
        self.setSelectedDate(value)

    def set_selection_mode(self, mode: Optional[str]):
        """Set selection mode for given calendar widget.

        Allowed values are "single" or "none"

        Args:
            mode: selection mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode is None:
            mode = "none"
        if mode not in SELECTION_MODES:
            raise InvalidParamError(mode, SELECTION_MODES)
        self.setSelectionMode(SELECTION_MODES[mode])

    def get_selection_mode(self) -> str:
        """Return current selection mode.

        Possible values: "single" or "none"

        Returns:
            selection mode
        """
        return SELECTION_MODES.inv[self.selectionMode()]


if __name__ == "__main__":
    app = widgets.app()
    w = CalendarWidget()
    w.show()
    app.main_loop()
