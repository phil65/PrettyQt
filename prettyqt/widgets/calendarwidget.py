from __future__ import annotations

import datetime
from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict, datatypes


SelectionModeStr = Literal["none", "single"]

SELECTION_MODE: bidict[
    SelectionModeStr, QtWidgets.QCalendarWidget.SelectionMode
] = bidict(
    none=QtWidgets.QCalendarWidget.SelectionMode.NoSelection,
    single=QtWidgets.QCalendarWidget.SelectionMode.SingleSelection,
)

VerticalHeaderFormatStr = Literal["none", "week_numbers"]

VERTICAL_HEADER_FORMAT: bidict[
    VerticalHeaderFormatStr, QtWidgets.QCalendarWidget.VerticalHeaderFormat
] = bidict(
    none=QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader,
    week_numbers=QtWidgets.QCalendarWidget.VerticalHeaderFormat.ISOWeekNumbers,
)

HorizontalHeaderFormatStr = Literal["single_letter", "short", "long", "none"]

HORIZONTAL_HEADER_FORMAT: bidict[
    HorizontalHeaderFormatStr, QtWidgets.QCalendarWidget.HorizontalHeaderFormat
] = bidict(
    single_letter=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames,
    short=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.ShortDayNames,
    long=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.LongDayNames,
    none=QtWidgets.QCalendarWidget.HorizontalHeaderFormat.NoHorizontalHeader,
)


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
        self.setSelectedDate(datatypes.to_date(value))

    def set_range(
        self,
        lower: datatypes.DateType,
        upper: datatypes.DateType,
    ):
        self.setMinimumDate(datatypes.to_date(lower))
        self.setMaximumDate(datatypes.to_date(upper))

    def set_selection_mode(
        self, mode: SelectionModeStr | QtWidgets.QCalendarWidget.SelectionMode | None
    ):
        """Set selection mode for given calendar widget.

        Args:
            mode: selection mode to use
        """
        if mode is None:
            mode = "none"
        self.setSelectionMode(SELECTION_MODE.get_enum_value(mode))

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
