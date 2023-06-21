from __future__ import annotations

import datetime
from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes


SELECTION_MODE = bidict(
    none=QtWidgets.QCalendarWidget.SelectionMode.NoSelection,
    single=QtWidgets.QCalendarWidget.SelectionMode.SingleSelection,
)

SelectionModeStr = Literal["none", "single"]

VERTICAL_HEADER_FORMAT = bidict(
    none=QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader,
    week_numbers=QtWidgets.QCalendarWidget.VerticalHeaderFormat.ISOWeekNumbers,
)

VerticalHeaderFormatStr = Literal["none", "week_numbers"]

HORIZONTAL_HEADER_FORMAT = bidict(
    single_letter=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames,
    short=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.ShortDayNames,
    long=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.LongDayNames,
    none=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.NoHorizontalHeader,
)

HorizontalHeaderFormatStr = Literal["single_letter", "short", "long", "none"]


class CalendarWidget(widgets.WidgetMixin, QtWidgets.QCalendarWidget):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "firstDayOfWeek": constants.DAY_OF_WEEK,
            "horizontalHeaderFormat": HORIZONTAL_HEADER_FORMAT,
            "verticalHeaderFormat": VERTICAL_HEADER_FORMAT,
            "selectionMode": SELECTION_MODE,
        }
        return maps

    def get_date(self) -> datetime.date:
        return self.selectedDate().toPython()

    def get_value(self) -> datetime.date:
        return self.get_date()

    def set_value(self, value: datatypes.DateType):
        if isinstance(value, str):
            value = QtCore.QDate.fromString(value)
        self.setSelectedDate(value)

    def set_range(
        self,
        lower: datatypes.DateType,
        upper: datatypes.DateType,
    ):
        if isinstance(lower, str):
            lower = QtCore.QDate.fromString(lower)
        if isinstance(upper, str):
            upper = QtCore.QDate.fromString(upper)
        self.setMinimumDate(lower)
        self.setMaximumDate(upper)

    def set_selection_mode(self, mode: SelectionModeStr | None):
        """Set selection mode for given calendar widget.

        Args:
            mode: selection mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode is None:
            mode = "none"
        if mode not in SELECTION_MODE:
            raise InvalidParamError(mode, SELECTION_MODE)
        self.setSelectionMode(SELECTION_MODE[mode])

    def get_selection_mode(self) -> SelectionModeStr:
        """Return current selection mode.

        Returns:
            selection mode
        """
        return SELECTION_MODE.inverse[self.selectionMode()]


if __name__ == "__main__":
    app = widgets.app()
    w = CalendarWidget()
    w.show()
    app.exec()
