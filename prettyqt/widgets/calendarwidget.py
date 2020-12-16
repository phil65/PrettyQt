import datetime
from typing import Literal, Optional, Union

from qtpy import QtCore, QtWidgets

from prettyqt import widgets
from prettyqt.utils import InvalidParamError, bidict, to_date


SELECTION_MODE = bidict(
    none=QtWidgets.QCalendarWidget.NoSelection,
    single=QtWidgets.QCalendarWidget.SingleSelection,
)

SelectionModeStr = Literal["none", "single"]

VERTICAL_HEADER_FORMAT = bidict(
    none=QtWidgets.QCalendarWidget.NoVerticalHeader,
    week_numbers=QtWidgets.QCalendarWidget.ISOWeekNumbers,
)

VerticalHeaderFormatStr = Literal["none", "week_numbers"]

HORIZONTAL_HEADER_FORMAT = bidict(
    single_letter=QtWidgets.QCalendarWidget.SingleLetterDayNames,
    short=QtWidgets.QCalendarWidget.ShortDayNames,
    long=QtWidgets.QCalendarWidget.LongDayNames,
    none=QtWidgets.QCalendarWidget.NoHorizontalHeader,
)

HorizontalHeaderFormatStr = Literal["single_letter", "short", "long", "none"]


QtWidgets.QCalendarWidget.__bases__ = (widgets.Widget,)


class CalendarWidget(QtWidgets.QCalendarWidget):
    def serialize_fields(self):
        return dict(date=self.get_date())

    def __setstate__(self, state):
        self.setSelectedDate(state["date"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def get_date(self) -> datetime.date:
        return to_date(self.selectedDate())

    def get_value(self) -> datetime.date:
        return self.get_date()

    def set_value(self, value):
        self.setSelectedDate(value)

    def set_range(
        self,
        min_val: Union[QtCore.QDate, datetime.date],
        max_val: Union[QtCore.QDate, datetime.date],
    ):
        self.setMinimumDate(min_val)
        self.setMaximumDate(max_val)

    def set_selection_mode(self, mode: Optional[SelectionModeStr]):
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
    app.main_loop()
